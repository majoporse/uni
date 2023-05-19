from typing import List, Union

# † Z přednášky již znáte vnořený seznam čísel ‹NestedList›:

NestedListItem = Union[int, 'NestedList']


class NestedList:
    def __init__(self, a_list: List[NestedListItem]):
        self.list = a_list


# Napište proceduru, která na vstupu dostane ‹NestedList› celých
# čísel a upraví ho tak, aby v něm byla čísla seřazená vzestupně
# napříč všemi vnitřními seznamy. Například seznam ‹[[4, 7, 1], [],
# [8], [0, 5]]› se použitím této procedury změní na ‹[[0, 1, 4], [],
# [5], [7, 8]]›.

def sort_nested(list_of_lists: NestedList) -> None:
    pass


def main() -> None:
    check_sort_nested(NestedList([]), NestedList([]))
    check_sort_nested(NestedList([NestedList([4, 1, 7]), NestedList([]),
                                  NestedList([8]), NestedList([0, 5])]),
                      NestedList([NestedList([0, 1, 4]), NestedList([]),
                                  NestedList([5]), NestedList([7, 8])]))
    check_sort_nested(NestedList([NestedList([1, 8, NestedList([2])])]),
                      NestedList([NestedList([1, 2, NestedList([8])])]))
    check_sort_nested(NestedList([NestedList([NestedList([1])])]),
                      NestedList([NestedList([NestedList([1])])]))


def equal_nested(a: NestedListItem, b: NestedListItem) -> bool:
    if isinstance(a, int) or isinstance(b, int):
        return isinstance(a, int) and isinstance(b, int) and a == b

    if len(a.list) != len(b.list):
        return False

    for a_item, b_item in zip(a.list, b.list):
        if not equal_nested(a_item, b_item):
            return False

    return True


def check_sort_nested(original: NestedList, expected: NestedList) -> None:
    sort_nested(original)
    assert equal_nested(original, expected)


if __name__ == '__main__':
    main()
