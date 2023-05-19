from typing import Optional


class Tree:
    def __init__(self, left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None) -> None:
        self.left = left
        self.right = right


# AVL strom je binární strom, který:
#
# 1. je vyhledávací, tzn. splňuje vlastnost popsanou v ukázce
#    ‹d3_lookup›, a zároveň
# 2. pro každý jeho uzel platí ‹abs(l_height - r_height) ≤ 1›, kde
#    ‹l_height› a ‹r_height› jsou výšky levého a pravého podstromu
#    daného uzlu.
#
# Napište predikát, který ověří, že vstupní strom má tuto druhou
# vlastnost (je-li zároveň stromem vyhledávacím ověřovat nemusíte).
# Pokuste se vlastnost ověřit jediným průchodem stromu (tedy každý
# uzel navštivte pouze jednou – naivní řešení, kdy opakovaně
# počítáte výšky průchodem podstromů není příliš uspokojivé).
def countmin(tree):
    if tree is None:
        return 0
    return 1 + min(countmin(tree.left), countmin(tree.right))

def countmax(tree):
    if tree is None:
        return 0
    return 1 + max(countmax(tree.left), countmax(tree.right))

def is_avl(tree) -> bool:
    return abs(countmin(tree) - countmax(tree)) <= 1

def main() -> None:
    assert is_avl(None)
    assert is_avl(Tree(Tree(), Tree()))
    assert is_avl(Tree(None, Tree()))

    assert is_avl(Tree(Tree(Tree(Tree()), Tree()),
                       Tree(Tree(None, Tree()),
                            Tree(Tree(Tree(), Tree()), Tree()))))
    assert not is_avl(Tree(Tree(Tree(Tree()), Tree()),
                           Tree(Tree(), Tree(Tree(Tree(),
                                                  Tree()), Tree()))))
    assert not is_avl(Tree(Tree(Tree(), Tree()),
                           Tree(Tree(None, Tree()),
                                Tree(Tree(Tree(), Tree()), Tree()))))

    assert is_avl(Tree(Tree(Tree(),
                            Tree(Tree(), Tree())),
                       Tree(Tree(), Tree())))
    assert is_avl(Tree(Tree(Tree(), Tree()),
                       Tree(Tree(None, Tree()), Tree())))
    assert is_avl(Tree(Tree(Tree(), Tree()), Tree(Tree(), Tree())))
    assert is_avl(Tree(Tree(Tree()), Tree(None, Tree())))

    assert not is_avl(Tree(Tree(Tree())))
    assert not is_avl(Tree(Tree(Tree(), Tree()),
                           Tree(None, Tree(None, Tree()))))


if __name__ == "__main__":
    main()
