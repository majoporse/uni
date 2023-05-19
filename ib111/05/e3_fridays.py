# Otypujte následující implementaci příkladu ‹02/fridays.py›.

def is_leap(year:int) -> bool:
    if year % 400 == 0:
        return True
    if year % 4 == 0 and year % 100 != 0:
        return True
    return False


def days_per_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if is_leap(year) else 28
    if month == 4 or month == 6 or month == 9 or month == 11:
        return 30
    return 31


def is_friday(day_of_week: int) -> int:
    return day_of_week == 4


def fridays(year: int, day_of_week: int) -> int:
    count = 0
    for month in range(1, 13):
        days = days_per_month(year, month)
        for day in range(1, days + 1):
            if is_friday(day_of_week) and day == 13:
                count += 1
            day_of_week = (day_of_week + 1) % 7
    return count


def main() -> None:
    assert fridays(2020, 2) == 2
    assert fridays(2019, 1) == 2
    assert fridays(2018, 0) == 2
    assert fridays(2017, 6) == 2
    assert fridays(2016, 4) == 1
    assert fridays(2015, 3) == 3
    assert fridays(2012, 6) == 3
    assert fridays(2000, 5) == 1
    assert fridays(1996, 0) == 2
    assert fridays(1643, 3) == 3
    assert fridays(1501, 1) == 2


if __name__ == "__main__":
    main()  # mypy-only exercise, this should already pass
