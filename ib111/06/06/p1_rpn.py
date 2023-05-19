from typing import Dict, List, Optional


# Napište (čistou) funkci, která na vstupu dostane:
#
#  • neprázdný výraz ‹expr› složený z proměnných a z aritmetických
#    operátorů, zapsaný v postfixové notaci, a
#  • slovník, přiřazující proměnným číselnou hodnotu (můžete se
#    spolehnout, že všechny proměnné použité v daném výrazu jsou
#    v tomto slovníku obsaženy),
#
# a vrátí číslo, na které se daný výraz vyhodnotí. Mezi všemi
# operátory a proměnnými se v daném výrazu nachází mezera a povolené
# operátory jsou pouze ‹+› a ‹*›.

def rpn_eval(expr: str, variables: Dict[str, int]) -> Optional[int]:
    stack: List[int] = []
    for variable in expr.split():
        (stack.append(stack.pop()+stack.pop()) )if variable == '+'
            
        elif variable == '*':
            stack.append(stack.pop()*stack.pop())
        else:
            num = variables.get(variable)
            assert num is not None
            stack.append(num)
    assert len(stack) == 1
    return stack[0]


def main() -> None:
    assert rpn_eval("a", {"a": 5}) == 5
    assert rpn_eval("a b +", {"a": 1, "b": -4}) == -3
    assert rpn_eval("x y +", {"x": 1, "y": 2}) == 3
    assert rpn_eval("x y + y * z +", {"x": 5, "y": 2, "z": 25}) == 39
    assert rpn_eval("x x * x *", {"x": 5}) == 125
    assert rpn_eval("a a a a a a + + + + +", {"a": 1}) == 6


if __name__ == '__main__':
    main()
