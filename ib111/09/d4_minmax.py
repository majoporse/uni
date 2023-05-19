from typing import Optional, List


# Tato ukázka přinese oproti předchozím dvě rozšíření:
#
#  • n-ární stromy (tedy takové, kde počet potomků jednoho uzlu není
#    předem omezen – potomky budeme ukládat do seznamu),
#  • nepřímá (nebo vzájemná – mutual) rekurze, tedy situaci, kdy
#    nějaká funkce ⟦f⟧ ve svém řešení používá k řešení menších
#    podproblémů funkci ⟦g⟧ a naopak, ⟦g⟧ využívá pro menší
#    podproblémy funkci ⟦f⟧.

# Definice stromu se od předchozích liší pouze reprezentací
# následníků. Protože se jedná o seznam, tento může být přirozeně
# prázdný a není tedy potřeba pro neexistující následníky používat
# ‹None›. Protože ale budeme chtít reprezentovat stromy, které
# nemají hodnoty ve všech uzlech, objeví se ‹None› tentokrát jako
# možná hodnota uzlu.

class Tree:
    def __init__(self, value: Optional[int], children: List['Tree']):
        self.value = value
        self.children = children


# Jaký problém tedy budeme řešit? Uvažme strom, který má dva typy
# vnitřních uzlů (vnitřní uzly jsou ty, které mají nějaké
# následníky): uzly typu „min“ a uzly typu „max“. Tyto jsou ve
# stromě navíc rozvrženy tak, že uzel „max“ má následníky pouze typu
# „min“ a naopak, uzel „min“ má následníky pouze typu „max“.

# Bude výhodné o situaci uvažovat tak, že to, které uzly budou „min“
# a které „max“ bude záviset od jejich vzdálenosti od kořene, a od
# toho, je-li kořen typu „min“ nebo typu „max“. Krom vnitřních uzlů
# má strom «listy»: to jsou právě ty uzly, které již žádné
# následníky nemají. Náš „minmax“ strom bude v listech obsahovat
# celá čísla. Hodnotu vnitřního uzlu pak spočítáme jako minimum
# (je-li to uzel typu „min“) nebo maximum (je-li typu „max“) hodnot
# všech jeho následníků.

# Funkce nazveme ‹tree_minmax› (kořen je typu „min“) a ‹tree_maxmin›
# (kořen je typu „max“). Z popisu výše je zřejmé, že je-li kořen
# stromu typu „min“, budou kořeny všech podstromů typu „max“:
# rekurzivní volání proto bude vždy používat opačnou funkci.

def tree_minmax(tree: Tree) -> int:

    # Jako vždy, nejprve vyřešíme jednoduché případy: konkrétně zde
    # případ, kdy je uzel listem (má hodnotu nastavenu přímo).

    if tree.value is not None:
        return tree.value

    # Ze seznamu potomků (podstromů) vytvoříme seznam jejich hodnot
    # použitím funkce ‹tree_maxmin›. Z tohoto seznamu již lehce
    # získáme výsledek: protože kořen je typu „min“, bude to minimum
    # z hodnot všech následníků.

    return min([tree_maxmin(child) for child in tree.children])


# Funkce ‹tree_maxmin› je vůči ‹tree_minmax› zcela symetrická:

def tree_maxmin(tree: Tree) -> int:
    if tree.value is not None:
        return tree.value
    return max([tree_minmax(child) for child in tree.children])


# Funkce již zbývá pouze otestovat.

def internal(children: List[Tree]) -> Tree:
    return Tree(None, children)


def leaf(value: int) -> Tree:
    return Tree(value, [])


def main() -> None:  # demo
    t1 = internal([internal([leaf(1), leaf(2)]),
                   internal([leaf(3), leaf(4)])])
    t2 = internal([t1, internal([leaf(4), leaf(5), leaf(6)])])
    assert tree_minmax(t1) == 2
    assert tree_maxmin(t1) == 3
    assert tree_minmax(t2) == 3
    assert tree_maxmin(t2) == 4


if __name__ == '__main__':
    main()
