import re
from calendar import monthrange
from datetime import date, datetime, timedelta

_ABSOLUTE_FORMATS = ("%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y")
_NAMED_DATE_RE = re.compile(r"^([a-z]+)\.?\s+(\d{1,2})(?:st|nd|rd|th)?\s*,?\s+(\d{4})$")
_NAMED_DAY_FIRST_RE = re.compile(r"^(\d{1,2})\s+([a-z]+)\.?\s+(\d{4})$")
_NEXT_WEEKDAY_RE = re.compile(r"^next\s+([a-z]+)$")
_LAST_WEEKDAY_RE = re.compile(r"^last\s+([a-z]+)$")
_BEFORE_RE = re.compile(
    r"^([a-z0-9]+)\s+(days?|weeks?|months?|years?)\s+before\s+(.+)$"
)
_AFTER_RE = re.compile(r"^([a-z0-9]+)\s+(days?|weeks?|months?|years?)\s+after\s+(.+)$")
_FROM_RE = re.compile(r"^([a-z0-9]+)\s+(days?|weeks?|months?|years?)\s+from\s+(.+)$")
_COMPOUND_OFFSET_RE = re.compile(
    r"^([a-z0-9]+)\s+(years?|months?|days?|weeks?)\s*(?:and|,)\s*([a-z0-9]+)\s+(years?|months?|days?|weeks?)\s+(before|after)\s+(.+)$"
)
_IN_OFFSET_RE = re.compile(r"^in\s+([a-z0-9]+)\s+(days?|weeks?|months?|years?)$")
_DAYS_AGO_RE = re.compile(r"^([a-z0-9]+)\s+(days?|weeks?|months?|years?)\s+ago$")
_WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}
_WEEKDAY_ABBREVIATIONS = {
    "mon": 0,
    "tue": 1,
    "wed": 2,
    "thu": 3,
    "fri": 4,
    "sat": 5,
    "sun": 6,
}
_NUMBERS = {
    "a": 1,
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
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
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
_MONTH_ABBREVIATIONS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


def parse(s: str, today: date | None = None) -> date:
    text = s.strip().lower()
    ref = today if today is not None else date.today()

    target = _resolve_relative(text, ref)
    if target is None:
        raise ValueError(f"Unrecognized date expression: {s!r}")
    return target


def _resolve_relative(text: str, ref: date) -> date | None:
    text = re.sub(r"^the\s+", "", text)
    for fmt in _ABSOLUTE_FORMATS:
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue

    named = _NAMED_DATE_RE.match(text)
    if named is not None:
        month = _MONTH_NAMES.get(named.group(1))
        if month is None:
            month = _MONTH_ABBREVIATIONS.get(named.group(1))
        if month is None:
            return None
        return date(int(named.group(3)), month, int(named.group(2)))

    named_day_first = _NAMED_DAY_FIRST_RE.match(text)
    if named_day_first is not None:
        month = _MONTH_NAMES.get(named_day_first.group(2))
        if month is None:
            month = _MONTH_ABBREVIATIONS.get(named_day_first.group(2))
        if month is None:
            return None
        return date(int(named_day_first.group(3)), month, int(named_day_first.group(1)))

    if text == "today" or text == "now":
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

    in_offset = _IN_OFFSET_RE.match(text)
    if in_offset is not None:
        token = in_offset.group(1)
        count = _parse_count(token)
        if count is None:
            return None
        unit = in_offset.group(2)
        if token == "a" and unit[-1:] == "s":
            return None
        result = ref
        if unit.startswith("week"):
            result = result + timedelta(weeks=count)
        elif unit.startswith("month"):
            result = _shift_months(result, count)
        elif unit.startswith("year"):
            result = _shift_months(result, count * 12)
        else:
            result = result + timedelta(days=count)
        return result

    ago_match = _DAYS_AGO_RE.match(text)
    if ago_match is not None:
        token = ago_match.group(1)
        count = _parse_count(token)
        if count is None:
            return None
        unit = ago_match.group(2)
        if token == "a" and unit[-1:] == "s":
            return None
        if unit.startswith("week"):
            return ref - timedelta(weeks=count)
        if unit.startswith("month"):
            return _shift_months(ref, -count)
        if unit.startswith("year"):
            return _shift_months(ref, -count * 12)
        return ref - timedelta(days=count)

    next_weekday = _NEXT_WEEKDAY_RE.match(text)
    if next_weekday is not None:
        weekday = _WEEKDAYS.get(next_weekday.group(1))
        if weekday is None:
            weekday = _WEEKDAY_ABBREVIATIONS.get(next_weekday.group(1))
        if weekday is None:
            return None
        days_ahead = (weekday - ref.weekday()) % 7
        if days_ahead == 0:
            days_ahead = 7
        return ref + timedelta(days=days_ahead)

    last_weekday = _LAST_WEEKDAY_RE.match(text)
    if last_weekday is not None:
        weekday = _WEEKDAYS.get(last_weekday.group(1))
        if weekday is None:
            weekday = _WEEKDAY_ABBREVIATIONS.get(last_weekday.group(1))
        if weekday is None:
            return None
        days_back = (ref.weekday() - weekday) % 7
        if days_back == 0:
            days_back = 7
        return ref - timedelta(days=days_back)

    before = _BEFORE_RE.match(text)
    if before is not None:
        token = before.group(1)
        count = _parse_count(token)
        if count is None:
            return None
        unit = before.group(2)
        if token == "a" and unit[-1:] == "s":
            return None
        anchor = _resolve_relative(before.group(3), ref)
        if anchor is None:
            return None
        if unit.startswith("week"):
            return anchor - timedelta(weeks=count)
        if unit.startswith("month"):
            return _shift_months(anchor, -count)
        if unit.startswith("year"):
            return _shift_months(anchor, -count * 12)
        return anchor - timedelta(days=count)

    after_match = _AFTER_RE.match(text)
    if after_match is not None:
        token = after_match.group(1)
        count = _parse_count(token)
        if count is None:
            return None
        unit = after_match.group(2)
        if token == "a" and unit[-1:] == "s":
            return None
        anchor = _resolve_relative(after_match.group(3), ref)
        if anchor is None:
            return None
        if unit.startswith("week"):
            return anchor + timedelta(weeks=count)
        if unit.startswith("month"):
            return _shift_months(anchor, count)
        if unit.startswith("year"):
            return _shift_months(anchor, count * 12)
        return anchor + timedelta(days=count)

    from_match = _FROM_RE.match(text)
    if from_match is not None:
        token = from_match.group(1)
        count = _parse_count(token)
        if count is None:
            return None
        unit = from_match.group(2)
        if token == "a" and unit[-1:] == "s":
            return None
        anchor = _resolve_relative(from_match.group(3), ref)
        if anchor is None:
            return None
        if unit.startswith("week"):
            return anchor + timedelta(weeks=count)
        if unit.startswith("month"):
            return _shift_months(anchor, count)
        if unit.startswith("year"):
            return _shift_months(anchor, count * 12)
        return anchor + timedelta(days=count)

    compound = _COMPOUND_OFFSET_RE.match(text)
    if compound is not None:
        first_count = _parse_count(compound.group(1))
        second_count = _parse_count(compound.group(3))
        unit1 = compound.group(2)
        unit2 = compound.group(4)
        direction = compound.group(5)
        anchor = _resolve_relative(compound.group(6), ref)
        if first_count is None or second_count is None or anchor is None:
            return None
        result = anchor
        for count, unit in ((first_count, unit1), (second_count, unit2)):
            if unit.startswith("week"):
                delta = timedelta(weeks=count)
                result = result - delta if direction == "before" else result + delta
            elif unit.startswith("year"):
                months = count * 12
                result = _shift_months(
                    result, -months if direction == "before" else months
                )
            elif unit.startswith("month"):
                months = count
                result = _shift_months(
                    result, -months if direction == "before" else months
                )
            elif unit.startswith("day"):
                result = (
                    result - timedelta(days=count)
                    if direction == "before"
                    else result + timedelta(days=count)
                )
        return result

    return None


def _shift_months(d: date, months: int) -> date:
    absolute = d.year * 12 + (d.month - 1) + months
    year = absolute // 12
    month = absolute % 12 + 1
    day = min(d.day, monthrange(year, month)[1])
    return date(year, month, day)


def _parse_count(token: str) -> int | None:
    if token.isdigit():
        return int(token)
    if token in _NUMBERS:
        return _NUMBERS[token]
    if "-" in token:
        parts = token.split("-")
        if len(parts) == 2 and parts[0] in _NUMBERS and parts[1] in _NUMBERS:
            return _NUMBERS[parts[0]] + _NUMBERS[parts[1]]
    return None


def main() -> None:
    print("Hello from nldate!")
