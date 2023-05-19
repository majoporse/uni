from typing import Set, List


# Napište čistou funkci, která dostane na vstup množinu čísel a
# vrátí seznam všech jejích podmnožin (v libovolném pořadí).

def subsets(input_set: Set[int]) -> List[Set[int]]:
    if len(input_set) == 0:
        return [set()]
    result = []
    for num in input_set:
        a = input_set.copy()
        a.remove(num)
        b = [{num}.add(rest) for rest in subsets(a)]
        result += b
    return result


def main() -> None:
    subsets_test(set())
    subsets_test({1})
    subsets_test({1, 2})
    subsets_test({1, 2, 3})
    subsets_test({-2, 0, 25, 100})


def subsets_test(input_set: Set[int]) -> None:
    copy = input_set.copy()
    sets = subsets(input_set)
    count = 2 ** len(input_set)
    assert input_set == copy

    if len(sets) != count:
        assert len(sets) != count, (len(sets), '≠', count)

    for i in range(count):
        for j in range(i):
            assert sets[i] != sets[j], (i, j, sets[i])

    for subset in sets:
        assert subset <= input_set, (subset, '⊆', input_set)


if __name__ == '__main__':
    main()
