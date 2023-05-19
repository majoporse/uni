# V této ukázce demonstrujeme základní použití složených datových
# typů. Srovnejte ‹05/shapes.py› – budeme nyní řešit stejné
# problémy, ale místo n-tic (kde jsou jednotlivé složky číslované
# ale jinak anonymní) budeme používat složené typy, které mají
# jednotlivé složky pojmenované.

from typing import List, Optional
from math import isclose, pi, sqrt, cos, sin


# Jako první si definujeme typ pro kruh (anglicky disc), který má
# jediný atribut, totiž poloměr typu ‹float›.

class Disc:
    def __init__(self, radius: float) -> None:
        self.radius = radius


# Dále definujeme čistou funkci ‹disc_area›, která má jediný
# parametr typu ‹Disc› a jejíž výsledkem je číslo typu ‹float›.

def disc_area(disc: Disc) -> float:
    return pi * disc.radius ** 2


# Dalším typem bude obdélník, ‹Rectangle›, který má atributy dva,
# šířku a výšku.

class Rectangle:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height


# Podobně jako u kruhu, definujeme čistou funkci pro výpočet plochy:

def rectangle_area(rect: Rectangle) -> float:
    return rect.width * rect.height


# Elipsa reprezentuje podobný případ, kdy potřebujeme k jejímu
# popisu dvě čísla, tentokrát délky jejích dvou poloos. Všimněte si,
# že na rozdíl od reprezentace v ukázce ‹05/shapes.py› (kde jsme
# používali n-tice) nám tu záměna elipsy a obdélníku v žádném
# případě nehrozí.

class Ellipse:
    def __init__(self, major: float, minor: float) -> None:
        assert major >= minor
        self.major = major
        self.minor = minor


def ellipse_area(ellipse: Ellipse) -> float:
    return pi * ellipse.major * ellipse.minor


# Atributy složeného typu samozřejmě nemusí být všechny stejného
# typu (jako tomu bylo v této ukázce dosud). Zadefinujeme si tedy
# ještě pravidelný n-úhelník, který zadáme hlavním poloměrem (tzn.
# vzdáleností vrcholu od středu) a počtem vrcholů (který je na
# rozdíl od poloměru celočíselný).

class Polygon:
    def __init__(self, radius: float, vertices: int) -> None:
        self.radius = radius
        self.vertices = vertices


def polygon_area(polygon: Polygon) -> float:
    half_angle = pi / polygon.vertices
    half_side = sin(half_angle) * polygon.radius
    minor_radius = cos(half_angle) * polygon.radius
    return polygon.vertices * minor_radius * half_side


# Dále napíšeme funkci, která ze seznamu obdélníků vybere ten
# s největší plochou, existuje-li takový právě jeden. Je zde vidět,
# že se složenými typy pracujeme velmi obdobně jako s těmi
# zabudovanými. Tím, že používáme pouze abstraktní operace (které
# jsou „schované“ do funkcí) je dokonce tělo oproti implementaci
# z ukázky ‹05/shapes.py› zcela nezměněné.

def largest_rectangle(rectangles: List[Rectangle]) \
        -> Optional[Rectangle]:

    if len(rectangles) == 0:
        return None

    largest = rectangles[0]
    count = 0

    for r in rectangles:
        if isclose(rectangle_area(r), rectangle_area(largest)):
            count += 1
        elif rectangle_area(r) > rectangle_area(largest):
            count = 1
            largest = r

    return largest if count == 1 else None


# Nyní zbývá pouze popsané funkce otestovat:

def main() -> None:  # demo
    unit_rectangle = Rectangle(1, 1)
    assert isclose(rectangle_area(unit_rectangle), 1)
    assert isclose(rectangle_area(Rectangle(2, 2)), 4)
    assert isclose(polygon_area(Polygon(sqrt(2), 4)), 4)
    assert isclose(polygon_area(Polygon(1, 6)), 2.5980762113533)
    assert isclose(ellipse_area(Ellipse(1, 1)), 3.1415926535898)
    assert isclose(ellipse_area(Ellipse(6, 2)), 37.699111843078)
    assert isclose(ellipse_area(Ellipse(12.532, 8.4444)),
                   332.4597362298)

    # Jak již bylo naznačeno, problém, který se nám objevil
    # s elipsou a obdélníkem před dvěma týdny nás už nyní nemusí
    # trápit. Odkomentujete-li následovné tvrzení, ‹mypy› Vám
    # v programu ohlásí chybu.

    pass  # assert ellipse_area(unit_rectangle) == 1

    assert largest_rectangle([]) is None
    r_11 = Rectangle(1, 1)
    r_43 = Rectangle(4, 3)
    r_55 = Rectangle(5, 5)
    r_62 = Rectangle(6, 2)
    r_c2 = Rectangle(12, 2)
    r_xy = Rectangle(10.2, 1.5)
    assert largest_rectangle([r_11, r_43, r_62]) is None
    assert largest_rectangle([r_55, r_43, r_11]) == r_55
    assert largest_rectangle([r_c2, r_xy]) == r_c2


if __name__ == '__main__':
    main()
