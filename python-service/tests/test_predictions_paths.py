import os
from unittest.mock import patch

import pytest

from routers import predictions


def test_resolve_model_file_prefers_models_directory(tmp_path):
    models_dir = tmp_path / "models"
    models_dir.mkdir()
    canonical = models_dir / "price_model.pkl"
    canonical.write_bytes(b"ok")
    legacy = tmp_path / "price_model.pkl"
    legacy.write_bytes(b"legacy")

    with patch.object(predictions, "MODELS_DIR", str(models_dir)), patch.object(
        predictions, "SERVICE_ROOT", str(tmp_path)
    ):
        assert predictions._resolve_model_file("price_model.pkl") == str(canonical)


def test_resolve_model_file_falls_back_to_legacy_root(tmp_path):
    legacy = tmp_path / "price_model.pkl"
    legacy.write_bytes(b"legacy")

    with patch.object(predictions, "MODELS_DIR", str(tmp_path / "models")), patch.object(
        predictions, "SERVICE_ROOT", str(tmp_path)
    ), pytest.warns(DeprecationWarning, match="legacy path"):
        resolved = predictions._resolve_model_file("price_model.pkl")

    assert resolved == str(legacy)


def test_resolve_model_file_returns_none_when_missing(tmp_path):
    with patch.object(predictions, "MODELS_DIR", str(tmp_path / "models")), patch.object(
        predictions, "SERVICE_ROOT", str(tmp_path)
    ):
        assert predictions._resolve_model_file("price_model.pkl") is None
