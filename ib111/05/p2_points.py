from math import sqrt
from typing import List, Tuple

# Vraťme se k ukázkovému příkladu ‹03/points.py›, kde Vám byly
# představeny n-tice. Při takto komplikovaných typech je vhodné
# funkce otypovat, jak pro čitelnost, tak pro jednodušší hledání
# chyb. Vaším úkolem bude nyní otypovat funkce i testovací procedury
# a případně proměnné, tak, aby Vám prošla typová kontrola.
# Doporučujeme si zavést typové aliasy pro opakující se jednoznačně
# pojmenovatelné typy.


# Funkce ‹distance› spočte Euklidovskou vzdálenost dvou bodů ‹a› a ‹b›.
doubleint_str = Tuple[int, int, str]


def distance(a: doubleint_str, b: doubleint_str) -> float:
    a_x, a_y, _ = a
    b_x, b_y, _ = b
    return sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)


# Funkce ‹leftmost_colour› v neprázdném seznamu bodů najde barvu
# „nejlevějšího“ bodu (takového, který má nejmenší x-ovou souřadnici).


def leftmost_colour(points: List[doubleint_str]) -> str:
    x_min, _, result = points[0]
    for x, _, colour in points:
        if x < x_min:
            x_min = x
            result = colour

    return result


# Dále funkce ‹center_of_gravity› dostane jako parametry seznam bodů
# ‹points› a barvu ‹colour›; jejím výsledkem bude bod, který se
# nachází v «těžišti» soustavy bodů dané barvy (a který bude stejné
# barvy). Vstupní podmínkou je, že ‹points› obsahuje alespoň jeden
# bod barvy ‹colour›.


def center_of_gravity(points: List[doubleint_str], colour: str)\
        -> Tuple[float, float, str]:
    total_x = 0
    total_y = 0
    count = 0
    for p_x, p_y, p_colour in points:
        if colour == p_colour:
            total_x += p_x
            total_y += p_y
            count += 1

    return (total_x / count, total_y / count, colour)


# Jako poslední si definujeme funkci ‹average_nonmatching_distance›,
# která spočítá průměrnou vzdálenost bodů různé barvy. Vstupní
# podmínkou je, že seznam ‹points› musí obsahovat alespoň dva
# různobarevné body.


def average_nonmatching_distance(points: List[doubleint_str]) -> float:
    total: float = 0
    pairs = 0

    for i in range(len(points)):
        for j in range(i):
            _, _, i_colour = points[i]
            _, _, j_colour = points[j]
            if i_colour != j_colour:
                total += distance(points[i], points[j])
                pairs += 1

    return total / pairs


def main() -> None:
    test_distance()
    test_leftmost_color()
    test_center_of_gravity()
    test_average_nonmatching_distance()


def test_average_nonmatching_distance() -> None:
    r00 = (0, 0, "red")
    r10 = (1, 0, "red")
    b20 = (2, 0, "blue")
    b10 = (1, 0, "blue")
    g30 = (3, 0, "green")
    y20 = (2, 0, "yellow")
    w40 = (4, 0, "white")
    dist = average_nonmatching_distance

    assert dist([r00, b20]) == 2
    assert dist([b10, r00, b20]) == 1.5
    assert dist([r00, b20, b10, g30]) == 1.8
    assert dist([r00, b20, g30]) == 2
    assert dist([r00, b20, b10, r10]) == 1
    assert dist([r00, b10, g30, y20, w40]) == 2


def test_center_of_gravity() -> None:
    r00 = (0, 0, "red")
    r22 = (2, 2, "red")
    b20 = (2, 0, "blue")
    b02 = (0, 2, "blue")
    cog = center_of_gravity

    assert cog([r00], "red") == (0, 0, "red")
    assert cog([r00, r22], "red") == (1, 1, "red")
    assert cog([b20, b02], "blue") == (1, 1, "blue")
    assert cog([r00, b02, b20, r22], "red") == (1, 1, "red")
    assert cog([r00, b02, b20, r22], "blue") == (1, 1, "blue")

    g68 = (6, 8, "green")
    g00 = (0, 0, "green")
    g64 = (6, 4, "green")
    g86 = (8, 6, "green")

    assert cog([g68, g00, g64], "green") == (4, 4, "green")
    assert cog([g68, g00, g64, g86], "green") == (5, 4.5, "green")
    assert cog([r22, b20, g68, g00, g64, g86], "green") == (5, 4.5, "green")


def test_leftmost_color() -> None:
    p1 = (0, 0, "white")
    p2 = (-2, 15, "red")
    p3 = (13, -15, "yellow")
    p4 = (0, 1, "black")

    assert leftmost_colour([p1]) == "white"
    assert leftmost_colour([p3]) == "yellow"
    assert leftmost_colour([p1, p3]) == "white"
    assert leftmost_colour([p1, p3, p4, p2]) == "red"
    assert leftmost_colour([p1, p4]) == "white"
    assert leftmost_colour([p3, p4]) == "black"


def test_distance() -> None:
    p1 = (0, 0, "white")
    p2 = (1, 0, "red")

    assert distance(p1, (0, -1, "red")) == 1
    assert distance(p2, p1) == 1
    assert distance(p1, p2) == 1
    assert distance(p1, (2, 0, "black")) == 2
    assert distance(p1, (3, 4, "black")) == 5
    assert distance((-3, -4, "black"), p1) == 5


if __name__ == '__main__':
    main()  # mypy-only exercise, this should already pass
