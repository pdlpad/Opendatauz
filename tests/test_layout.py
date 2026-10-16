"""Каркас репозитория по разделу 3 SPEC.md (этап 0)."""

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "SOURCES.md",
    "DATA_LICENSE.md",
    "LICENSE",
    "CLAUDE.md",
    "SPEC.md",
    ".gitignore",
    "pyproject.toml",
    "requirements-dev.txt",
    "schema/catalog.schema.json",
    "schema/meta.schema.json",
    "schema/territories.schema.json",
    ".github/workflows/ci.yml",
    "site/package.json",
    "site/index.html",
    "site/vite.config.ts",
    "site/tsconfig.json",
    "site/src/main.tsx",
    "site/src/App.tsx",
]

REQUIRED_DIRS = [
    "data/classifiers/other",
    "data/indicators",
    "data/geo",
    "data/sync_log",
    "tools",
    "schema",
    "site",
    "tests",
]


@pytest.mark.parametrize("path", REQUIRED_FILES)
def test_required_file_exists(path):
    assert (ROOT / path).is_file(), path


@pytest.mark.parametrize("path", REQUIRED_DIRS)
def test_required_dir_exists(path):
    assert (ROOT / path).is_dir(), path


def test_licenses_are_declared():
    assert "CC BY 4.0" in (ROOT / "DATA_LICENSE.md").read_text(encoding="utf-8")
    assert "MIT License" in (ROOT / "LICENSE").read_text(encoding="utf-8")


def test_site_footer_names_the_source():
    app = (ROOT / "site" / "src" / "App.tsx").read_text(encoding="utf-8")
    assert "Неофициальное зеркало" in app
    assert "Национальный комитет по статистике" in app
