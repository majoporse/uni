# Napište funkci, která spočítá počet pátků 13. v daném roce ‹year›.
# Parametr ‹day_of_week› udává den v týdnu, na který v daném roce
# padne 1. leden. Dny v týdnu mají hodnoty 0–6, počínaje pondělím
# s hodnotou 0.

def fridays(year, day_of_week):
    pass


def main():
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
    main()
