import re
from calendar import monthrange
from datetime import date, datetime, timedelta

_ABSOLUTE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d")
_NAMED_DATE_RE = re.compile(r"^([a-z]+)\s+(\d{1,2})(?:st|nd|rd|th)?\s*,?\s+(\d{4})$")
_NEXT_WEEKDAY_RE = re.compile(r"^next\s+([a-z]+)$")
_BEFORE_DAYS_RE = re.compile(r"^([a-z0-9]+)\s+days?\s+before\s+(.+)$")
_WEEKS_FROM_RE = re.compile(r"^([a-z0-9]+)\s+weeks?\s+from\s+(.+)$")
_YEARS_MONTHS_RE = re.compile(
    r"^([a-z0-9]+)\s+years?\s+and\s+([a-z0-9]+)\s+months?\s+after\s+(.+)$"
)
_IN_DAYS_RE = re.compile(r"^in\s+([a-z0-9]+)\s+days?$")
_DAYS_AGO_RE = re.compile(r"^([a-z0-9]+)\s+days?\s+ago$")
_WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
_NUMBERS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
}
_MONTH_NAMES = {
    "january": 1,
    "february": 2,
    "march": 3,
    "april": 4,
    "may": 5,
    "june": 6,
    "july": 7,
    "august": 8,
    "september": 9,
    "october": 10,
    "november": 11,
    "december": 12,
}


def parse(s: str, today: date | None = None) -> date:
    text = s.strip().lower()
    ref = today if today is not None else date.today()

    target = _resolve_relative(text, ref)
    if target is None:
        raise ValueError(f"Unrecognized date expression: {s!r}")
    return target


def _resolve_relative(text: str, ref: date) -> date | None:
    for fmt in _ABSOLUTE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    named = _NAMED_DATE_RE.match(text)
    if named is not None:
        month = _MONTH_NAMES.get(named.group(1))
        if month is None:
            return None
        return date(int(named.group(3)), month, int(named.group(2)))

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
        count = _parse_count(in_days.group(1))
        if count is None:
            return None
        return ref + timedelta(days=count)

    days_ago = _DAYS_AGO_RE.match(text)
    if days_ago is not None:
        count = _parse_count(days_ago.group(1))
        if count is None:
            return None
        return ref - timedelta(days=count)

    next_weekday = _NEXT_WEEKDAY_RE.match(text)
    if next_weekday is not None:
        weekday = _WEEKDAYS.get(next_weekday.group(1))
        if weekday is None:
            return None
        days_ahead = (weekday - ref.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return ref + timedelta(days=days_ahead)

    before = _BEFORE_DAYS_RE.match(text)
    if before is not None:
        count = _parse_count(before.group(1))
        anchor = _resolve_relative(before.group(2), ref)
        if count is None or anchor is None:
            return None
        return anchor - timedelta(days=count)

    weeks_from = _WEEKS_FROM_RE.match(text)
    if weeks_from is not None:
        count = _parse_count(weeks_from.group(1))
        anchor = _resolve_relative(weeks_from.group(2), ref)
        if count is None or anchor is None:
            return None
        return anchor + timedelta(weeks=count)

    years_months = _YEARS_MONTHS_RE.match(text)
    if years_months is not None:
        anchor = _resolve_relative(years_months.group(3), ref)
        if anchor is None:
            return None
        years = _parse_count(years_months.group(1))
        months = _parse_count(years_months.group(2))
        if years is None or months is None:
            return None
        return _shift_months(anchor, years * 12 + months)

    return None


def _shift_months(d: date, months: int) -> date:
    total = (d.month - 1) + months
    year = d.year + total // 12
    month = total % 12 + 1
    day = min(d.day, monthrange(year, month)[1])
    return date(year, month, day)


def _parse_count(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    return _NUMBERS.get(token)


def main() -> None:
    print("Hello from nldate!")
