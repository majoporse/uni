from typing import Optional


# Toto je poslední z příkladů, ve kterém budeme pracovat
# s aritmetickými výrazy. Tyto mají následující strukturu:
#
#  • konstantu reprezentuje strom, který má oba podstromy prázdné,
#  • složený výraz je reprezentován stromem, který má v kořenu
#    uložen operátor a jeho neprázdné podstromy reprezentují
#    operandy.
#
# Žádné jiné uzly ve stromě přítomny nebudou.

class Tree:
    def __init__(self, value: str,
                 left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.value = value
        self.left = left
        self.right = right


# Napište čistou funkci, která dostane jako parametr instanci výše
# uvedeného stromu reprezentující nějaký aritmetický výraz, a vrátí
# řetězec, ve kterém je tento výraz zapsán v postfixové (rpn)
# notaci. Konstanty i operátory budou ve výstupu odděleny právě
# jednou mezerou.

def to_rpn(tree: Optional[Tree]) -> str:
    if tree is None:
        return ' '
    elif tree.value == "*":
        return to_rpn(tree.left) + ' ' + to_rpn(tree.right) + ' *'
    elif tree.value == "+":
        return to_rpn(tree.left) + ' ' + to_rpn(tree.right) + ' +'
    else:
        return tree.value


def main() -> None:
    t1 = Tree("5")
    t2 = Tree("+", Tree("2"), Tree("4"))
    t3 = Tree("*", t1, t2)
    t4 = Tree("+", t3, Tree("0"))

    assert to_rpn(t1) == "5"
    assert to_rpn(t2) == "2 4 +"
    assert to_rpn(t3) == "5 2 4 + *"
    assert to_rpn(t4) == "5 2 4 + * 0 +"


if __name__ == '__main__':
    main()
