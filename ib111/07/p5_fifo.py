from typing import Optional


# V této úloze budeme implementovat (tentokrát neomezenou) frontu
# pomocí zřetězeného seznamu. Třídu ‹Node› nemusíte měnit (bude
# sloužit jako jeden uzel fronty):

class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


# Třída ‹Queue› bude implementovat běžné rozhraní fronty (‹push›,
# ‹pop›) a data bude ukládat do jednoho spojitého řetězu uzlů
# (instancí třídy ‹Node›). Hlavu tohoto řetězu (tzn. takový uzel,
# z kterého lze dojít do všech ostatních uzlů) uložte do atributu
# ‹chain›. Řetěz musí mít právě tolik prvků, kolik jich je uloženo
# ve frontě a musí být ukončen uzlem, který má ‹next› nastavený na
# ‹None›. Výjimku tvoří případ, kdy je fronta prázdná, kdy není
# hodnota ‹chain› vůbec určena.
#
# «Pozor:» V žádné metodě neprocházejte celý seznam.

class Queue:

    def __init__(self) -> None:
        self.chain = None
        self.last = None
        

    def push(self, value: int) -> None:
        a = Node(value)
        if self.chain is None:
            self.chain = a
            self.last = a

        else:
            self.last.next = a
            self.last = a

    def pop(self) -> Optional[int]:
        
        if self.chain is None:
            return None
        a = self.chain.value
        self.chain = self.chain.next 
        return a


def main() -> None:
    queue = Queue()
    queue.push(1)
    check_count(queue, 1)
    check_value(queue.pop(), 1)
    assert queue.pop() is None
    queue.push(3)
    queue.push(5)
    queue.push(7)

    assert queue.chain is not None
    broken = queue.chain.next
    assert broken is not None
    lost = broken.next
    assert lost is not None
    broken.next = None

    queue.push(8)
    queue.push(9)
    check_value(queue.pop(), 3)
    broken.next = lost
    check_value(queue.pop(), 5)
    check_value(queue.pop(), 7)
    check_value(queue.pop(), 8)
    check_value(queue.pop(), 9)
    assert queue.pop() is None


def check_count(queue: Queue, count: int) -> None:
    node = queue.chain
    while node:
        node = node.next
        count -= 1
    assert count == 0


def check_value(value: Optional[int], expect: int) -> None:
    assert value is not None
    assert value == expect


if __name__ == '__main__':
    main()
