# V této úloze budete implementovat jednoduchý zřetězený seznam
# s dodatečnou vlastností, že jeho prvky jsou vždy vzestupně
# seřazené.

from typing import List, Optional


# Třída ‹Node› reprezentuje jeden uzel seznamu, a má dva atributy:
# hodnotu typu ‹int› a odkaz na další uzel ‹next›.

class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


# Následující třída reprezentuje seřazený, zřetězený seznam.
# Implementujte naznačené metody ‹insert› a ‹get_greater_than›.

class SortedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    # Metoda ‹insert› vloží do seznamu nový prvek. Nezapomeňte, že
    # seznam musí být vždy seřazený.

    def insert(self, value: int) -> None:
        top = self.head
        while top is not None:
            if  top.value < value < top.next.value:
                a = top.head.next
                top.head.next = Node(value)
                top.head.next = a
            top = top.head.next

        if top is None:
            self.head = Node(value)


    # Následující metoda vrátí všechny prvky seznamu, kterých
    # hodnoty spadají do oboustranně uzavřeného intervalu [‹value›,
    # ‹value› + ‹dist›]. V případech, kdy se tomu lze vyhnout,
    # neprocházejte seznam zbytečně celý.

    def get_greater_than(self, value: int, dist: int) -> List[int]:
        while self.head is not None:
            if self.head in range(value, dist):
                result.append(i)
            self.head = self.head.next
        return result


def main() -> None:
    test_insert()
    test_get()


def test_get() -> None:
    s_list = SortedList()
    assert s_list.get_greater_than(0, 1000) == []
    s_list.insert(1)
    assert s_list.get_greater_than(0, 10) == [1]
    assert s_list.get_greater_than(0, 0) == []
    assert s_list.get_greater_than(1, 0) == [1]
    s_list.insert(15)
    assert s_list.get_greater_than(0, 10) == [1]
    s_list.insert(5)
    assert s_list.get_greater_than(0, 10) == [1, 5]
    assert s_list.get_greater_than(0, 15) == [1, 5, 15]

    for num in [12, 56, 21, 43]:
        s_list.insert(num)

    assert s_list.get_greater_than(10, 25) == [12, 15, 21]
    assert s_list.get_greater_than(10, 10) == [12, 15]
    assert s_list.get_greater_than(10, 2) == [12]
    assert s_list.get_greater_than(10, 0) == []


def test_insert() -> None:
    s_list = SortedList()
    s_list.insert(4)
    assert s_list.head is not None
    assert s_list.head.value == 4
    s_list.insert(5)
    assert s_list.head.value == 4
    assert s_list.head.next is not None
    assert s_list.head.next.value == 5
    s_list.insert(3)
    assert s_list.head.value == 3
    assert s_list.head.next.value == 4
    assert s_list.head.next.next is not None
    assert s_list.head.next.next.value == 5

    s_list = SortedList()
    assert s_list.head is None
    s_list.insert(1)
    s_list.insert(0)
    s_list.insert(-1)
    s_list.insert(5)
    assert s_list.head is not None
    assert s_list.head.value == -1
    assert s_list.head.next is not None
    assert s_list.head.next.value == 0
    assert s_list.head.next.next is not None
    assert s_list.head.next.next.value == 1
    assert s_list.head.next.next.next is not None
    assert s_list.head.next.next.next.value == 5


if __name__ == "__main__":
    main()
