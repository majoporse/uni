from typing import Optional


# V tomto příkladu budeme opět pracovat se stromy, které
# reprezentují aritmetické výrazy. Tyto mají následující strukturu:
#
#  • konstantu reprezentuje strom, který má oba podstromy prázdné,
#  • složený výraz je reprezentován stromem, který má v kořenu
#    uložen operátor a jeho neprázdné podstromy reprezentují
#    operandy.
#
# Žádné jiné uzly ve stromě přítomny nebudou. Hodnoty konstant lze
# na celá čísla převést zabudovanou funkcí ‹int›.

class Tree:
    def __init__(self, value: str,
                 left: Optional['Tree'] = None,
                 right: Optional['Tree'] = None):
        self.value = value
        self.left = left
        self.right = right


# Napište čistou funkci, která na vstupu dostane instanci výše
# popsaného stromu a vrátí výsledek vyhodnocení výrazu, který
# tento strom reprezentuje.

def evaluate(tree: Optional[Tree]) -> int:
    count = 0
    if tree is None:
        return count
    elif tree.value == "*":
        count += evaluate(tree.left) * evaluate(tree.right)
    elif tree.value == "+":
        count += evaluate(tree.left) + evaluate(tree.right)
    else:
        count += int(tree.value)
    return count


def main() -> None:
    t1 = Tree("5")
    t2 = Tree("+", Tree("2"), Tree("4"))
    t3 = Tree("*", t1, t2)
    t4 = Tree("*", Tree("0"), t3)

    assert evaluate(t1) == 5
    assert evaluate(t2) == 6
    assert evaluate(t3) == 30
    assert evaluate(t4) == 0


if __name__ == '__main__':
    main()
