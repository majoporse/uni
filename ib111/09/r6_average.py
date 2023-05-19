from typing import Optional
from math import isclose


class Tree:
    def __init__(self, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None) -> None:
        self.left = left
        self.right = right


# Napište čistou funkci, která pro vstupní binární strom spočítá
# průměrnou délku větve (cesty od kořene k listu).

def average_branch_len(tree) -> float:
    pass


def main() -> None:
    assert isclose(average_branch_len(None), 0)
    assert isclose(average_branch_len(Tree()), 1)
    assert isclose(average_branch_len(Tree(Tree())), 2)
    assert isclose(average_branch_len(Tree(Tree(), Tree())), 2)

    assert isclose(average_branch_len(
        Tree(Tree(Tree()), Tree(Tree(), Tree(Tree())))), 10 / 3)
    assert isclose(average_branch_len(
        Tree(Tree(Tree(), Tree()),
             Tree(Tree(Tree(), Tree()),
                  Tree(Tree(Tree(), Tree()), Tree())))), 28 / 7)
    assert isclose(average_branch_len(
        Tree(None, Tree(Tree(None, Tree(
            Tree(None, Tree()), None)), None))), 6)
    assert isclose(average_branch_len(
        Tree(Tree(Tree(Tree())), Tree())), 3)
    assert isclose(average_branch_len(
        Tree(Tree(Tree(Tree(Tree()))), Tree())), 7 / 2)


if __name__ == "__main__":
    main()
