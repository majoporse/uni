from typing import List, Tuple, Optional, Set
from math import inf

Array = List[List[int]]


class Clue:
    def __init__(self, total: int, position: Tuple[int, int],
                 is_row: bool, length: int):
        self.total = total
        self.position = position
        self.is_row = is_row
        self.length = length


class Kakuro:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.array = [[-1 for _ in range(width)] for _ in range(height)]
        self.clues: List[Clue] = []

    def set(self, x: int, y: int, value: int) -> None:
        self.array[y][x] = value

    def show_board(self) -> None:
        result = ''
        for line in self.array:
            new_line = ['\\' if a == -1 else '.'
                        if a == 0 else str(a) for a in line]
            result += ' '.join(new_line) + '\n'
        print(result[:-1])

    def save(self, filename: str) -> None:
        result: List[List[str]] = []
        array = self.array
        for line in array:
            new_line = ['\\' if a == -1 else '.'
                        if a == 0 else str(a) for a in line]
            result.append(new_line)

        for clue in self.clues:
            x, y = clue.position
            res = result[y][x]

            new_clue = res + str(clue.total) if clue.is_row else \
                str(clue.total) + res
            result[y][x] = new_clue

        with open(filename, 'w') as file:
            for lines in result:
                file.write(' '.join(lines) + '\n')

    def is_valid(self) -> bool:
        array = self.array
        for clue in self.clues:
            x, y = clue.position
            section = [num for num in
                       get_section(array, (x, y), clue.is_row) if num != 0]
            if sum(section) > clue.total or \
               len(set(section)) < len(section):
                return False
        return True

    def check_sum(self) -> bool:
        for clue in self.clues:
            if sum(get_section(self.array, clue.position, clue.is_row)) \
               != clue.total:
                return False
        return True

    def pick_clue(self) -> Optional[Clue]:
        best_empty = inf
        best_suited: List[Clue] = []
        for clue in self.clues:
            count = get_section(self.array, clue.position,
                                clue.is_row).count(0)
            if count > 0:
                if count < best_empty:
                    best_suited = []
                    best_empty = count
                if count == best_empty:
                    best_suited.append(clue)
        best_suited.sort(key=lambda x: x.position)
        if best_empty != inf:
            return best_suited[0]
        return None

    def solve(self) -> bool:
        return self.solve_rec(self.array)

    def solve_rec(self, old_array: Array) -> bool:
        clue = self.pick_clue()
        if clue is None:
            return self.check_sum() and self.is_valid()

        for cell in cells_from_partial(
                clue.total, get_section(old_array,
                                        clue.position, clue.is_row)):
            self.array = [a.copy() for a in old_array]
            insert_to_array(self.array, clue.position, cell, clue.is_row)
            if self.solve_rec(self.array):
                return True
        self.array = old_array
        return False


def get_section(array: Array, position: Tuple[int, int],
                is_row: bool) -> List[int]:
    x, y = position
    length = []
    bound = len(array[y]) if is_row else len(array)
    i = x + 1 if is_row else y + 1
    while i < bound and (array[y][i] if is_row else array[i][x]) != -1:
        length.append(array[y][i] if is_row else array[i][x])
        i += 1
    return length


def load_kakuro(filename: str) -> Kakuro:
    array = []
    clues = []
    with open(filename) as file:
        lines = file.readlines()
        for i in range(len(lines)):
            line = []
            for j, elem in enumerate(lines[i].split()):
                if elem == '.':
                    line.append(0)
                elif '\\' in elem:
                    for pos, num in enumerate(elem.split('\\')):
                        if num != '':
                            clue = Clue(int(num), (j, i), pos == 1, 0)
                            clues.append(clue)
                    line.append(-1)
                else:
                    line.append(int(elem))
            array.append(line)

    kakuro = Kakuro(len(array[0]), len(array))
    kakuro.array = array
    for clue in clues:
        kakuro.clues.append(clue)
        clue.length = len(get_section(kakuro.array,
                                      clue.position, clue.is_row))
    return kakuro


def insert_to_array(array: Array, position: Tuple[int, int],
                    cell: List[int], is_row: bool) -> None:
    x, y = position
    for i, num in enumerate(cell):
        if is_row:
            array[y][x + i + 1] = num
        else:
            array[y + i + 1][x] = num


def cells_from_empty(total: int, length: int) -> List[List[int]]:
    if total <= length * 9:           # maximum is length*9
        return cells_rec([], [0 for _ in range(length)], 0, total, set())
    else:
        return []


def cells_rec(result: Array, current: List[int],
              index: int, total: int, used: Set[int]) -> List[List[int]]:

    if index == len(current) and sum(current) == total:
        result.append(current)
        return result

    if index == len(current) or sum(current) > total:
        return result

    if current[index] > 0:
        return cells_rec(result, current, index + 1, total, used)

    else:
        for i in range(1, 10):
            if i not in used:
                new = current.copy()
                new[index] = i
                cells_rec(result, new, index + 1, total, used | {i})

    return result


