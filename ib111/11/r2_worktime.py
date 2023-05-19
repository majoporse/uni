from datetime import date, datetime, timedelta, time
from typing import List, Tuple


# † V tomto příkladu bude vaší úlohou vytvořit seznam volných
# termínů v pracovním kalendáři, například pro domluvení schůzky.
# Implementujte čistou funkci ‹free_slots›, která spočte volné
# časové intervaly v pracovní době pro den ‹day›. Parametrem je
# kalendář ‹calendar›: seznam již zabraných časových intervalů.
#
# Vaším úkolem bude spočítat doplněk již rezervovaných časů který
# spadá do pracovní doby, kterou budeme uvazovat jako všední
# pracovní dny od 8:00 do 17:00. O víkendu žádný volný pracovní čas
# není. Pro jednoduchost v této úloze nemusíte řešit státní svátky.
#
# Příklad: pokud je v kalendáři pro pracovní den rezervovaný čas
# 11:00–13:30 a 16:15–19:00, tak volný pracovní čas bude: 8:00–11:00
# a 13:30–16:15.

Slot = Tuple[datetime, datetime]
Calendar = List[Slot]


def free_slots(calendar: Calendar, day: date) -> List[Slot]:
    pass


def main() -> None:
    day = date(2020, 8, 27)
    slot = day_slot(day, time(11, 15), time(16, 15))
    assert free_slots([slot], day) == \
        [day_slot(day, time(8, 0), time(11, 15)),
         day_slot(day, time(16, 15), time(17, 0))]

    slot = day_slot(day, time(6, 0), time(10, 20))
    assert free_slots([slot], day) == \
        [day_slot(day, time(10, 20), time(17, 0))]

    slot = day_slot(day, time(6, 0), time(18, 20))
    assert free_slots([slot], day) == []

    slot = day_slot(day, time(13, 0), time(18, 20))
    assert free_slots([slot], day) == \
        [day_slot(day, time(8, 0), time(13, 0))]

    assert free_slots([], day) == \
        [day_slot(day, time(8, 0), time(17, 0))]

    assert free_slots([(datetime(2020, 8, 26, 15, 0),
                        datetime(2020, 8, 29, 10, 0))], day) == []
    assert free_slots([(datetime(2020, 8, 27, 15, 0),
                        datetime(2020, 8, 29, 10, 0))], day) == \
        [(datetime(2020, 8, 27, 8, 0), datetime(2020, 8, 27, 15, 0))]

    cal1 = testcase(datetime(2020, 11, 1),
                    datetime(2020, 11, 7),
                    timedelta(hours=2, minutes=30))

    copy = cal1[:]

    assert free_slots(copy, date(2020, 11, 2)) == \
        [(datetime(2020, 11, 2, 8, 30), datetime(2020, 11, 2, 11, 0)),
         (datetime(2020, 11, 2, 13, 30), datetime(2020, 11, 2, 16, 0))]
    assert copy == cal1

    assert free_slots(copy, date(2020, 11, 21)) == []
    assert copy == cal1

    assert free_slots(copy, date(2020, 11, 20)) == \
        [(datetime(2020, 11, 20, 8, 0), datetime(2020, 11, 20, 17, 0))]
    assert copy == cal1

    assert free_slots(copy, date(2020, 11, 1)) == []
    assert copy == cal1

    cal2 = testcase(datetime(2020, 11, 1, 1),
                    datetime(2020, 11, 7),
                    timedelta(hours=2))

    assert free_slots(cal2, date(2020, 11, 4)) == \
        [(datetime(2020, 11, 4, 8, 0), datetime(2020, 11, 4, 9, 0)),
         (datetime(2020, 11, 4, 11, 0), datetime(2020, 11, 4, 13, 0)),
         (datetime(2020, 11, 4, 15, 0), datetime(2020, 11, 4, 17, 0))]


def day_slot(day: date, start: time, end: time) -> Slot:
    return (datetime.combine(day, start), datetime.combine(day, end))


def testcase(start: datetime, end: datetime, delta: timedelta) -> Calendar:
    calendar = []
    while start < end:
        calendar.append((start, start + delta))
        start += 2 * delta
    return calendar


if __name__ == "__main__":
    main()
