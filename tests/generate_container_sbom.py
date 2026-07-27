"""Generate a deterministic CycloneDX inventory from a locally loaded image."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

_REQUIRED_PROVENANCE_LABELS = (
    "org.opencontainers.image.revision",
    "org.opencontainers.image.version",
)
_OPTIONAL_PROVENANCE_LABELS = ("io.nmulti.proxmox-sdk.wheel.sha256",)


class SbomError(RuntimeError):
    """Raised when an image inventory cannot be collected safely."""


def _run(arguments: list[str], *, timeout: int = 180) -> str:
    completed = subprocess.run(
        arguments,
        check=True,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    return completed.stdout


def _container_run_arguments(
    *,
    image: str,
    platform: str,
    entrypoint: str,
    arguments: list[str],
    emulator: Path | None,
) -> list[str]:
    command = ["docker", "run", "--rm", "--platform", platform]
    if emulator is None:
        return [*command, "--entrypoint", entrypoint, image, *arguments]

    try:
        emulator_path = emulator.resolve(strict=True)
    except OSError as exc:
        raise SbomError(f"Container emulator does not exist: {emulator}") from exc
    if not emulator_path.is_file():
        raise SbomError(f"Container emulator is not a file: {emulator_path}")
    container_emulator = "/tmp/proxmox-sdk-sbom-emulator"
    return [
        *command,
        "--volume",
        f"{emulator_path}:{container_emulator}:ro",
        "--entrypoint",
        container_emulator,
        image,
        entrypoint,
        entrypoint,
        *arguments,
    ]


def generate_sbom(
    *,
    image: str,
    platform: str,
    emulator: Path | None = None,
) -> dict[str, Any]:
    """Return a CycloneDX document for OS and Python packages in ``image``."""

    inspect_values = json.loads(_run(["docker", "image", "inspect", image]))
    if not isinstance(inspect_values, list) or len(inspect_values) != 1:
        raise SbomError(f"Expected one inspected image, got {inspect_values!r}")
    inspected = inspect_values[0]
    if not isinstance(inspected, dict) or not isinstance(inspected.get("Id"), str):
        raise SbomError("Docker image inspection did not return an image ID")
    expected_architecture = platform.removeprefix("linux/")
    if inspected.get("Os") != "linux" or inspected.get("Architecture") != expected_architecture:
        raise SbomError(
            "Docker image platform does not match the requested SBOM platform: "
            f"requested={platform!r}, inspected="
            f"{inspected.get('Os')!r}/{inspected.get('Architecture')!r}"
        )
    config = inspected.get("Config")
    labels = config.get("Labels") if isinstance(config, dict) else None
    if labels is None:
        labels = {}
    if not isinstance(labels, dict) or not all(
        isinstance(key, str) and isinstance(value, str) for key, value in labels.items()
    ):
        raise SbomError("Docker image labels are not a string mapping")
    missing_labels = [label for label in _REQUIRED_PROVENANCE_LABELS if not labels.get(label)]
    if missing_labels:
        raise SbomError(f"Docker image is missing provenance labels: {missing_labels}")

    apk_output = _run(
        _container_run_arguments(
            image=image,
            platform=platform,
            entrypoint="/sbin/apk",
            arguments=["list", "--installed"],
            emulator=emulator,
        )
    )
    python_script = (
        "import importlib.metadata as m,json;"
        "print(json.dumps(sorted((d.metadata['Name'],d.version) for d in m.distributions())))"
    )
    python_output = _run(
        _container_run_arguments(
            image=image,
            platform=platform,
            entrypoint="/app/.venv/bin/python",
            arguments=["-c", python_script],
            emulator=emulator,
        )
    )
    python_packages = json.loads(python_output)
    if not isinstance(python_packages, list):
        raise SbomError("Python package inventory is not a list")

    components: list[dict[str, str]] = []
    for line in sorted(filter(None, (item.strip() for item in apk_output.splitlines()))):
        package_identity = line.split(maxsplit=1)[0]
        match = re.fullmatch(r"(.+)-(\d[^\s]*)", package_identity)
        if match is None:
            raise SbomError(f"Invalid Alpine package identity: {package_identity!r}")
        name, version = match.groups()
        components.append(
            {
                "bom-ref": f"apk:{package_identity}",
                "name": name,
                "type": "library",
                "version": version,
            }
        )
    for item in python_packages:
        if (
            not isinstance(item, list)
            or len(item) != 2
            or not all(isinstance(value, str) for value in item)
        ):
            raise SbomError(f"Invalid Python distribution identity: {item!r}")
        name, version = item
        components.append(
            {
                "bom-ref": f"pypi:{name.lower()}@{version}",
                "name": name,
                "type": "library",
                "version": version,
            }
        )
    components.sort(key=lambda component: component["bom-ref"])

    image_id = inspected["Id"]
    serial = uuid.uuid5(uuid.NAMESPACE_URL, f"{image_id}:{platform}")
    properties = [
        {"name": "oci.image.id", "value": image_id},
        {"name": "oci.image.platform", "value": platform},
    ]
    properties.extend(
        {
            "name": f"oci.image.label.{label}",
            "value": labels[label],
        }
        for label in (*_REQUIRED_PROVENANCE_LABELS, *_OPTIONAL_PROVENANCE_LABELS)
        if label in labels
    )
    return {
        "$schema": "http://cyclonedx.org/schema/bom-1.5.schema.json",
        "bomFormat": "CycloneDX",
        "components": components,
        "metadata": {
            "component": {
                "bom-ref": image_id,
                "name": image,
                "properties": properties,
                "type": "container",
            }
        },
        "serialNumber": f"urn:uuid:{serial}",
        "specVersion": "1.5",
        "version": 1,
    }


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--platform", required=True, choices=("linux/amd64", "linux/arm64"))
    parser.add_argument(
        "--emulator",
        type=Path,
        help="Optional reviewed static user-mode emulator for hosts without binfmt_misc",
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Write one deterministic CycloneDX JSON document."""

    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    document = generate_sbom(
        image=args.image,
        platform=args.platform,
        emulator=args.emulator,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
