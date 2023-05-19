# Na vstupu dostanete (standardní Pythonovský) seznam čísel
# z rozsahu ⟦⟨0, n - 1⟩⟧ takový, že každé číslo se v něm vyskytuje
# právě jednou, a který tedy popisuje permutaci. Na každém indexu
# tohoto seznamu najdete číslo, na které se má daný index permutací
# zobrazit. Vaším úkolem je tuto permutaci aplikovat na vstupní
# zřetězený seznam (t.j. upravit odpovídajícím způsobem pořadí uzlů
# ve vstupním seznamu).


from typing import Optional, List


class Node:
    def __init__(self, value: int):
        self.value = value
        self.next: Optional['Node'] = None


class LinkedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None


def shuffle(permutation: List[int], linked: LinkedList) -> None:
    pass


def main() -> None:
    assert shuffle_test([], [], [])
    assert shuffle_test([0, 1], [1, 2], [1, 2])
    assert shuffle_test([1, 0], [1, 2], [2, 1])
    assert shuffle_test([1, 0, 2], [0, 1, 2], [1, 0, 2])
    assert shuffle_test([0, 2, 1, 3], [1, 2, 3, 4], [1, 3, 2, 4])
    assert shuffle_test([0], [-1], [-1])
    assert shuffle_test([1, 0, 4, 2, 3],
                        [0, 1, 2, 3, 4], [1, 0, 3, 4, 2])


def build_linked(nums: List[int]) -> LinkedList:
    result = LinkedList()

    if len(nums) == 0:
        return result

    result.head = Node(nums[0])
    tail = result.head

    for i in range(1, len(nums)):
        tail.next = Node(nums[i])
        tail = tail.next

    return result


def check_list_content(to_check: LinkedList,
                       expected_content: List[int]) -> bool:
    curr_idx = 0
    curr_node = to_check.head

    while curr_node is not None:
        if len(expected_content) == curr_idx:
            return False

        if curr_node.value != expected_content[curr_idx]:
            return False

        curr_node = curr_node.next
        curr_idx += 1

    return len(expected_content) == curr_idx


def shuffle_test(permutation: List[int],
                 list_nums: List[int],
                 expected_content: List[int]) -> bool:
    test_list = build_linked(list_nums)
    shuffle(permutation, test_list)

    return check_list_content(test_list, expected_content)


if __name__ == "__main__":
    main()
