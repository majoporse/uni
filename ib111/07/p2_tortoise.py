from typing import Tuple
from math import sin, cos, radians

# V této úloze budete programovat třídu ‹Tortoise›, která se chová
# podobně jako želva, kterou jsme používali v kapitole B. Rozdílem
# bude, že naše želva nebude kreslit na obrazovku, ale pouze počítat
# své aktuální souřadnice. Souřadnice želvy jsou po každém kroku
# celočíselné, ale výpočty provádějte na hodnotách typu ‹float›,
# které po každém kroku zaokrouhlíte zabudovanou funkcí ‹round›.

# Všechny kreslící metody želvy budou vracet odkaz na vlastní
# instanci, aby bylo lze volání pohodlně řetězit (viz použití
# v testech).

Point = Tuple[int, int]


class Tortoise:

    # Želva je po vytvoření otočena v kladném směru osy ⟦y⟧ t.j. „na
    # sever“ a nachází se v bodě ‹initial_point›.

    def __init__(self, initial_point: Point):
        self.angle = 90
        self.get_x = initial_point[0]
        self.get_y = initial_point[1]

    # Metoda ‹forward› posune želvu vpřed o vzdálenost ‹distance›.

    def forward(self, distance: int) -> 'Tortoise':
        angle = self.angle
        self.get_x += round(distance * cos(radians(angle)))
        self.get_y += round(distance * sin(radians(angle)))
        return self

    # Metoda ‹backward› ji posune naopak vzad, opět o vzdálenost
    # ‹distance›.

    def backward(self, distance: int) -> 'Tortoise':
        angle = self.angle
        self.get_x -= round(distance * cos(radians(angle)))
        self.get_y -= round(distance * sin(radians(angle)))
        return self

    # Metody ‹left› a ‹right› želvu otočí o počet stupňů daný
    # parametrem ‹angle›. Metoda ‹left› proti, a metoda ‹right› po
    # směru hodinových ručiček.

    def left(self, angle: int) -> 'Tortoise':
        self.angle += angle
        return self

    def right(self, angle: int) -> 'Tortoise':
        self.angle -= angle
        return self

    # Konečně (čistá) metoda ‹position› vrátí aktuální pozici želvy.

    def position(self) -> Point:
        return (self.get_x, self.get_y)


def main() -> None:
    turtle = Tortoise((0, 0))
    turtle.forward(5)
    assert turtle.position() == (0, 5)
    turtle.right(90).forward(5)
    assert turtle.position() == (5, 5)
    assert turtle.right(90).forward(3).position() == (5, 2)
    assert turtle.right(90).forward(5).position() == (0, 2)
    assert turtle.right(90).backward(2).position() == (0, 0)
    assert turtle.position() == (0, 0)

    turtle.forward(10).left(180).forward(15)
    assert turtle.position() == (0, -5)
    turtle.left(45).forward(2)
    assert turtle.position() == (1, -6)
    turtle.left(15).forward(4)
    assert turtle.position() == (4, -8)


if __name__ == "__main__":
    main()
