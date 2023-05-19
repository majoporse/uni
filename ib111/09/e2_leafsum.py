from typing import List


# Třída ‹Tree› bude tentokrát reprezentovat n-ární strom, který má
# v uzlech uloženy celočíselné hodnoty.

class Tree:
    def __init__(self, value: int, children: List['Tree']):
        self.value = value
        self.children = children


# Napište (čistou) funkci, která na vstupu dostane instanci výše
# popsaného stromu a vrátí součet čísel ve všech jeho listech
# (uzlech bez potomků).

def sum_leaves(tree: Tree) -> int:
    if tree.children == []:
        return tree.value
    return sum([sum_leaves(child) for child in tree.children])


def main() -> None:
    t1 = Tree(5, [])
    t2 = Tree(5, [Tree(5, [Tree(1, [])])])
    t3 = Tree(-1, [t1, t2])
    t4 = Tree(25, [Tree(1, []), t1, t2, t3])

    assert sum_leaves(t1) == 5
    assert sum_leaves(t2) == 1
    assert sum_leaves(t3) == 6
    assert sum_leaves(t4) == 13


if __name__ == '__main__':
    main()
