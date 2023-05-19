from typing import Optional


# Třída ‹Tree› reprezentuje (neohodnocený) binární strom. Prázdný
# strom je reprezentován hodnotou ‹None›.

class Tree:
    def __init__(self, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.left = left
        self.right = right


# Napište čistou funkci, která vrátí počet uzlů v zadaném stromě.

def count(tree: Optional[Tree]) -> int:
    if tree is None:
        return 0
    return 1 + count(tree.left) + count(tree.right)


def main() -> None:
    assert count(Tree()) == 1
    assert count(Tree(Tree(Tree(), Tree()), Tree())) == 5
    assert count(Tree(Tree(), None)) == 2
    assert count(None) == 0
    assert count(Tree(Tree(),
                      Tree(None,
                           Tree(Tree(Tree(), None), None)))) == 6


if __name__ == "__main__":
    main()
