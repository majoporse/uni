from typing import List, Optional, Union, Tuple


# † V tomto příkladě pokračujeme proudy. Tentokrát budou proudy
# obecné: mohou být jak konečné tak nekonečné, a nemusí být
# cyklické. Protože v obecném případě nelze proud uložit celý,
# musíme datovou strukturu naprogramovat tak, aby potřebný výpočet
# proběhl až ve chvíli, kdy se pokusíme z proudu vybrat další prvek.
#
# To zabezpečíme tak, že každá transformace proudu bude samostatná
# třída, která si bude pamatovat odkaz na vnitřní proud (t.j. ten,
# který transformuje) a podle potřeby z něj bude vybírat prvky.
#
# Protože všechny tyto třídy mají metodu ‹take_head›, obecný proud
# lze reprezentovat jako instanci libovolné z těchto tříd.

Stream = Union['FinStream', 'Cycle', 'Drop', 'Take', 'Skip']


# Třída ‹FinStream› bude reprezentovat konečný proud, který vznikl
# ze seznamu konverzní funkcí ‹to_stream›. Ostatní třídy
# reprezentují transformace popsané níže u příslušných funkcí.

class FinStream:
    def __init__(self, data: List[int]) -> None:
        pass

    # Metoda ‹take_head› vrátí dvojici, kde první složka je první
    # prvek proudu (existuje-li) a druhá složka reprezentuje proud,
    # který vznikne odstraněním prvního prvku.

    def take_head(self) -> Tuple[Optional[int], Stream]:
        pass


class Cycle:
    def __init__(self, inner: Stream) -> None:
        pass

    def take_head(self) -> Tuple[Optional[int], Stream]:
        pass


class Drop:
    def __init__(self, n: int, inner: Stream) -> None:
        pass

    def take_head(self) -> Tuple[Optional[int], Stream]:
        pass


class Take:
    def __init__(self, n: int, inner: Stream) -> None:
        pass

    def take_head(self) -> Tuple[Optional[int], Stream]:
        pass


class Skip:
    def __init__(self, inner: Stream) -> None:
        pass

    def take_head(self) -> Tuple[Optional[int], Stream]:
        pass


# Čistá funkce, která vytvoří konečný proud z dat zadaných v seznamu.

def to_stream(data: List[int]) -> Stream:
    pass


# Čistá funkce, která vytvoří nekonečný proud, a to tak, že bude
# vybírat prvky z vnitřního proudu, dokud to lze. V případě, že
# prvky dojdou (vstupní proud byl konečný), výstupní proud se vrátí
# na začátek toho vstupního a toto bude dále opakovat (libovolně
# dlouho).

def cycle(inner: Stream) -> Stream:
    pass


# Čistá funkce, která vytvoří nový proud tím, že zahodí prvních ‹n›
# prvků toho vstupního.

def drop(n: int, original: Stream) -> Stream:
    pass


# Čistá funkce, která z libovolně dlouhého vstupního proudu vytvoří
# konečný proud o nejvýše ‹n› prvcích.

def take(n: int, original: Stream) -> Stream:
    pass


# Čistá funkce, která vytvoří proud, který se bude chovat
# následovně: první prvek vybere z proudu ‹data›, pak dalších ‹n›
# prvků přeskočí, kde ‹n› je hodnota vybraná z proudu ‹skips›. Toto
# bude opakovat, dokud budou v ‹data› nějaké prvky. Dojdou-li
# v ‹skips› hodnoty, výsledný proud nebude dále nic přeskakovat.

def skip(data: Stream, skips: Stream) -> Stream:
    pass


def main() -> None:
    stream: Stream = to_stream(list(range(10)))
    for i in range(10):
        stream = check_head(stream, i)
    stream = check_head(stream, None)
    stream = check_head(stream, None)

    stream = cycle(to_stream(list(range(15))))
    for _ in range(4):
        for i in range(15):
            stream = check_head(stream, i)

    stream = drop(3, to_stream(list(range(10))))
    stream = check_head(stream, 3)
    stream = check_head(stream, 4)
    stream = drop(0, stream)
    stream = check_head(stream, 5)
    stream = drop(8, stream)
    stream = check_head(stream, None)

    stream = drop(3, cycle(to_stream(list(range(15)))))
    stream_2 = check_head(stream, 3)
    stream = check_head(stream, 3)
    stream = check_head(stream, 4)
    stream = drop(0, stream)
    stream = check_head(stream, 5)
    stream = drop(8, stream)
    stream = check_head(stream, 14)
    stream = drop(11, stream)
    stream = check_head(stream, 11)
    stream = drop(3, stream)

    for _ in range(4):
        for i in range(15):
            stream = check_head(stream, i)

    stream = to_stream(list(range(10)))
    stream = take(8, stream)
    for i in range(6):
        stream = check_head(stream, i)

    stream = take(8, stream)
    stream = check_head(stream, 6)
    stream = check_head(stream, 7)
    stream = check_head(stream, None)

    stream = cycle(to_stream(list(range(15))))
    stream_2 = take(20, stream)

    for i in range(15):
        stream = check_head(stream, i)
        stream_2 = check_head(stream_2, i)
    for i in range(5):
        stream = check_head(stream, i)
        stream_2 = check_head(stream_2, i)
    for i in range(5, 10):
        stream = check_head(stream, i)
        stream_2 = check_head(stream_2, None)

    stream = to_stream(list(range(10)))
    stream = skip(cycle(stream), stream)

    for i in [0, 1, 3, 6, 0, 5, 1, 8, 6, 5, 5, 6, 7, 8]:
        stream = check_head(stream, i)


def check_head(stream: Stream, value: Optional[int]) -> Stream:
    head, tail = stream.take_head()
    assert head == value, (head, value)
    return tail


if __name__ == "__main__":
    main()
