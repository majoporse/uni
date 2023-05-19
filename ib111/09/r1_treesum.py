from typing import Optional


# Uvažujme ternární stromy, které mají v uzlech uložena celá čísla:

class Tree:
    def __init__(self, value: int,
                 first: Optional['Tree'] = None,
                 second: Optional['Tree'] = None,
                 third: Optional['Tree'] = None):
        self.value = value
        self.first = first
        self.second = second
        self.third = third


# Napište čistou funkci, která na vstupu dostane instanci výše
# popsaného stromu a vrátí součet všech hodnot ve všech jeho uzlech.

def sum_tree(tree) -> int:
    if tree is None:
        return 0
    return tree.value + sum_tree(tree.first) + sum_tree(tree.second) + sum_tree(tree.third)
    


def main() -> None:
    t1 = Tree(5)
    t2 = Tree(1, Tree(2), Tree(3), Tree(4))
    t3 = Tree(2, None, Tree(1))
    t4 = Tree(10, t2)
    t5 = Tree(-5, Tree(5), t1, t4)

    assert sum_tree(t1) == 5
    assert sum_tree(t2) == 10
    assert sum_tree(t3) == 3
    assert sum_tree(t4) == 20
    assert sum_tree(t5) == 25


if __name__ == '__main__':
    main()
