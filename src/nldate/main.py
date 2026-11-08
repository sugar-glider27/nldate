import re
from calendar import monthrange
from datetime import date, datetime, timedelta

_ABSOLUTE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d")
_IN_DAYS_RE = re.compile(r"^in\s+(\d+)\s+days?$")
_DAYS_AGO_RE = re.compile(r"^(\d+)\s+days?\s+ago$")


def parse(s: str, today: date | None = None) -> date:
    text = s.strip().lower()
    ref = today if today is not None else date.today()

    for fmt in _ABSOLUTE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    target = _resolve_relative(text, ref)
    if target is None:
        raise ValueError(f"Unrecognized date expression: {s!r}")
    return target


def _resolve_relative(text: str, ref: date) -> date | None:
    if text == "today":
        return ref
    if text == "tomorrow":
        return ref + timedelta(days=1)
    if text == "yesterday":
        return ref - timedelta(days=1)
    if text == "day after tomorrow":
        return ref + timedelta(days=2)
    if text == "next week":
        return ref + timedelta(weeks=1)
    if text == "last week":
        return ref - timedelta(weeks=1)
    if text == "next month":
        return _shift_months(ref, 1)
    if text == "last month":
        return _shift_months(ref, -1)

    in_days = _IN_DAYS_RE.match(text)
    if in_days is not None:
        return ref + timedelta(days=int(in_days.group(1)))

    days_ago = _DAYS_AGO_RE.match(text)
    if days_ago is not None:
        return ref - timedelta(days=int(days_ago.group(1)))

    return None


def _shift_months(d: date, months: int) -> date:
    total = (d.month - 1) + months
    year = d.year + total // 12
    month = total % 12 + 1
    day = min(d.day, monthrange(year, month)[1])
    return date(year, month, day)


def main() -> None:
    print("Hello from nldate!")
