from typing import List, Optional

# V této úloze budeme programovat jednoduše zřetězený seznam, který
# si v každém uzlu udržuje seznam hodnot ‹data› maximální délky
# ‹capacity›. Jinak je zřetězený seznam definován tak, jak jej už
# znáte:


class Node:
    def __init__(self) -> None:
        self.data: List[int] = []
        self.next: Optional['Node'] = None


class ArrayList:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.head: Optional[Node] = None
        self.tail: Optional[Node] = None

    # Napište metodu ‹append›, která vloží hodnotu ‹value› na konec
    # posledního uzlu, není-li plný, jinak vytvoří nový uzel na
    # konci seznamu.

    def append(self, value: int) -> None:
        if self.tail is not None:
            if len(self.tail.data) < self.capacity:
                self.tail.data.append(value)
            else:
                next_ = Node()
                next_.data.append(value)
                self.tail.next = next_
                self.tail = next_
        else:
            new = Node()
            new.data.append(value)
            self.tail = new
            self.head = new

    # Napište metodu ‹delete›, která smaže první výskyt hodnoty
    # ‹value› ze seznamu. Pokud by po smazání nastalo, že zůstane
    # v seznamu prázdny uzel, smaže se i ten. Například mějme
    # následující seznam:
    #
    #  ┌──────┐ ┌──────┐        ┌──────┐            ┌──────┐
    #  │ head │▶│ next │───────▶│ next │───────────▶│ None │
    #  └──────┘ ├┄┄┄┄┄┄┤ ┌───┐  ├┄┄┄┄┄┄┤ ┌───┬───┐  └──────┘
    #           │ data │▶│ 3 │  │ data │▶│ 5 │ 1 │
    #           └──────┘ └───┘  └──────┘ └───┴───┘
    #
    # Po smazání hodnoty ‹5› bude výsledný seznam vypadat
    # následovně:
    #
    #  ┌──────┐ ┌──────┐        ┌──────┐       ┌──────┐
    #  │ head │▶│ next │───────▶│ next │──────▶│ None │
    #  └──────┘ ├┄┄┄┄┄┄┤ ┌───┐  ├┄┄┄┄┄┄┤ ┌───┐ └──────┘
    #           │ data │▶│ 3 │  │ data │▶│ 1 │
    #           └──────┘ └───┘  └──────┘ └───┘
    #
    # Naproti tomu smazáním hodnoty ‹3› z původního seznamu vznikne
    # prázdny uzel, který se smaže:
    #
    #  ┌──────┐ ┌──────┐            ┌──────┐
    #  │ head │▶│ next │───────────▶│ None │
    #  └──────┘ ├┄┄┄┄┄┄┤ ┌───┬───┐  └──────┘
    #           │ data │▶│ 5 │ 1 │
    #           └──────┘ └───┴───┘

    def delete(self, value: int) -> None:
        current = self.head
        last = None

        while current is not None:
            if value in current.data:
                current.data.remove(value)
                
                if current.data == []:
                    if current.next is None:
                        self.tail = last
                        if last is not None:
                            last.next = None
                    if last is None:
                        self.head = current.next
                    else:
                        last.next = current.next
                break
            last = current
            current = current.next
            

    # Konečně napište metodu ‹compact›, která maximalizuje využití
    # kapacity uzlů: přesune prvky v seznamu tak, aby se uzly
    # v seznamu odpředu zaplnily. Přebytečné prázdné uzly metoda
    # smaže. Ve výsledném seznamu zachovejte vzájemné pořadí prvků.
    # Například kompaktní reprezentace pro seznam z předchozího
    # příkladu a kapacitu ‹3› je:
    #
    #  ┌──────┐ ┌──────┐               ┌──────┐
    #  │ head │▶│ next │──────────────▶│ None │
    #  └──────┘ ├┄┄┄┄┄┄┤ ┌───┬───┬───┐ └──────┘
    #           │ data │▶│ 3 │ 5 │ 1 │
    #           └──────┘ └───┴───┴───┘
    #
    # Výsledek pro seznam s kapacitou ‹2› je:
    #
    #  ┌──────┐ ┌──────┐           ┌──────┐       ┌──────┐
    #  │ head │▶│ next │──────────▶│ next │──────▶│ None │
    #  └──────┘ ├┄┄┄┄┄┄┤ ┌───┬───┐ ├┄┄┄┄┄┄┤ ┌───┐ └──────┘
    #           │ data │▶│ 3 │ 5 │ │ data │▶│ 1 │
    #           └──────┘ └───┴───┘ └──────┘ └───┘

    def compact(self) -> None:
        pass


