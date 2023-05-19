from typing import List

# Uvažme následovný problém: na vstupu máme výškový profil trasy, a
# zajímá nás, jak dlouho jsme se pohybovali ve výšce aspoň takové,
# v jaké jsme teď. Zajímavé hodnoty budeme samozřejmě dostávat pouze
# na sestupu. Například (aktuální pozici budeme značit symbolem × a
# odpovídající úsek vyšší nadmořské výšky vybarvíme):
#
#   ┌─┐     ┌─┐          ┌─┐     ┌─┐          ┌─┐     ┌─┐
#   │░├─┐ ┌─┤ ├─┐ ┌─┐    │░├─┐ ┌─┤ ├─┐ ┌─┐    │░├─┐ ┌─┤ ├─┐ ┌─┐
#   │░│ │ │ │ │ ├─┤ │    │░│░│ │ │ │ ├─┤ │    │░│░│ │ │ │ ├─┤ │
#   │░│ ├─┤ │ │ │ │ ├─┐  │░│░├─┤ │ │ │ │ ├─┐  │░│░├─┤ │ │ │ │ ├─┐
#   │░│ │ │ │ │ │ │ │ │  │░│░│ │ │ │ │ │ │ │  │░│░│░│ │ │ │ │ │ │
#   └─┴─┴─┴─┴─┴─┴─┴─┴─┘  └─┴─┴─┴─┴─┴─┴─┴─┴─┘  └─┴─┴─┴─┴─┴─┴─┴─┴─┘
#    ×                    0 ×                  0   ×
#
#   ┌─┐     ┌─┐          ┌─┐     ┌─┐          ┌─┐     ┌─┐
#   │ ├─┐ ┌─┤ ├─┐ ┌─┐    │ ├─┐ ┌─┤░├─┐ ┌─┐    │ ├─┐ ┌─┤░├─┐ ┌─┐
#   │ │ │ │░│ │ ├─┤ │    │ │ │ │ │░│ ├─┤ │    │ │ │ │░│░│░├─┤ │
#   │ │ ├─┤░│ │ │ │ ├─┐  │ │ ├─┤ │░│ │ │ ├─┐  │ │ ├─┤░│░│░│ │ ├─┐
#   │ │ │ │░│ │ │ │ │ │  │ │ │ │ │░│ │ │ │ │  │ │ │ │░│░│░│ │ │ │
#   └─┴─┴─┴─┴─┴─┴─┴─┴─┘  └─┴─┴─┴─┴─┴─┴─┴─┴─┘  └─┴─┴─┴─┴─┴─┴─┴─┴─┘
#          ×                      ×                  3   ×
#
#   ┌─┐     ┌─┐          ┌─┐     ┌─┐         ┌─┐     ┌─┐
#   │ ├─┐ ┌─┤░├─┐ ┌─┐    │ ├─┐ ┌─┤ ├─┐ ┌─┐   │░├─┐ ┌─┤░├─┐ ┌─┐
#   │ │ │ │░│░│░├─┤ │    │ │ │ │ │ │ ├─┤░│   │░│░│ │░│░│░├─┤░│
#   │ │ ├─┤░│░│░│░│ ├─┐  │ │ ├─┤ │ │ │ │░├─┐ │░│░├─┤░│░│░│░│░├─┐
#   │ │ │ │░│░│░│░│ │ │  │ │ │ │ │ │ │ │░│ │ │░│░│░│░│░│░│░│░│░│
#   └─┴─┴─┴─┴─┴─┴─┴─┴─┘  └─┴─┴─┴─┴─┴─┴─┴─┴─┘ └─┴─┴─┴─┴─┴─┴─┴─┴─┘
#          3     ×                      ×     0               ×


# Definujeme tedy čistou funkci ‹hills›, která dostane na vstupu
# seznam výšek (celých čísel) a které výsledkem bude stejně dlouhý
# seznam indexů, které odpovídají vždy prvnímu vybarvenému sloupci
# v ilustraci výše.

def hills(heights: List[int]) -> List[int]:

    # V proměnné ‹stack› budeme udržovat zásobník, který bude
    # obsahovat indexy všech předchozích vrcholů, které jsou nižší
    # než ten aktuální. Do proměnné ‹indices› budeme počítat
    # výsledný seznam indexů.

    stack: List[int] = []
    indices: List[int] = []
    for i in range(len(heights)):
        while len(stack) > 0 and heights[stack[-1]] >= heights[i]:
            stack.pop()
        if len(stack) == 0:
            indices.append(0)
        else:
            indices.append(stack[-1] + 1)
        stack.append(i)
    return indices


# Funkčnost ověříme na několika příkladech (seznam ‹example›
# odpovídá obrázku výše).

def main() -> None:  # demo
    assert hills([1, 2, 3]) == [0, 1, 2]
    assert hills([3, 2, 1]) == [0, 0, 0]
    assert hills([1, 2, 1]) == [0, 1, 0]
    assert hills([2, 2, 2]) == [0, 0, 0]
    assert hills([1, 2, 3, 2]) == [0, 1, 2, 1]
    assert hills([1, 3, 2, 3]) == [0, 1, 1, 3]
    assert hills([3, 1, 3, 2]) == [0, 0, 2, 2]
    example = [4, 3, 1, 3, 4, 3, 2, 3, 1]
    assert hills(example) == [0, 0, 0, 3, 4, 3, 3, 7, 0]


if __name__ == '__main__':
    main()
