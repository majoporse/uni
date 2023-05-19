from typing import List


# † Obecný proud je datová struktura podobná seznamu, která je
# potenciálně nekonečná, ale funguje přitom i v programovacích
# jazycích se striktním vyhodnocováním. V tomto příkladu se omezíme
# na nekonečné cyklické proudy. Do třídy ‹Stream› si doplňte
# potřebné atributy. Metoda ‹get› z proudu vybere další prvek (tzn.
# odstraní první prvek a vrátí jej).

class Stream:
    def __init__(self, data: List[int]) -> None:
        pass

    def get(self) -> int:
        pass


# Čistá funkce ‹cycle› ze seznamu (který je konečný) vytvoří proud
# (který je nekonečný), a to tak, že pomyslně zřetězí nekonečně
# mnoho kopií tohoto seznamu za sebe.

def cycle(data: List[int]) -> Stream:
    pass


# Čistá funkce ‹drop› odstraní ze vstupního proudu ‹n› počátečních
# prvků a vrátí výsledný proud.

def drop(n: int, original: Stream) -> Stream:
    pass


# Čistá funkce ‹take› dostane na vstupu (nekonečný) proud a vytvoří
# z něj konečný seznam, a to tak, že vybere prvních ‹n› prvků.

def take(n: int, original: Stream) -> List[int]:
    pass


# Čistá funkce ‹every_nth› vytvoří proud, který vznikne z toho
# vstupního tak, že vždy jeden prvek zachová a pak ⟦n - 1⟧ prvků
# přeskočí. Jinými slovy, vyberete ze vstupního proudu ty prvky,
# které jsou na pozicích dělitelných ⟦n⟧.

def every_nth(n: int, original: Stream) -> Stream:
    pass


def main() -> None:
    trivial = cycle([1])
    for _ in range(10):
        assert trivial.get() == 1
    assert take(5, trivial) == [1, 1, 1, 1, 1]
    trivial_drop = drop(12, trivial)
    for _ in range(10):
        assert trivial_drop.get() == 1
    trivial_nth = every_nth(7, trivial)
    for _ in range(10):
        assert trivial_nth.get() == 1

    sequence = cycle(list(range(10)))
    for i in range(10):
        assert sequence.get() == i
    assert sequence.get() == 0
    assert sequence.get() == 1
    assert take(5, sequence) == [2, 3, 4, 5, 6]
    sequence_drop = drop(6, sequence)
    assert sequence_drop.get() == 3
    sequence_nth = every_nth(2, sequence_drop)
    for i in range(4, 10, 2):
        assert sequence_nth.get() == i

    sequence_nth = every_nth(1, sequence_nth)
    for i in range(0, 10, 2):
        assert sequence_nth.get() == i

    sequence_nth = every_nth(3, sequence_nth)
    assert sequence_nth.get() == 0
    assert sequence_nth.get() == 6
    assert sequence_nth.get() == 2
    sequence_nth = every_nth(3, sequence_nth)
    assert take(2, sequence_nth) == [8, 6]
    sequence_nth = drop(2, sequence_nth)
    assert sequence_nth.get() == 0


if __name__ == "__main__":
    main()