def main() -> None:
    test_append()
    test_delete()
    test_compact()

    # check handling of the tail pointer
    al = ArrayList(2)
    al.append(1)
    al.append(2)
    al.append(3)
    al.delete(1)
    al.compact()
    al.append(4)
    assert to_list(al) == [[2, 3], [4]]
    al.delete(4)
    assert to_list(al) == [[2, 3]]
    al.append(4)
    assert to_list(al) == [[2, 3], [4]]


def to_list(slist: ArrayList) -> List[List[int]]:
    result = []
    node = slist.head
    while node is not None:
        result.append(node.data)
        node = node.next
    return result


def create_alist(nodes: List[List[int]], cap: int) -> ArrayList:
    alist = ArrayList(cap)
    prev = None
    for data in nodes:
        assert len(data) <= cap
        node = Node()
        node.data = data
        if prev is None:
            alist.head = node
        else:
            prev.next = node
        prev = node
    alist.tail = prev
    return alist


def check_append(capacity: int, append: List[int]) -> None:
    alist = ArrayList(capacity)
    appended: List[List[int]] = [[]]
    for value in append:
        if len(appended[-1]) == capacity:
            appended.append([])
        appended[-1].append(value)
        alist.append(value)
    assert to_list(alist) == appended


def test_append() -> None:
    check_append(1, [1, 2, 3, 4, 5])
    check_append(2, [1, 2, 3, 4, 5])
    check_append(3, [1, 2, 3, 4, 5])
    check_append(5, [1, 2, 3, 4, 5])

    l1 = create_alist([[1], [1], [1, 1]], 2)

    l1.append(2)
    assert to_list(l1) == [[1], [1], [1, 1], [2]]

    l1.append(3)
    assert to_list(l1) == [[1], [1], [1, 1], [2, 3]]

    l1.append(4)
    assert to_list(l1) == [[1], [1], [1, 1], [2, 3], [4]]


def test_delete() -> None:
    l1 = create_alist([[1, 3], [1, 2]], 3)

    l1.delete(3)
    assert to_list(l1) == [[1], [1, 2]]

    l1.delete(1)
    assert to_list(l1) == [[1, 2]]

    l1.delete(2)
    assert to_list(l1) == [[1]]

    l1.delete(1)
    assert to_list(l1) == []

    l1.delete(7)  # do nothing
    assert to_list(l1) == []

    l2 = create_alist([[1], [7, 2], [3], [1, 4, 5]], 3)

    l2.delete(4)
    assert to_list(l2) == [[1], [7, 2], [3], [1, 5]]

    l2.delete(4)  # do nothing
    assert to_list(l2) == [[1], [7, 2], [3], [1, 5]]

    l2.delete(7)
    assert to_list(l2) == [[1], [2], [3], [1, 5]]


def test_compact() -> None:
    l1 = create_alist([[1, 3], [2], [7, 4, 8]], 6)
    l1.compact()
    assert to_list(l1) == [[1, 3, 2, 7, 4, 8]]

    l2 = create_alist([[1, 3], [2], [7, 4, 8]], 4)
    l2.compact()
    assert to_list(l2) == [[1, 3, 2, 7], [4, 8]]

    l3 = create_alist([[1], [2], [7, 4, 8], [9], [12]], 3)
    l3.compact()
    assert to_list(l3) == [[1, 2, 7], [4, 8, 9], [12]]

    l4 = create_alist([[1], [2], [7, 4, 8], [9], [12], [10, 11], [5, 3]], 10)
    l4.compact()
    assert to_list(l4) == [[1, 2, 7, 4, 8, 9, 12, 10, 11, 5], [3]]


if __name__ == "__main__":
    main()
