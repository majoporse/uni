from typing import Optional


# Třída ‹Tree› reprezentuje (neohodnocený) binární strom. Prázdný
# strom je reprezentován hodnotou ‹None›.

class Tree:
    def __init__(self, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.left = left
        self.right = right


# Napište čistou funkci, která vrátí hloubku zadaného stromu, tzn.
# délku jeho nejdelší větve (posloupnosti uzlů od kořene k listu).

def depth(tree: Optional[Tree]) -> int:
    if tree is None:
        return 0
    return 1 + max([depth(tree.right), depth(tree.left)])


def main() -> None:
    assert depth(Tree()) == 1
    assert depth(Tree(Tree(Tree(), Tree()), Tree())) == 3
    assert depth(Tree(Tree(), None)) == 2
    assert depth(None) == 0
    assert depth(Tree(Tree(),
                      Tree(None,
                           Tree(Tree(Tree(), None), None)))) == 5
    assert depth(Tree(Tree(Tree(),
                           Tree(Tree(Tree(Tree(), None), None),
                                Tree())), Tree(None,
                                               Tree(Tree(Tree(),
                                                         None),
                                                    None)))) == 6


if __name__ == "__main__":
    main()
