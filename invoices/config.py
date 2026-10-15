import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ROOT / "config"
FONTS_DIR = ROOT / "fonts"
COUNTER_FILE = CONFIG_DIR / "next_invoice_number.toml"
COUNTER_KEY = "next_invoice_number"


class ConfigError(Exception):
    pass


def _load(path: Path) -> dict:
    if not path.exists():
        example = path.with_suffix(".example.toml")
        hint = f" Copy {example.name} to {path.name} and edit it." if example.exists() else ""
        raise ConfigError(f"Missing config file: {path}.{hint}")
    with path.open("rb") as f:
        return tomllib.load(f)


def _require(data: dict, keys: list[str], where: Path) -> None:
    missing = [k for k in keys if not str(data.get(k, "")).strip()]
    if missing:
        raise ConfigError(f"{where} is missing: {', '.join(missing)}")


def load_settings() -> dict:
    path = CONFIG_DIR / "config.toml"
    data = _load(path)
    sender = data.get("sender", {})
    payment = data.get("payment", {})
    _require(sender, ["name", "address", "phone", "email"], path)
    _require(payment, ["details"], path)
    return {
        "sender": sender,
        "payment": payment,
        "output_dir": data.get("output_dir", "pdfs"),
        "prefix": data.get("invoice_prefix", "INV-"),
    }


def load_client(name: str) -> dict:
    path = CONFIG_DIR / "clients" / f"{name}.toml"
    data = _load(path)
    _require(data, ["name", "address"], path)
    return data


def read_next_number() -> int:
    data = _load(COUNTER_FILE)
    value = data.get(COUNTER_KEY)
    if not isinstance(value, int) or value < 1:
        raise ConfigError(f"{COUNTER_FILE} needs {COUNTER_KEY} = <positive whole number>")
    return value


def write_next_number(number: int) -> None:
    COUNTER_FILE.write_text(
        "# The number the NEXT invoice will get. Edit to move the counter back.\n"
        f"{COUNTER_KEY} = {number}\n"
    )


def safe_filename_part(text: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-") or "client"
