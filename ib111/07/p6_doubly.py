# † V této úloze budeme programovat dvojitě zřetězený seznam, který se
# podobá jednoduše zřetězenému seznamu, který již dobře znáte. Jak
# napovídá už název, každý uzel bude připojen do řetězu na obě
# strany, tzn. krom následovníka si bude pamatovat i svého
# předchůdce.

# Oproti seznamu zřetězenému jednoduše se v tom dvojitém lépe
# odebírají prvky: z libovolného místa seznamu (tedy zejména na obou
# koncích) lze totiž odebrat prvek bez toho, abychom museli seznam
# jakkoliv procházet.

from typing import Optional


class Node:
    def __init__(self, init_val: int) -> None:
        self.value = init_val
        self.next: Optional['Node'] = None
        self.prev: Optional['Node'] = None


class DoubleLinkedList:
    def __init__(self) -> None:
        self.head: Optional['Node'] = None
        self.tail: Optional['Node'] = None

    # Metoda ‹append› přidá novou hodnotu na konec seznamu.

    def append(self, value: int) -> None:
        a = Node(value)
        if self.head is None:
            self.head = a
            self.tail = a
            
        else:
            old_last = self.tail
            old_last.next = a
            self.tail = a
            self.tail.prev = old_last

    # Metoda ‹prepend› naopak vloží novou hodnotu na začátek. Na
    # rozdíl od zabudovaného typu ‹list› je toto v principu levná
    # operace (nic nebudeme procházet).

    def prepend(self, value: int) -> None:
        a = Node(value)
        if self.head is None:
            self.head = a
            self.tail = a
        else:
            old_first = self.head
            old_first.prev = a
            self.head = a
            self.head.next = old_first

    # Metoda ‹remove› odstraní ze seznamu libovolný uzel. Seznam
    # není potřeba procházet od konce.

    def remove(self, node: Node) -> None:
        if node.prev is None:
            
            if node.next is None:
                self.head = None
                self.tail = None
                node = None
                
            else:
                self.head = self.head.next
                node.next.prev = None

        elif node.next is None:
            node.prev.next = None
            self.tail = self.tail.prev

        else:
            prev_node = node.prev
            next_node = node.next
            prev_node.next = next_node
            next_node.prev = prev_node

    # Konečně metoda ‹search› najde první uzel s danou hodnotu.
    # Když takový uzel neexistuje, vrátí ‹None›.

    def search(self, value: int) -> Optional[Node]:
        a = self.head
        if self.head is None:
            return None
        while a.value != value:
            if a.next is None:
                return None
            a = a.next
        return a


def main() -> None:
    test_insertion()
    test_remove()


def remove(d_list: DoubleLinkedList, value: int) -> None:
    node = d_list.search(value)
    assert node is not None
    d_list.remove(node)
    assert d_list.search(value) is None


def test_remove() -> None:
    elems = [4, 2, 6, 8, -3, 11]
    for chosen in elems:
        d_list = DoubleLinkedList()
        for elem in elems:
            d_list.append(elem)

        remove(d_list, chosen)

        for elem in elems:
            if elem != chosen:
                assert d_list.search(elem) is not None

    d_list = DoubleLinkedList()
    for elem in elems:
        d_list.append(elem)

    for elem in elems:
        remove(d_list, elem)

    for elem in elems:
        assert d_list.search(elem) is None


def test_insertion() -> None:
    d_list = DoubleLinkedList()
    for i in [1, 3, 17, 11, 7, 9]:
        d_list.append(i)
        d_list.prepend(i - 1)
    assert d_list.search(1) is not None
    assert d_list.search(4) is None
    assert d_list.search(14) is None

    node = d_list.search(11)
    assert node is not None
    assert node.value == 11

    assert node.prev is d_list.search(17)
    assert node.next is d_list.search(7)

    node = d_list.search(3)
    assert node is not None
    assert node.next is d_list.search(17)

    head, tail = d_list.head, d_list.tail
    assert tail is not None
    assert head is not None
    node = head.next
    assert node is not None

    assert d_list.search(7) is tail.prev
    assert d_list.search(8) is head
    assert d_list.search(6) is head.next
    assert d_list.search(10) is node.next


if __name__ == "__main__":
    main()
