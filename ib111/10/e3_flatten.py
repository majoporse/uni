from typing import List, Union

# Typ pro libovolně zanořený seznam znáte z přednášky. Nejprve
# zadefinujeme typový alias pro jeden prvek takového seznamu:

NestedListItem = Union[int, 'NestedList']


# A s jeho pomocí pak samotný typ seznamu, ‹NestedList›:

class NestedList:
    def __init__(self, a_list: List[NestedListItem]):
        self.list = a_list


# Vaším úkolem je napsat čistou funkci, která na vstupu dostane
# ‹NestedList› (vnořený seznam celých čísel) a vrátí obyčejný
# seznam, který zachovává pořadí čísel na vstupu, ale „zapomene“
# strukturu vnoření.

def flatten(to_flatten: NestedList) -> List[int]:
    pass


def main() -> None:
    assert flatten(NestedList([])) == []
    assert flatten(NestedList([1, 2, 3])) == [1, 2, 3]
    assert flatten(NestedList([NestedList([NestedList([NestedList([1])]),
                                           NestedList([2])]), 3])) == [1, 2, 3]
    assert flatten(NestedList([NestedList([1, 2]),
                               NestedList([NestedList([7, 4]),
                                           NestedList([5])])])) \
        == [1, 2, 7, 4, 5]


if __name__ == '__main__':
    main()
