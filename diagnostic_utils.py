"""Utilities for working with diagnostic templates and schema."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft7Validator


def load_json(path: str | Path) -> Any:
    """Load JSON from a file path."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_sample(sample_path: str | Path, schema_path: str | Path) -> bool:
    """Validate a diagnostic sample against the schema."""
    schema = load_json(schema_path)
    sample = load_json(sample_path)
    Draft7Validator(schema).validate(sample)
    return True
