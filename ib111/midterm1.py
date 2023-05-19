# Úkol 1.

def filter_bad_primes(num):
    result = 1
    for i in range(2, (100 if num > 100 else num + 1)):
        while num % i == 0:
            num //= i
            result *= i

    return result


def test_filter_bad_primes():
    assert filter_bad_primes(1) == 1
    assert filter_bad_primes(1414) == 14
    assert filter_bad_primes(2310) == 2310
    assert filter_bad_primes(12345) == 15
    assert filter_bad_primes(123456) == 192
    assert filter_bad_primes(1295527) == 1
    assert filter_bad_primes(4900000343) == 49


# Úkol 2.
def largest_elf_island(num):
    my_num = num
    biggest_island = 0
    current_island = 0
    position = 0
    biggest_position = 0
    while my_num > 0:

        if my_num % 11 == 10:
            current_island += 1

        if biggest_island < current_island:
            biggest_island = current_island
            biggest_position = position - biggest_island + 1

        if my_num % 11 != 10:
            current_island = 0

#         my_num -= my_num % 11
        my_num //= 11

        position += 1

    return (biggest_position, biggest_island)


def test_largest_elf_island():
    largest_elf_island(1330)
    assert largest_elf_island(0) == (0, 0)
    assert largest_elf_island(100) == (0, 0)
    assert largest_elf_island(2566) == (2, 1)
    assert largest_elf_island(13430) == (0, 2)
    assert largest_elf_island(159840) == (0, 2)
    assert largest_elf_island(205354196303) == (3, 2)
    assert largest_elf_island(285294327680) == (7, 4)


# Úkol 3.

def flats(heights):
    flats = []
    for i in range(len(heights) - 1):
        if heights[i] == heights[i + 1]:

            if not flats:
                flats.append(heights[i])

            elif heights[i] != heights[i - 1]:
                flats.append(heights[i])
    return flats


def test_flats():
    heights = [2, 2, 4, 5, 4, 4, 3]
    assert flats(heights) == [2, 4]
    assert heights == [2, 2, 4, 5, 4, 4, 3]

    heights = [1, 2, 3, 5, 4, 7, 2, 1]
    assert flats(heights) == []
    assert heights == [1, 2, 3, 5, 4, 7, 2, 1]

    heights = [1, 2, 2, 10, 2, 9, 3, 3, 2, 2]
    assert flats(heights) == [2, 3, 2]
    assert heights == [1, 2, 2, 10, 2, 9, 3, 3, 2, 2]

    heights = [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]
    assert flats(heights) == [2]
    assert heights == [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3]

    heights = [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 3]
    assert flats(heights) == []
    assert heights == [0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 3]

    heights = [0, 0, 1, 1, 2, 2, 0, 2, 2, 0, 2]
    assert flats(heights) == [0, 1, 2, 2]
    assert heights == [0, 0, 1, 1, 2, 2, 0, 2, 2, 0, 2]

    heights = []
    assert flats(heights) == []
    assert heights == []


# Úkol 4.

def sum_missing_numbers(numbers, n):
    remaining = n
    sum_ = 0
    position = 0
    current_num = 1
    while remaining > 0:

        if position < len(numbers) and numbers[position] == current_num:
            position += 1

        else:
            remaining -= 1
            sum_ += current_num
        current_num += 1
    return sum_


def test_sum_missing_numbers():
    numbers = [1, 3, 7, 10, 14]
    assert sum_missing_numbers(numbers, 5) == 25
    assert numbers == [1, 3, 7, 10, 14]

    numbers = [1, 2, 3, 5, 6, 7, 8, 11]
    assert sum_missing_numbers(numbers, 1) == 4
    assert numbers == [1, 2, 3, 5, 6, 7, 8, 11]

    numbers = [1, 2, 3, 5, 6, 7, 8, 11]
    assert sum_missing_numbers(numbers, 2) == 13
    assert numbers == [1, 2, 3, 5, 6, 7, 8, 11]

    numbers = [1, 2, 3, 5, 6, 7, 8, 11]
    assert sum_missing_numbers(numbers, 3) == 23
    assert numbers == [1, 2, 3, 5, 6, 7, 8, 11]

    numbers = [1, 2, 3, 5, 6, 7, 8, 11]
    assert sum_missing_numbers(numbers, 4) == 35
    assert numbers == [1, 2, 3, 5, 6, 7, 8, 11]

    numbers = [10, 20, 30]
    assert sum_missing_numbers(numbers, 17) == 161
    assert numbers == [10, 20, 30]

    numbers = []
    assert sum_missing_numbers(numbers, 7) == 28
    assert numbers == []


if __name__ == '__main__':
    test_filter_bad_primes()
    test_largest_elf_island()
    test_flats()
    test_sum_missing_numbers()
