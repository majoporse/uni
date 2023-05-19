from math import gcd
from typing import Tuple

# Opět netradiční úloha: tentokrát budete doplňovat vstupní
# podmínky, opět k funkcím, které jsou zapsané bez jakýchkoliv
# užitečných názvů nebo komentářů. Vstupní podmínky doplňujte do
# samostatných funkcí (predikátů) k tomuto účelu nachystaných.
# Vstupní podmínka musí zaručit, že funkce skončí a splní výstupní
# podmínku. Zároveň by měla co nejméně omezit použitelnost funkce
# (tzn. měla by povolit co nejvíce vstupů).


def f_1(x_0: int, y: int) -> int:
    assert precondition_1(x_0, y)
    x = x_0
    z = 0
    s = -1 if (x < 0) != (y < 0) else 1
    while abs(x) > 0:
        x -= s * y
        z += s
    assert x_0 // y == z
    return z


def precondition_1(x_0, y):
    return False


def f_2(x_0: int, y_0: int) -> int:
    assert precondition_2(x_0, y_0)
    x = x_0
    y = y_0
    z = 0
    while x != y:
        x += 1
        y -= 1
        z += 2
    assert x_0 + z == y_0
    return z


def precondition_2(x_0, y_0):
    return x_0 <= y_0 and False


def f_3(x: int, y: int) -> int:
    assert precondition_3(x, y)
    i = 2
    j = 1
    while i <= min(x, -y):
        if x % i == 0 and y % i == 0:
            j = i
        i += 1
    assert j == gcd(x, y)
    return j


def precondition_3(x, y):
    return True


def f_4(x_0: int, y: int) -> Tuple[int, int]:
    assert precondition_4(x_0, y)
    x = x_0
    z = 0
    while x >= y:
        x -= y
        z += 1
    assert z * y + x == x_0
    assert z >= 0 and x >= 0
    return (z, x)


def precondition_4(x_0, y):
    return False


def main():
    check(f_1, precondition_1)
    check(f_2, precondition_2)
    check(f_3, precondition_3)
    check(f_4, precondition_4)


def check(f, precondition):
    passes = 0
    for x in range(-10, 11):
        for y in range(-10, 11):
            if precondition(x, y):
                f(x, y)
                passes += 1
    assert passes >= 100


if __name__ == '__main__':
    main()
