from typing import List


# Naprogramujte algoritmus řazení výběrem (formou procedury, která
# upraví vstupní seznam).

def selectsort(num_list: List[int]) -> None:
    for i in range(len(num_list) - 1):
        leftmin = i
        for j in range(i, len(num_list)):
            if num_list[j] < num_list[leftmin]:
                leftmin = j
        num_list[i], num_list[leftmin] = num_list[leftmin], num_list[i]        
        


def main() -> None:
    assert selectsort_test([], [])
    assert selectsort_test([1], [1])
    assert selectsort_test([1, 2, 3, 4], [1, 2, 3, 4])
    assert selectsort_test([2, 1], [1, 2])
    assert selectsort_test([2, 1, 4, 3, 5], [1, 2, 3, 4, 5])
    assert selectsort_test([-15, 0, 0, -2], [-15, -2, 0, 0])
    assert selectsort_test([1, 2, 3, 2, 4], [1, 2, 2, 3, 4])
    assert selectsort_test([2, -100, 25, 0, 14], [-100, 0, 2, 14, 25])


def selectsort_test(test_list: List[int],
                    expected_result: List[int]) -> bool:
    selectsort(test_list)
    return test_list == expected_result


if __name__ == "__main__":
    main()
