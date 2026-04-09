"""Tests for PBS (Proxmox Backup Server) support."""

from __future__ import annotations

from pathlib import Path

import pytest

from proxmox_openapi import schema as schema_module
from proxmox_openapi.proxmox_codegen.apidoc_parser import (
    PBS_API_VIEWER_URL,
    PBS_APIDOC_JS_URL,
    PROXMOX_API_VIEWER_URL,
    SERVICE_URLS,
    extract_api_schema_text,
)
from proxmox_openapi.proxmox_codegen.pipeline import (
    LATEST_VERSION_TAG,
    _validate_source_for_version_tag,
)
from proxmox_openapi.schema import (
    _generated_dir,
    available_proxmox_openapi_versions,
    load_proxmox_generated_openapi,
    load_pydantic_models,
)


class TestPBSURLConstants:
    def test_pbs_viewer_url_defined(self):
        assert PBS_API_VIEWER_URL == "https://pbs.proxmox.com/docs/api-viewer/"

    def test_pbs_apidoc_js_url_defined(self):
        assert PBS_APIDOC_JS_URL == "https://pbs.proxmox.com/docs/api-viewer/apidoc.js"

    def test_service_urls_registry(self):
        assert "PVE" in SERVICE_URLS
        assert "PBS" in SERVICE_URLS
        assert SERVICE_URLS["PVE"][0] == PROXMOX_API_VIEWER_URL
        assert SERVICE_URLS["PBS"][0] == PBS_API_VIEWER_URL

    def test_service_urls_pbs_viewer_and_apidoc(self):
        viewer, apidoc = SERVICE_URLS["PBS"]
        assert viewer == PBS_API_VIEWER_URL
        assert apidoc == PBS_APIDOC_JS_URL


class TestExtractApiSchemaText:
    def test_handles_const_apischema(self):
        """PVE uses 'const apiSchema ='."""
        source = "const apiSchema = [1, 2, 3];"
        result = extract_api_schema_text(source)
        assert result == "[1, 2, 3]"

    def test_handles_var_apischema(self):
        """PBS uses 'var apiSchema ='."""
        source = "var apiSchema = [4, 5, 6];"
        result = extract_api_schema_text(source)
        assert result == "[4, 5, 6]"

    def test_prefers_const_over_var(self):
        """When both are present, const is found first."""
        source = "const apiSchema = [1, 2]; var apiSchema = [3, 4];"
        result = extract_api_schema_text(source)
        assert result == "[1, 2]"

    def test_raises_when_no_marker(self):
        source = "let something = [1, 2, 3];"
        with pytest.raises(ValueError, match="Unable to locate"):
            extract_api_schema_text(source)

    def test_nested_objects(self):
        """Bracket counting handles nested objects correctly."""
        source = 'var apiSchema = [{"path": "/access", "children": []}];'
        result = extract_api_schema_text(source)
        assert result == '[{"path": "/access", "children": []}]'


class TestGeneratedDir:
    def test_pve_returns_proxmox_subdir(self):
        result = _generated_dir(service="PVE")
        assert result.name == "proxmox"

    def test_pbs_returns_pbs_subdir(self):
        result = _generated_dir(service="PBS")
        assert result.name == "pbs"

    def test_default_is_pve(self):
        assert _generated_dir() == _generated_dir(service="PVE")

    def test_unknown_service_falls_back_to_proxmox(self):
        result = _generated_dir(service="UNKNOWN")
        assert result.name == "proxmox"

    def test_case_insensitive(self):
        assert _generated_dir(service="pbs") == _generated_dir(service="PBS")


class TestLoadProxmoxGeneratedOpenapi:
    def test_pve_loads_from_proxmox_subdir(self, tmp_path: Path, monkeypatch) -> None:
        version_dir = tmp_path / "latest"
        version_dir.mkdir(parents=True)
        openapi = '{"openapi": "3.1.0", "info": {"title": "PVE", "version": "latest"}, "paths": {}}'
        (version_dir / "openapi.json").write_text(openapi, encoding="utf-8")

        monkeypatch.setattr(schema_module, "_generated_dir", lambda service="PVE": tmp_path)
        result = load_proxmox_generated_openapi("latest", service="PVE")
        assert result is not None
        assert result["info"]["title"] == "PVE"

    def test_pbs_loads_from_pbs_subdir(self, tmp_path: Path, monkeypatch) -> None:
        version_dir = tmp_path / "latest"
        version_dir.mkdir(parents=True)
        openapi = '{"openapi": "3.1.0", "info": {"title": "PBS", "version": "latest"}, "paths": {}}'
        (version_dir / "openapi.json").write_text(openapi, encoding="utf-8")

        monkeypatch.setattr(schema_module, "_generated_dir", lambda service="PVE": tmp_path)
        result = load_proxmox_generated_openapi("latest", service="PBS")
        assert result is not None
        assert result["info"]["title"] == "PBS"

    def test_pbs_returns_none_when_missing(self, tmp_path: Path, monkeypatch) -> None:
        monkeypatch.setattr(schema_module, "_generated_dir", lambda service="PVE": tmp_path)
        result = load_proxmox_generated_openapi("latest", service="PBS")
        assert result is None


class TestAvailableVersions:
    def test_pbs_versions_separate_from_pve(self, tmp_path: Path, monkeypatch) -> None:
        pve_dir = tmp_path / "proxmox"
        pbs_dir = tmp_path / "pbs"
        (pve_dir / "v1").mkdir(parents=True)
        (pve_dir / "v1" / "openapi.json").touch()
        (pbs_dir / "v2").mkdir(parents=True)
        (pbs_dir / "v2" / "openapi.json").touch()

        def fake_generated_dir(service: str = "PVE") -> Path:
            return pbs_dir if service.upper() == "PBS" else pve_dir

        monkeypatch.setattr(schema_module, "_generated_dir", fake_generated_dir)

        pve_versions = available_proxmox_openapi_versions(service="PVE")
        pbs_versions = available_proxmox_openapi_versions(service="PBS")

        assert "v1" in pve_versions
        assert "v2" not in pve_versions
        assert "v2" in pbs_versions
        assert "v1" not in pbs_versions


class TestValidateSourceForVersionTag:
    def test_pbs_url_allowed_with_latest_tag(self):
        """PBS official URL must be allowed with 'latest' tag."""
        _validate_source_for_version_tag(
            source_url=PBS_API_VIEWER_URL,
            version_tag=LATEST_VERSION_TAG,
            service="PBS",
        )

    def test_pve_url_blocked_for_pbs_latest(self):
        """PVE URL must not be allowed as 'latest' for PBS service."""
        with pytest.raises(ValueError, match="reserved"):
            _validate_source_for_version_tag(
                source_url=PROXMOX_API_VIEWER_URL,
                version_tag=LATEST_VERSION_TAG,
                service="PBS",
            )

    def test_pve_url_allowed_for_pve_latest(self):
        """PVE URL must be allowed for PVE service with 'latest'."""
        _validate_source_for_version_tag(
            source_url=PROXMOX_API_VIEWER_URL,
            version_tag=LATEST_VERSION_TAG,
            service="PVE",
        )

    def test_custom_version_tag_allows_any_url(self):
        """A custom (non-'latest') version tag bypasses the URL restriction."""
        _validate_source_for_version_tag(
            source_url=PBS_API_VIEWER_URL,
            version_tag="v0.1",
            service="PVE",
        )
