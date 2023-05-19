from typing import Optional, Tuple


# Třídy ‹IntTree›, ‹StrTree› a ‹TupleTree› reprezentují postupně
# stromy, které mají v uzlech uložená celá čísla (‹int›), řetězce
# (‹str›) a dvojice číslo + řetězec.

class IntTree:
    def __init__(self, value: int, left: Optional['IntTree'] = None,
                 right: Optional['IntTree'] = None):
        self.value = value
        self.left = left
        self.right = right


class StrTree:
    def __init__(self, value: str, left: Optional['StrTree'] = None,
                 right: Optional['StrTree'] = None):
        self.value = value
        self.left = left
        self.right = right


class TupleTree:
    def __init__(self, value: Tuple[int, str],
                 left: Optional['TupleTree'] = None,
                 right: Optional['TupleTree'] = None):
        self.value = value
        self.left = left
        self.right = right


# Napište (čistou) funkci, která na vstupu dostane jednu instanci
# ‹IntTree› a jednu instanci ‹StrTree› a vrátí nový strom typu
# ‹TupleTree›, který vznikne takto:
#
#  • uzel ve výstupním stromě bude přítomen, existuje-li
#    odpovídající uzel v obou vstupních stromech,
#  • hodnota uzlu vznikne jako dvojice hodnot uložených
#    v odpovídajících uzlech vstupních stromů.

def treezip(it, st):
    pass


def main() -> None:
    int0 = IntTree(5)
    str0 = StrTree("a")
    mix0 = treezip(int0, str0)
    assert mix0 is not None
    assert mix0.left is None
    assert mix0.right is None
    assert mix0.value == (5, "a")

    int1 = IntTree(1)
    int1.left = IntTree(2)
    int1.right = IntTree(3)
    str1 = StrTree("a")
    str1.left = StrTree("b")
    str1.right = StrTree("c")
    mix1 = treezip(int1, str1)
    assert mix1 is not None
    assert mix1.value == (1, "a")
    assert mix1.left is not None
    assert mix1.left.value == (2, "b")
    assert mix1.right is not None
    assert mix1.right.value == (3, "c")
    assert mix1.left.left is None
    assert mix1.left.right is None
    assert mix1.right.left is None
    assert mix1.right.right is None

    int2 = IntTree(5, IntTree(1), IntTree(2))
    str2 = StrTree("a", StrTree("c"))
    mix2 = treezip(int2, str2)
    assert mix2 is not None
    assert mix2.value == (5, "a")
    assert mix2.left is not None
    assert mix2.left.value == (1, "c")
    assert mix2.left.left is None
    assert mix2.left.right is None
    assert mix2.right is None

    int3 = IntTree(5,
                   IntTree(6),
                   IntTree(7, IntTree(8), IntTree(9)))
    str3 = StrTree("a", None,
                   StrTree("x", StrTree("y")))
    mix3 = treezip(int3, str3)
    assert mix3 is not None
    assert mix3.value == (5, "a")
    assert mix3.left is None
    assert mix3.right is not None
    assert mix3.right.value == (7, "x")
    assert mix3.right.left is not None
    assert mix3.right.left.value == (8, "y")
    assert mix3.right.right is None


if __name__ == '__main__':
    main()
