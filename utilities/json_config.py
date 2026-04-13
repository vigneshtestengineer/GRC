"""
JSON configuration loader helpers.
"""
import json
from functools import lru_cache
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_FILE = BASE_DIR / "config" / "Executive_Login.json"


@lru_cache(maxsize=1)
def _load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _get_value(section, key, default=None):
    section_data = _load_config().get(section, {})
    if not isinstance(section_data, dict):
        return default
    return section_data.get(key, default)


def get_str(section, key, default=""):
    value = _get_value(section, key, default)
    if value is None:
        return default
    return str(value)


def get_bool(section, key, default=False):
    value = _get_value(section, key, default)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("1", "true", "yes", "y", "on")
    if isinstance(value, (int, float)):
        return bool(value)
    return default


def get_int(section, key, default):
    value = _get_value(section, key, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def get_path(section, key, default):
    raw_path = _get_value(section, key, default)
    candidate = Path(raw_path) if raw_path else Path(default)
    if not candidate.is_absolute():
        candidate = BASE_DIR / candidate
    return str(candidate.resolve())
