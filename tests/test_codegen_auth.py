import os
from unittest.mock import patch

import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from proxmox_sdk.routes.codegen import verify_codegen_auth


def test_codegen_generate_missing_api_key_env():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": ""}):
        with pytest.raises(HTTPException) as exc_info:
            verify_codegen_auth(None)

        assert exc_info.value.status_code == 403
        assert "CODEGEN_API_KEY environment variable must be set" in exc_info.value.detail


def test_codegen_generate_missing_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        with pytest.raises(HTTPException) as exc_info:
            verify_codegen_auth(None)

        assert exc_info.value.status_code == 401
        assert "Invalid or missing API key" in exc_info.value.detail


def test_codegen_generate_invalid_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="wrong-key")

        with pytest.raises(HTTPException) as exc_info:
            verify_codegen_auth(credentials)

        assert exc_info.value.status_code == 401
        assert "Invalid or missing API key" in exc_info.value.detail


def test_codegen_generate_valid_auth_header():
    with patch.dict(os.environ, {"CODEGEN_API_KEY": "secret-key"}):
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="secret-key")

        assert verify_codegen_auth(credentials) is None
