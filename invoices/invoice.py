import sys
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path

from . import config, pdf
from .money import parse_amount, parse_date


@dataclass
class Item:
    date: date
    description: str
    amount: Decimal


class Invoice:
    def __init__(self, client, *, date=None, number=None, notes=None):
        settings = config.load_settings()
        self.client = config.load_client(client)
        self.sender = settings["sender"]
        self.payment = settings["payment"]
        self._output_dir = settings["output_dir"]
        self._prefix = settings["prefix"]
        self.date = parse_date(date) if date else _today()
        self._explicit_number = number
        self.notes = notes
        self.items: list[Item] = []

    def add_item(self, date, description, amount) -> None:
        self.items.append(Item(parse_date(date), description, parse_amount(amount)))

    @property
    def total(self) -> Decimal:
        return sum((i.amount for i in self.items), Decimal("0.00"))

    @property
    def number(self) -> str:
        if self._explicit_number is not None:
            return str(self._explicit_number)
        return f"{self._prefix}{config.read_next_number():04d}"

    def save(self, output_dir=None) -> Path:
        if not self.items:
            raise ValueError("Add at least one item before saving")
        out = Path(output_dir or self._output_dir).expanduser()
        if not out.is_absolute():
            out = config.ROOT / out
        out.mkdir(parents=True, exist_ok=True)

        number = self.number
        name = f"{number}_{config.safe_filename_part(self.client['name'])}_{self.date.isoformat()}.pdf"
        path = out / name
        if path.exists() and not _confirm_overwrite(path):
            raise FileExistsError(f"Not overwriting {path}")

        pdf.render(self, path)
        if self._explicit_number is None:
            config.write_next_number(config.read_next_number() + 1)
        return path


def _today() -> date:
    return date.today()


def _confirm_overwrite(path: Path) -> bool:
    if not sys.stdin.isatty():
        return False
    return input(f"{path.name} already exists. Overwrite? [y/N] ").strip().lower() == "y"
