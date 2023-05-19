from typing import Tuple


# Naprogramujte třídu ‹TimeInterval›, která bude reprezentovat
# časový interval.

class TimeInterval:
    def __init__(self, hours: int, minutes: int, seconds: int):
        self.hrs = hours
        self.min = minutes
        self.sec = seconds
        self.insec = hours * 3600 + minutes * 60 + seconds

    # Metoda zkrátí interval o čas reprezentovaný parametrem
    # ‹interval›.

    def shorten(self, interval: 'TimeInterval') -> None:
        time = self.hrs * 3600 + self.min * 60 + self.sec \
               - (interval.hrs * 3600 + interval.min * 60 + interval.sec)
        if time < 0:
            time = 0
        self.hrs = time // 3600
        time %= 3600
        self.min = time // 60
        time %= 60
        self.sec = time

    # Metoda prodlouží interval o čas reprezentovaný parametrem
    # ‹interval›.

    def extend(self, interval: 'TimeInterval') -> None:
        time = self.hrs * 3600 + self.min * 60 + self.sec \
               + (interval.hrs * 3600 + interval.min * 60 + interval.sec)
        self.hrs = time // 3600
        time %= 3600
        self.min = time // 60
        time %= 60
        self.sec = time

    # Metoda vrátí reprezentovaný interval jako n-tici ve formátu
    # (hodiny, minuty, sekundy), kde minuty a sekundy nabývají
    # hodnoty z uzavřeného intervalu [0, 59].

    def format(self) -> Tuple[int, int, int]:
        return (self.hrs, self.min, self.sec)


def main() -> None:
    for h, m, s in [(12, 3, 59), (14, 59, 59), (0, 0, 0),
                    (0, 0, 1), (0, 12, 12)]:
        assert TimeInterval(h, m, s).format() == (h, m, s)

    duration = TimeInterval(0, 0, 0)
    duration.extend(TimeInterval(0, 5, 30))
    assert duration.format() == (0, 5, 30)
    duration.extend(TimeInterval(0, 5, 30))
    assert duration.format() == (0, 11, 0)
    duration.extend(TimeInterval(0, 49, 0))
    assert duration.format() == (1, 0, 0)

    duration.shorten(TimeInterval(0, 32, 41))
    assert duration.format() == (0, 27, 19)
    duration.shorten(TimeInterval(123, 12, 43))
    assert duration.format() == (0, 0, 0)

    duration.extend(TimeInterval(1, 32, 56))
    duration.extend(duration)
    assert duration.format() == (3, 5, 52)
    duration.extend(duration)
    assert duration.format() == (6, 11, 44)
    duration.shorten(duration)
    assert duration.format() == (0, 0, 0)

    duration = TimeInterval(1, 0, 20)
    duration.shorten(TimeInterval(0, 0, 40))
    assert duration.format() == (0, 59, 40)


if __name__ == "__main__":
    main()
