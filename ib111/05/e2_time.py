from typing import Tuple, Optional
# Napište a otypujte funkci ‹parse_time›, která z řetězce ve
# 24-hodinovém formátu «hodiny:minuty» přečte čas do dvojice celých
# čísel ‹(hodiny, minuty)›. Není-li vstupní řetězec zadaného formátu
# nebo neobsahuje platný čas, funkce vrátí ‹None›.

def parse_time(input_string: str) -> Optional[Tuple[int, int]]:
    if input_string.count(":") != 1:
        return None
    hours, minutes = input_string.split(':')
    if not hours.isdecimal() or not minutes.isdecimal():
        return None
    if int(hours) > 23:
        return None
    if int(minutes) >= 60:
        return None
    return int(hours), int(minutes)

def main() -> None:
    assert parse_time("17:00") == (17, 0)
    assert parse_time("8:15") == (8, 15)
    assert parse_time("0:04") == (0, 4)
    assert parse_time("0:541") is None
    assert parse_time("cas") is None
    assert parse_time("10:15:00") is None
    assert parse_time("1015") is None
    assert parse_time("24:15") is None
    assert parse_time("8:60") is None
    assert parse_time("12:72") is None
    assert parse_time("24:00") is None
    assert parse_time("10::00") is None
    assert parse_time("17:OO") is None


if __name__ == "__main__":
    main()
