from typing import Optional


class Tree:
    def __init__(self, key: int,
                 left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.key = key
        self.left = left
        self.right = right


# Binární halda je binární strom, který má dvě speciální vlastnosti
# uvedené níže. V tomto příkladu budeme kontrolovat pouze tu druhou,
# totiž vlastnost haldy:
#
#  1. každé patro je plné (s možnou výjimkou posledního),
#  2. hodnota každého uzlu je větší nebo rovna hodnotě libovolného
#     jeho potomka.
#
# Predikát ‹is_heap› rozhodne, splňuje-li vstupní strom tuto druhou
# vlastnost.
def count(tree):
    if tree.left is None:
        return 0
    return 1 + max(count(tree.left), count(tree.right))

def is_heap(tree) -> bool:
    bool_ = True
    if tree is None:
        return True
    if tree.right is None and tree.left is None:
        return True
    if tree.right is None:
        return tree.key > tree.left.key
    if tree.left is None:
        return tree.key > tree.right.key
    if tree.key < tree.left.key or tree.key < tree.right.key:
        bool_ = False

    count_left = count(tree.left)
    count_right = count(tree.right)
    
    return count_left == count_right and bool_ and is_heap(tree.left) and is_heap(tree.right)


def main() -> None:
    assert is_heap(None)
    assert is_heap(Tree(1))
    assert is_heap(Tree(1, Tree(0), Tree(0)))
    assert is_heap(Tree(1, Tree(1), Tree(1)))
#     assert is_heap(Tree(1, Tree(0)))
    assert not is_heap(Tree(1, Tree(2), Tree(0)))
    assert not is_heap(Tree(1, Tree(1), Tree(2)))
    assert not is_heap(Tree(1, Tree(8)))

#     assert is_heap(Tree(10, Tree(9,
#                                  Tree(7, Tree(3), Tree(2)),
#                                  Tree(6, Tree(1), Tree(0))),
#                         Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(10, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(9))))
    assert not is_heap(Tree(10, Tree(9,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(11), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(10, Tree(11,
                                     Tree(7, Tree(3), Tree(2)),
                                     Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))
    assert not is_heap(Tree(-10, Tree(9,
                                      Tree(7, Tree(3), Tree(2)),
                                      Tree(6, Tree(1), Tree(0))),
                            Tree(8, Tree(5), Tree(4))))


if __name__ == "__main__":
    main()
