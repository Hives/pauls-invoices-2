from datetime import date
from decimal import Decimal, InvalidOperation


def parse_amount(value) -> Decimal:
    if isinstance(value, float):
        raise TypeError("Use a string, int or Decimal for amounts, not float")
    try:
        amount = Decimal(str(value).replace(",", "").lstrip("£"))
    except InvalidOperation:
        raise ValueError(f"Invalid amount: {value!r}") from None
    if not amount.is_finite():
        raise ValueError(f"Invalid amount: {value!r}")
    return amount.quantize(Decimal("0.01"))


def parse_date(value) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


def fmt_money(amount: Decimal) -> str:
    sign = "-" if amount < 0 else ""
    return f"{sign}£{abs(amount):,.2f}"


def fmt_date(d: date) -> str:
    return f"{d.day} {d:%b %Y}"
