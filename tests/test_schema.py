"""Схемы в schema/: валидный JSON Schema, запрет персональных полей, правила кодов СОАТО."""

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILES = ["catalog.schema.json", "meta.schema.json", "territories.schema.json"]
# Поля, которые по SPEC.md (раздел 2, п. 7) не сохраняются нигде.
PERSONAL_KEYS = {"fullname", "phone", "email", "user", "elektron_pochtasi"}


def load_schema(name: str) -> dict:
    return json.loads((ROOT / "schema" / name).read_text(encoding="utf-8"))


def declared_property_names(node) -> set[str]:
    """Все имена полей, объявленные в schema, на любой глубине."""
    found: set[str] = set()
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "properties" and isinstance(value, dict):
                found.update(value)
            found |= declared_property_names(value)
    elif isinstance(node, list):
        for item in node:
            found |= declared_property_names(item)
    return found


def territory_row(**changes) -> dict:
    row = {
        "soato": "1735",
        "level": "region",
        "parent_soato": "1700",
        "siat_id": None,
        "name_uz": None,
        "name_ru": None,
        "name_en": None,
        "name_uzc": None,
        "map_code": None,
        "status": "active",
        "first_period": None,
        "last_period": None,
    }
    row.update(changes)
    return row


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_is_valid_draft_2020_12(name):
    Draft202012Validator.check_schema(load_schema(name))


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_forbids_extra_fields_at_top_level(name):
    assert load_schema(name).get("additionalProperties") is False


@pytest.mark.parametrize("name", SCHEMA_FILES)
def test_schema_declares_no_personal_fields(name):
    assert not declared_property_names(load_schema(name)) & PERSONAL_KEYS


def test_soato_length_matches_level():
    validator = Draft202012Validator(load_schema("territories.schema.json"))

    assert validator.is_valid(territory_row())  # регион — 4 знака
    assert validator.is_valid(territory_row(soato="1700", level="country", parent_soato=None))
    assert validator.is_valid(
        territory_row(soato="1735411", level="district", parent_soato="1735", status="historic")
    )

    assert not validator.is_valid(territory_row(soato="1735411"))  # регион не бывает с 7 знаками
    assert not validator.is_valid(territory_row(level="district", parent_soato="1735"))  # район — 7 знаков
    assert not validator.is_valid(territory_row(soato="1700", level="country", parent_soato="1700"))  # у республики нет родителя
