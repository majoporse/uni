from typing import Optional, List


# Uvažme n-ární strom, který má v uzlech uloženu volitelnou hodnotu
# typu ‹int›.

class Tree:
    def __init__(self, children: Optional[List["Tree"]] = None):
        self.value: Optional[int] = None
        self.children = children if children is not None else []


# Napište proceduru, která v argumentu dostane instanci výše
# popsaného stromu, a vyplní atributy ‹value› všech jeho uzlů tak,
# aby v každém uzlu byl uložen celkový počet jeho potomků (tedy
# včetně nepřímých).

def count1(tree: Tree) -> int:
    count = 0
    for child in tree.children:
        count += 1 + count1(child)
    tree.value = count
    return count


def count_children(tree: Tree) -> None:
    count = 0
    for child in tree.children:
        count += 1 + count1(child)
    tree.value = count


def main() -> None:
    t1 = Tree()
    count_children(t1)
    assert get_value(t1, []) == 0

    t2 = Tree([Tree(), Tree()])
    count_children(t2)
    assert get_value(t2, []) == 2
    assert get_value(t2, [0]) == 0
    assert get_value(t2, [1]) == 0

    t3 = Tree([Tree(), Tree([Tree([Tree()])])])
    count_children(t3)
    assert get_value(t3, []) == 4
    assert get_value(t3, [0]) == 0
    assert get_value(t3, [1]) == 2
    assert get_value(t3, [1, 0]) == 1
    assert get_value(t3, [1, 0, 0]) == 0

    t4 = Tree([Tree(),
               Tree([Tree([Tree(), Tree()])]),
               Tree()])
    count_children(t4)
    assert get_value(t4, []) == 6
    assert get_value(t4, [0]) == 0
    assert get_value(t4, [1]) == 3
    assert get_value(t4, [2]) == 0
    assert get_value(t4, [1, 0]) == 2
    assert get_value(t4, [1, 0, 0]) == 0
    assert get_value(t4, [1, 0, 1]) == 0


def get_value(tree: Tree, indices: List[int],
              current: int = 0) -> int:
    if current == len(indices):
        assert tree.value is not None
        return tree.value
    subtree = tree.children[indices[current]]
    return get_value(subtree, indices, current + 1)


if __name__ == '__main__':
    main()
