from typing import Optional


# V tomto příkladu budeme pracovat se stromy, které mají
# v jednotlivých uzlech uloženy řetězce. Tyto stromy budeme používat
# k reprezentaci aritmetických výrazů složených z konstant a
# binárních operátorů:
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


# Napište čistou funkci, která dostane výše popsaný strom jako
# parametr a vrátí odpovídající plně uzávorkovaný aritmetický výraz,
# formou řetězce. Plným uzávorkováním myslíme, že každému
# aritmetickému operátoru přísluší jedna dvojice kulatých závorek.

def tree_to_expr(tree) -> str:
    pass


def main() -> None:
    t1 = Tree("5")
    t2 = Tree("+", Tree("2"), Tree("4"))
    t3 = Tree("*", t1, t2)
    t4 = Tree("-", Tree("0"), t3)

    assert tree_to_expr(t1) == "5"
    assert tree_to_expr(t2) == "(2 + 4)"
    assert tree_to_expr(t3) == "(5 * (2 + 4))"
    assert tree_to_expr(t4) == "(0 - (5 * (2 + 4)))"


if __name__ == '__main__':
    main()
