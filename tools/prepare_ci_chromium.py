"""Acquire Debian 12 Chromium libraries without changing the runner image."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import re
import stat
import subprocess
from pathlib import Path

KEYRING = Path("/usr/share/keyrings/debian-archive-keyring.gpg")
HOST_STATUS = Path("/var/lib/dpkg/status")
FONT_PACKAGE = "fonts-liberation"
CORE_ABI_PREFIXES = ("libc6", "libc-bin", "libc-dev-bin", "ld-linux", "ld.so", "musl")
PACKAGES = (
    "libasound2",
    "libatk-bridge2.0-0",
    "libatk1.0-0",
    "libatspi2.0-0",
    "libcairo2",
    "libcups2",
    "libdbus-1-3",
    "libdrm2",
    "libgbm1",
    "libglib2.0-0",
    "libnspr4",
    "libnss3",
    "libpango-1.0-0",
    "libx11-6",
    "libxcb1",
    "libxcomposite1",
    "libxdamage1",
    "libxext6",
    "libxfixes3",
    "libxkbcommon0",
    "libxrandr2",
)


def require_supported_host() -> None:
    """Refuse privilege or an ABI outside the actual untrusted runner lane."""
    if os.geteuid() == 0:
        raise ValueError("Chromium library preparation requires an unprivileged job")
    release = platform.freedesktop_os_release()
    if (release.get("ID"), release.get("VERSION_ID"), platform.machine()) != (
        "debian",
        "12",
        "x86_64",
    ):
        raise ValueError("Chromium library preparation requires Debian 12 amd64")
    metadata = KEYRING.lstat()
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_uid != 0 or metadata.st_mode & 0o022:
        raise ValueError("The preinstalled Debian archive keyring must be root controlled")


def require_locked_playwright() -> None:
    """Bind the fixed dependency set to the locked upstream runtime description."""
    package = importlib.metadata.distribution("playwright")
    if package.version != "1.58.0":
        raise ValueError("Chromium preparation requires locked Playwright 1.58.0")
    registry = Path(package.locate_file("playwright/driver/package"))
    native = (registry / "lib/server/registry/nativeDeps.js").read_text(encoding="utf-8")
    section = re.search(r'"debian12-x64":\s*\{.*?chromium:\s*\[([^]]+)\]', native, re.S)
    if section is None or tuple(re.findall(r'"([a-z0-9.+-]+)"', section[1])) != PACKAGES:
        raise ValueError("The fixed Chromium packages differ from locked nativeDeps")
    require_locked_font(native)
    manifest = json.loads((registry / "browsers.json").read_text(encoding="utf-8"))
    revisions = {
        row["name"]: row["revision"]
        for row in manifest["browsers"]
        if row["name"] in {"chromium", "chromium-headless-shell"}
    }
    if revisions != {"chromium": "1208", "chromium-headless-shell": "1208"}:
        raise ValueError("The locked Chromium browser identity changed")


def require_locked_font(native: str) -> None:
    """Keep the single headless font asset tied to the locked tools inventory."""
    tools = re.search(r'"debian12-x64":\s*\{.*?tools:\s*\[([^]]+)\]', native, re.S)
    if tools is None or FONT_PACKAGE not in re.findall(r'"([a-z0-9.+-]+)"', tools[1]):
        raise ValueError("The fixed font package differs from locked nativeDeps tools")


def font_configuration(directory: Path) -> None:
    """Point Fontconfig only at the extracted font package and a private cache."""
    (directory / "fontconfig/fonts.conf").write_text(
        '<?xml version="1.0"?>\n<fontconfig>\n'
        f"  <dir>{directory}/prefix/usr/share/fonts/truetype/liberation</dir>\n"
        f"  <cachedir>{directory}/fontconfig/cache</cachedir>\n"
        "</fontconfig>\n",
        encoding="utf-8",
    )


def private_configuration(directory: Path) -> Path:
    """Isolate APT state while retaining a private snapshot of installed host ABI."""
    if not directory.is_absolute() or re.fullmatch(r"/[A-Za-z0-9_./-]+", str(directory)) is None:
        raise ValueError("The job directory must be an absolute APT-safe path")
    if directory.parent.resolve() != directory.parent:
        raise ValueError("The job directory parent must not contain symbolic links")
    directory.mkdir(mode=0o700)
    for name in (
        "etc/parts",
        "etc/sources.parts",
        "etc/trusted.parts",
        "etc/preferences.parts",
        "etc/auth.parts",
        "state/lists/partial",
        "cache/archives/partial",
        "log",
        "prefix",
        "fontconfig/cache",
    ):
        (directory / name).mkdir(parents=True, mode=0o700)
    for name in ("etc/main", "etc/trusted.gpg", "etc/preferences", "etc/auth", "state/status"):
        (directory / name).touch(mode=0o600)
    (directory / "state/status").write_bytes(HOST_STATUS.read_bytes())
    font_configuration(directory)
    sources = directory / "etc/sources.list"
    sources.write_text(
        f"deb [arch=amd64 signed-by={KEYRING}] https://deb.debian.org/debian bookworm main\n"
        f"deb [arch=amd64 signed-by={KEYRING}] https://deb.debian.org/debian bookworm-updates main\n"
        f"deb [arch=amd64 signed-by={KEYRING}] "
        "https://deb.debian.org/debian-security bookworm-security main\n",
        encoding="utf-8",
    )
    configuration = directory / "apt.conf"
    configuration.write_text(
        f'Dir::Etc "{directory}/etc";\n'
        'Dir::Etc::parts "parts"; Dir::Etc::main "main";\n'
        'Dir::Etc::sourcelist "sources.list"; Dir::Etc::sourceparts "sources.parts";\n'
        'Dir::Etc::trusted "trusted.gpg"; Dir::Etc::trustedparts "trusted.parts";\n'
        'Dir::Etc::preferences "preferences"; Dir::Etc::preferencesparts "preferences.parts";\n'
        'Dir::Etc::netrc "auth"; Dir::Etc::netrcparts "auth.parts";\n'
        f'Dir::State "{directory}/state"; Dir::State::status "{directory}/state/status";\n'
        f'Dir::Cache "{directory}/cache"; Dir::Log "{directory}/log";\n'
        'Dir::Cache::pkgcache "pkgcache.bin"; Dir::Cache::srcpkgcache "srcpkgcache.bin";\n'
        'APT::Architecture "amd64"; APT::Architectures { "amd64"; };\n'
        'APT::Install-Recommends "false"; APT::Install-Suggests "false";\n'
        'Acquire::Languages "none"; Acquire::Retries "0";\n'
        'Acquire::AllowInsecureRepositories "false";\n'
        'Acquire::AllowDowngradeToInsecureRepositories "false";\n'
        'APT::Get::AllowUnauthenticated "false"; Acquire::Check-Valid-Until "true";\n'
        'Acquire::https::Timeout "60"; APT::Update::Error-Mode "any";\n',
        encoding="utf-8",
    )
    return configuration


def package_fields(raw: str) -> dict[str, str]:
    """Parse only the three public archive identity fields."""
    fields = {}
    for line in raw.splitlines():
        name, separator, value = line.partition(": ")
        if not separator or name in fields:
            raise ValueError("Invalid package identity fields")
        fields[name] = value
    if set(fields) != {"Package", "Version", "Architecture"}:
        raise ValueError("Incomplete package identity fields")
    if fields["Architecture"] not in {"amd64", "all"}:
        raise ValueError("An archive has an unsupported architecture")
    if re.fullmatch(r"[a-z0-9][a-z0-9+.-]{0,127}", fields["Package"]) is None:
        raise ValueError("Invalid package name")
    if re.fullmatch(r"[0-9A-Za-z.+:~_-]{1,256}", fields["Version"]) is None:
        raise ValueError("Invalid package version")
    return fields


def archive_identity(archive: Path, environment: dict[str, str]) -> dict[str, str]:
    """Record public identity and exact bytes of one authenticated archive."""
    result = subprocess.run(
        ["/usr/bin/dpkg-deb", "--field", str(archive), "Package", "Version", "Architecture"],
        env=environment,
        check=True,
        timeout=30,
        stdout=subprocess.PIPE,
        text=True,
    )
    fields = package_fields(result.stdout)
    with archive.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    return {"file": archive.name, **fields, "sha256": digest}


def downloaded_archives(directory: Path) -> list[Path]:
    """Bound the authenticated archive set before inspecting or extracting it."""
    archives = sorted((directory / "cache/archives").glob("*.deb"))
    if not archives or len(archives) > 256:
        raise ValueError("The authenticated package closure is missing or oversized")
    if sum(archive.stat().st_size for archive in archives) > 512 * 1024 * 1024:
        raise ValueError("The authenticated package closure exceeds the download bound")
    return archives


def acquire(directory: Path) -> None:
    """Authenticate metadata, download the complete closure, and extract data only."""
    require_supported_host()
    require_locked_playwright()
    configuration = private_configuration(directory)
    environment = {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "APT_CONFIG": str(configuration)}
    subprocess.run(
        ["/usr/bin/apt-get", "update"],
        env=environment,
        check=True,
        timeout=300,
    )
    subprocess.run(
        [
            "/usr/bin/apt-get",
            "--yes",
            "--download-only",
            "--reinstall",
            "--no-install-recommends",
            "install",
            *PACKAGES,
            FONT_PACKAGE,
        ],
        env=environment,
        check=True,
        timeout=300,
    )
    archives = downloaded_archives(directory)
    inventory = [archive_identity(archive, environment) for archive in archives]
    raw = json.dumps(inventory, sort_keys=True, indent=2) + "\n"
    (directory / "archive-inventory.json").write_text(raw, encoding="utf-8")
    print(raw, end="")
    if any(row["Package"].startswith(CORE_ABI_PREFIXES) for row in inventory):
        raise ValueError("A core ABI or loader archive must not replace the host runtime")
    for archive in archives:
        subprocess.run(
            ["/usr/bin/dpkg-deb", "--extract", str(archive), str(directory / "prefix")],
            env=environment,
            check=True,
            timeout=60,
        )


def main() -> None:
    """Prepare one fresh job-owned directory; never install runner packages."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    arguments = parser.parse_args()
    acquire(arguments.directory)


if __name__ == "__main__":
    main()