def cells_from_partial(total: int, partial: List[int]) -> List[List[int]]:
    return cells_rec([], partial, 0, total,  set(partial))


# --- Tests ---

# Note: If there is a file with the following name in the current working
# directory, running these tests will overwrite that file!

TEST_FILENAME = "_ib111_tmp_file_"

EXAMPLE = ("\\   11\\  8\\     \\   \\   7\\ 16\\\n"
           "\\16   .   .   11\\   \\4   .   .\n"
           "\\7    .   .     .  7\\13  .   .\n"
           "\\   15\\ 21\\12   .   .    .   .\n"
           "\\12   .   .     .   .   4\\  6\\\n"
           "\\13   .   .     \\6  .    .   .\n"
           "\\17   .   .     \\   \\6   .   .\n")

EXAMPLE1 = ("\\   9\\   14\\\n"
            "\\8  .     . \n"
            "\\13 .     .")


def write_example(filename: str) -> None:
    with open(filename, "w") as file:
        file.write(EXAMPLE)


def example() -> Kakuro:
    write_example(TEST_FILENAME)
    return load_kakuro(TEST_FILENAME)


def test_1() -> None:
    kakuro = example()
    assert kakuro.width == 7
    assert kakuro.height == 7
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 0, 0, -1, -1, 0, 0],
        [-1, 0, 0, 0, -1, 0, 0],
        [-1, -1, -1, 0, 0, 0, 0],
        [-1, 0, 0, 0, 0, -1, -1],
        [-1, 0, 0, -1, 0, 0, 0],
        [-1, 0, 0, -1, -1, 0, 0],
    ]
    clue_set = {(clue.total, clue.position, clue.is_row, clue.length)
                for clue in kakuro.clues}
    assert clue_set == {
        (11, (1, 0), False, 2),
        (8, (2, 0), False, 2),
        (7, (5, 0), False, 3),
        (16, (6, 0), False, 3),
        (16, (0, 1), True, 2),
        (11, (3, 1), False, 3),
        (4, (4, 1), True, 2),
        (7, (0, 2), True, 3),
        (7, (4, 2), False, 3),
        (13, (4, 2), True, 2),
        (15, (1, 3), False, 3),
        (21, (2, 3), False, 3),
        (12, (2, 3), True, 4),
        (12, (0, 4), True, 4),
        (4, (5, 4), False, 2),
        (6, (6, 4), False, 2),
        (13, (0, 5), True, 2),
        (6, (3, 5), True, 3),
        (17, (0, 6), True, 2),
        (6, (4, 6), True, 2)}


def test_2() -> None:
    kakuro = example()

    print("show_board result:")
    kakuro.show_board()
    print("---")

    print("save result:")
    kakuro.save(TEST_FILENAME)
    with open(TEST_FILENAME) as file:
        print(file.read(), end="")
    print("---")


def test_3() -> None:
    kakuro = example()
    assert kakuro.is_valid()

    kakuro.set(2, 1, 9)
    assert not kakuro.is_valid()

    kakuro.set(2, 1, 0)
    assert kakuro.is_valid()

    kakuro.set(1, 2, 1)
    kakuro.set(2, 2, 1)
    assert not kakuro.is_valid()

    kakuro.set(1, 2, 0)
    kakuro.set(2, 2, 0)
    assert kakuro.is_valid()

    kakuro.set(5, 5, 4)
    assert kakuro.is_valid()


def test_4() -> None:
    assert cells_from_empty(13, 2) \
        == [[4, 9], [5, 8], [6, 7], [7, 6], [8, 5], [9, 4]]

    assert cells_from_partial(12, [0, 0, 6, 0]) \
        == [[1, 2, 6, 3], [1, 3, 6, 2], [2, 1, 6, 3],
            [2, 3, 6, 1], [3, 1, 6, 2], [3, 2, 6, 1]]


def test_5() -> None:
    kakuro = example()
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 16
    assert clue.position == (0, 1)
    assert clue.is_row
    assert clue.length == 2

    kakuro.set(6, 5, 1)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (6, 4)
    assert not clue.is_row
    assert clue.length == 2

    kakuro.set(6, 6, 5)
    clue = kakuro.pick_clue()

    assert clue is not None
    assert clue.total == 6
    assert clue.position == (4, 6)
    assert clue.is_row
    assert clue.length == 2


def test_6() -> None:
    kakuro = example()
    kakuro.solve()
    assert kakuro.array == [
        [-1, -1, -1, -1, -1, -1, -1],
        [-1, 9, 7, -1, -1, 1, 3],
        [-1, 2, 1,  4, -1, 4, 9],
        [-1, -1, -1, 5, 1, 2, 4],
        [-1, 1, 5, 2, 4, -1, -1],
        [-1, 6, 7, -1, 2, 3,  1],
        [-1, 8, 9, -1, -1, 1, 5],
    ]


if __name__ == '__main__':
    test_1()
    # uncomment to visually check the results:
    test_2()
    test_3()
    test_4()
    test_5()
    test_6()
