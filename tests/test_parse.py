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


def test_in_2_weeks():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 22)

    # when
    feedback = parse("in 2 weeks", today)

    # then
    assert feedback == target


def test_in_one_week():
    # given
    today = date(2026, 12, 28)
    target = date(2027, 1, 4)

    # when
    feedback = parse("in one week", today)

    # then
    assert feedback == target


def test_in_3_months():
    # given
    today = date(2026, 11, 8)
    target = date(2027, 2, 8)

    # when
    feedback = parse("in 3 months", today)

    # then
    assert feedback == target


def test_in_4_years():
    # given
    today = date(2026, 11, 8)
    target = date(2030, 11, 8)

    # when
    feedback = parse("in 4 years", today)

    # then
    assert feedback == target


def test_in_one_month():
    # given
    today = date(2024, 1, 31)
    target = date(2024, 2, 29)

    # when
    feedback = parse("in one month", today)

    # then
    assert feedback == target


def test_in_one_year():
    # given
    today = date(2024, 2, 29)
    target = date(2025, 2, 28)

    # when
    feedback = parse("in one year", today)

    # then
    assert feedback == target


def test_one_week_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 1)

    # when
    feedback = parse("1 week ago", today)

    # then
    assert feedback == target


def test_two_weeks_ago():
    # given
    today = date(2026, 1, 5)
    target = date(2025, 12, 22)

    # when
    feedback = parse("two weeks ago", today)

    # then
    assert feedback == target


def test_one_month_ago():
    # given
    today = date(2024, 3, 31)
    target = date(2024, 2, 29)

    # when
    feedback = parse("1 month ago", today)

    # then
    assert feedback == target


def test_three_months_ago():
    # given
    today = date(2026, 5, 31)
    target = date(2026, 2, 28)

    # when
    feedback = parse("3 months ago", today)

    # then
    assert feedback == target


def test_one_year_ago():
    # given
    today = date(2024, 2, 29)
    target = date(2023, 2, 28)

    # when
    feedback = parse("one year ago", today)

    # then
    assert feedback == target


def test_four_years_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2022, 11, 8)

    # when
    feedback = parse("4 years ago", today)

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


def test_dec_1_2025():
    # given
    today = date(2026, 11, 8)
    target = date(2025, 12, 1)

    # when
    feedback = parse("Dec 1, 2025", today)

    # then
    assert feedback == target


def test_feb_29_2024():
    # given
    today = date(2026, 11, 8)
    target = date(2024, 2, 29)

    # when
    feedback = parse("Feb 29, 2024", today)

    # then
    assert feedback == target


def test_feb_29_2025_raises_value_error():
    # given
    today = date(2026, 11, 8)

    # when / then
    with pytest.raises(ValueError):
        parse("Feb 29, 2025", today)


def test_five_days_before_dec_1_2025():
    # given
    today = date(2026, 11, 8)
    target = date(2025, 11, 26)

    # when
    feedback = parse("5 days before Dec 1st, 2025", today)

    # then
    assert feedback == target


def test_dec_1_2025_with_period():
    # given
    today = date(2026, 11, 8)
    target = date(2025, 12, 1)

    # when
    feedback = parse("Dec. 1, 2025", today)

    # then
    assert feedback == target


def test_five_days_before_feb_29_2024():
    # given
    today = date(2026, 11, 8)
    target = date(2024, 2, 24)

    # when
    feedback = parse("5 days before Feb. 29, 2024", today)

    # then
    assert feedback == target


def test_feb_29_2025_with_period_raises_value_error():
    # given
    today = date(2026, 11, 8)

    # when / then
    with pytest.raises(ValueError):
        parse("Feb. 29, 2025", today)


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


def test_one_week_ago_from_feb_29():
    # given
    today = date(2024, 2, 29)
    target = date(2024, 2, 22)

    # when
    feedback = parse("1 week ago", today)

    # then
    assert feedback == target


def test_three_weeks_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 10, 18)

    # when
    feedback = parse("3 weeks ago", today)

    # then
    assert feedback == target


def test_two_months_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 9, 8)

    # when
    feedback = parse("2 months ago", today)

    # then
    assert feedback == target


def test_one_month_ago_from_may_31st():
    # given
    today = date(2026, 5, 31)
    target = date(2026, 4, 30)

    # when
    feedback = parse("1 month ago", today)

    # then
    assert feedback == target


def test_five_years_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2021, 11, 8)

    # when
    feedback = parse("5 years ago", today)

    # then
    assert feedback == target


def test_a_week_ago():
    # given
    today = date(2026, 11, 8)
    target = date(2026, 11, 1)

    # when
    feedback = parse("a week ago", today)

    # then
    assert feedback == target


def test_in_a_year():
    # given
    today = date(2026, 11, 8)
    target = date(2027, 11, 8)

    # when
    feedback = parse("in a year", today)

    # then
    assert feedback == target


def test_a_weeks_ago_raises_value_error():
    # given
    today = date(2026, 11, 8)

    # when / then
    with pytest.raises(ValueError):
        parse("a weeks ago", today)


def test_a_month_ago():
    # given
    today = date(2024, 3, 31)
    target = date(2024, 2, 29)

    # when
    feedback = parse("a month ago", today)

    # then
    assert feedback == target
