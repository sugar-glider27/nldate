from datetime import date

import pytest

from nldate import parse


def test_today():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 8)

    # when
    feedback = parse("today", today)

    # then
    assert feedback == target


def test_tomorrow():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 9)

    # when
    feedback = parse("tomorrow", today)

    # then
    assert feedback == target


def test_yesterday():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 7)

    # when
    feedback = parse("yesterday", today)

    # then
    assert feedback == target


def test_day_after_tomorrow():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 10)

    # when
    feedback = parse("day after tomorrow", today)

    # then
    assert feedback == target


def test_in_two_days():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 10)

    # when
    feedback = parse("in two days", today)

    # then
    assert feedback == target


def test_in_three_days():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 11)

    # when
    feedback = parse("in 3 days", today)

    # then
    assert feedback == target


def test_three_days_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 5)

    # when
    feedback = parse("3 days ago", today)

    # then
    assert feedback == target


def test_next_week():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 15)

    # when
    feedback = parse("next week", today)

    # then
    assert feedback == target


def test_last_week():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 1)

    # when
    feedback = parse("last week", today)

    # then
    assert feedback == target


def test_absolute_date():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 8)

    # when
    feedback = parse("2026-11-08", today)

    # then
    assert feedback == target


def test_unrecognized_expression_raises_value_error():
    # given
    today = date(2026, 11, 8)

    # when / then
    with pytest.raises(ValueError):
        parse("not a date", today)


def test_empty_string_raises_value_error():
    # given
    today = date(2026, 11, 8)

    # when / then
    with pytest.raises(ValueError):
        parse("", today)


def test_today_without_reference_returns_current_date():
    # when
    feedback = parse("today")

    # then
    assert feedback == date.today()


def test_next_tuesday():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 10)

    # when
    feedback = parse("next Tuesday", today)

    # then
    assert feedback == target


def test_days_before_named_date():
    # given
    today = date(2026, 11, 8)
    target = date(2025, 11, 26)

    # when
    feedback = parse("5 days before December 1st, 2025", today)

    # then
    assert feedback == target


def test_years_and_months_after_yesterday():
    # given
    today = date(2026, 11, 8)
    target = date(2028, 1, 7)

    # when
    feedback = parse("1 year and 2 months after yesterday", today)

    # then
    assert feedback == target


def test_years_and_months_after_yesterday_with_word_numbers():
    # given
    today = date(2026, 11, 8)
    target = date(2028, 1, 7)

    # when
    feedback = parse("one year and two months after yesterday", today)

    # then
    assert feedback == target


def test_two_weeks_from_tomorrow():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 23)

    # when
    feedback = parse("two weeks from tomorrow", today)

    # then
    assert feedback == target


def test_absolute_date_2025():
    # given
    today = date(2026, 11, 8)
    target = date(2025, 12, 1)

    # when
    feedback = parse("2025-12-01", today)

    # then
    assert feedback == target
