from typing import List


# † Implementujte co nejefektivněji čistou funkci ‹unique›, která
# vrátí seznam unikátních prvků ze vzestupně seřazeného seznamu
# ‹values›. Vstupní seznam je reprezentován třídou, která poskytuje
# pouze metody ‹get(i)› (vrátí ‹i›-tý prvek) a ‹size› (vrátí počet
# prvků). Výsledný seznam je běžný seznam typu ‹list› a bude také
# vzestupně seřazený.

def unique(values: 'CountingList') -> List[int]:
    pass


def main() -> None:
    assert unique(CountingList([1, 2, 3])) == [1, 2, 3]
    assert unique(CountingList([1, 1, 1, 1, 1, 2, 3])) == [1, 2, 3]
    assert unique(CountingList([1, 1, 1, 2, 2, 2, 2, 3, 3, 3])) \
           == [1, 2, 3]
    assert unique(CountingList([1, 2, 2, 5, 100])) == [1, 2, 5, 100]

    big_1 = CountingList([x // 1000 for x in range(50000)])
    assert unique(big_1) == list(range(50))
    assert big_1.access_count() < 25000

    big_2 = CountingList([x // 2500 for x in range(50000)])
    assert unique(big_2) == list(range(20))
    assert big_2.access_count() < 25000


class CountingList:

    def __init__(self, items: List[int]):
        self.__items = items
        self.__count = 0

    def get(self, index: int) -> int:
        self.__count += 1
        return self.__items[index]

    def size(self) -> int:
        return len(self.__items)

    def access_count(self) -> int:
        return self.__count


if __name__ == "__main__":
    main()
