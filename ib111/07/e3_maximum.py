from typing import Optional


class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None


# Napište čistou funkci, která najde největší hodnotu uloženou ve
# vstupním zřetězeném seznamu, případně ‹None› je-li vstupní seznam
# prázdný.

def maximum(num_list: LinkedList) -> Optional[int]:
    top = num_list.head
    if top is None:
        maximum = top
    else:
        maximum = top.value
    while top is not None:
        if top.next is not None:
            if top.next.value > top.value:
                maximum = top.next.value
            else:
                maximum = top.value
            top = top.next
        else:
            return maximum
    
    return top


def main() -> None:
    test_list = LinkedList()
    assert maximum(test_list) is None
    test_list.head = Node(5)
    assert maximum(test_list) == 5
    test_list.head.next = Node(3)
    assert maximum(test_list) == 5
    test_list.head.next.next = Node(10)
    assert maximum(test_list) == 10
    test_list.head.next.next.next = Node(3)
    assert maximum(test_list) == 10
    test_list.head = Node(-5)
    assert maximum(test_list) == -5
    test_list.head.next = Node(-5)
    assert maximum(test_list) == -5
    test_list.head.next.next = Node(0)
    assert maximum(test_list) == 0


if __name__ == "__main__":
    main()
