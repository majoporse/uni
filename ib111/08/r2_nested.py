from typing import List


# Implementujte čistou funkci ‹sort_nested›, která vzestupně
# uspořádá prvky v seznamu seznamů čísel ‹lists›, a to tak, že
# přeuspořádá jenom čísla ve vnitřních seznamech, aniž by měnil
# jejich délku. Výstupní seznam bude tedy obsahovat stejný počet
# stejně dlouhých seznamů jako ten vstupní, ale v obecném případě
# budou tyto vnořené seznamy obsahovat jiná čísla.

def sort_nested(lists: List[List[int]]) -> List[List[int]]:
    list_lengths = []
    list_values = []
    result = []
    for list_ in lists:
        list_lengths.append(len(list_))
        list_values += list_
    sorted_values = sorted(list_values)
    position = 0
    for i in list_lengths:
        current = []
        for j in range(i):
            current.append(sorted_values[j + position])
        position += i
        result.append(current)
    return result


def main() -> None:
    assert sort_nested([[5, 4], [1, 2, 3]]) == [[1, 2], [3, 4, 5]]
    assert sort_nested([[5], [4], [1, 2, 3]]) == [[1], [2], [3, 4, 5]]
    assert sort_nested([[5], [4], [2, 1], [3]]) == [[1], [2], [3, 4], [5]]
    assert sort_nested([[5], [4, 2, 1], [3]]) == [[1], [2, 3, 4], [5]]
    lists = [[5], [4, 2, 1], [3]]
    assert sort_nested(lists) == [[1], [2, 3, 4], [5]]
    assert lists == [[5], [4, 2, 1], [3]]


if __name__ == "__main__":
    main()
