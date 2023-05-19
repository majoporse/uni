from typing import List


# Implementujte čistou funkci ‹count_in_sorted›, která ve vzestupně
# seřazeném seznamu ‹records› co nejefektivněji spočte počet výskytů
# hodnoty ‹value›. K hodnotám v ‹records› přistupujte použitím
# metody ‹get›: např. ‹records.get(7)› vrátí hodnotu na indexu 7.
# Délku seznamu získáte voláním ‹records.size()›.

def count_in_sorted(records: 'CountingList', value: int) -> int:
    right = records.size() - 1
    left = 0
    current = left + (right - left)//2
    while records.get(current) != value:
        if records.get(current) > value:
            right = current
        else:
            left = current + 1
        if left == right:
            return 0
        current = left + (right - left)//2

    r_check = current + 1
    l_left = 0
    r_left = current
    l_check = (r_left - l_left)//2 + l_left

    while not(records.get(l_check) == value
              and records.get(l_check - 1) != value):
        if records.get(l_check) == value:
            r_left = l_check
        else:
            l_left = l_check + 1
        l_check = (r_left - l_left)//2 + l_left

        if l_check < 0 or l_left == r_left:
            break
    count = current - l_check + 1

    r_right = records.size()
    l_right = current
    r_check = (r_right - l_right)//2 + l_right

    while not(records.get(r_check) == value
              and records.get(r_check + 1) != value):
        if records.get(r_check) == value:
            l_right = r_check
        else:
            r_right = r_check
        r_check = (r_right - l_right)//2 + l_right

        if r_check == records.size() - 1 or l_right == r_right:
            break

    count += r_check - current
    return count


def main() -> None:
    assert count_in_sorted(CountingList([1, 2, 2, 5]), 2) == 2
    assert count_in_sorted(CountingList([1, 2, 2, 5]), 1) == 1
    assert count_in_sorted(CountingList([1, 2, 2, 2, 2]), 2) == 4
    assert count_in_sorted(CountingList([2, 2, 2, 3]), 2) == 3
    assert count_in_sorted(CountingList([1, 2, 2, 5]), 10) == 0
    big_1 = CountingList([x // 3 for x in range(1000)])
    big_2 = CountingList([x // 7 for x in range(1000)])
    assert count_in_sorted(big_1, 180) == 3
    assert big_1.access_count() < 100
    assert count_in_sorted(big_2, 90) == 7
    assert big_2.access_count() < 100
    big_3 = CountingList([1, 1] + [2] * 1000 + [3, 3])
    assert count_in_sorted(big_3, 2) == 1000
    assert big_3.access_count() < 100


class CountingList:

    def __init__(self, items: List[int]):
        self.__items = items
        self.__count = 0

    def get(self, index: int) -> int:
        self.__count += 1
        return self.__items[index]

    def size(self) -> int:
        return len(self.__items)

    def access_count(self) -> int:
        return self.__count


if __name__ == "__main__":
    main()
