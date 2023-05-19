from typing import List, Optional
# Opět je Vašim úkolem do již hotového programu doplnit typové
# anotace tak, aby prošel kontrolou nástrojem ‹mypy›. Zároveň si zde
# můžete procvičit porozumění kódu (budete-li vědět, co která funkce
# dělá, typové anotace se Vám budou vymýšlet lépe).

Grid = List[List[int]]


def cell_value(grid: Grid, x: int, y: int) -> int:
    if 0 <= x < len(grid) and 0 <= y < len(grid):
        return grid[x][y]
    return 0


def live_neighbour_count(grid: Grid, x: int, y: int) -> int:
    assert x < len(grid) and y < len(grid)

    res = 0
    for row in range(x - 1, x + 2):
        for col in range(y - 1, y + 2):
            res += cell_value(grid, row, col)
    return res - grid[x][y]


def next_value(grid : Grid, x: int, y: int) -> int:
    assert x < len(grid) and y < len(grid)

    live_neighbours = live_neighbour_count(grid, x, y)

    if grid[x][y] == 0:
        return 1 if live_neighbours == 3 else 0

    if live_neighbours == 2 or live_neighbours == 3:
        return 1
    return 0


def step(grid: Grid) -> Grid:
    assert len(grid) > 0

    res: Grid = []
    for i in range(len(grid)):
        res.append([])
        for j in range(len(grid[0])):
            res[i].append(next_value(grid, i, j))
    return res


def life(grid: Grid, count: int) -> Grid:
    assert len(grid) > 0
    assert count >= 0

    world = [curr[:] for curr in grid]

    for _ in range(count):
        next_step = step(world)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                world[i][j] = next_step[i][j]

    return world


def main() -> None:
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 1) \
        == [[1, 0, 1], [1, 0, 0], [1, 0, 1]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 2) \
        == [[0, 1, 0], [1, 0, 0], [0, 1, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 3) \
        == [[0, 0, 0], [1, 1, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 4) \
        == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 5) \
        == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    assert life([[0, 1, 1],
                 [1, 1, 1],
                 [0, 1, 1]], 0) \
        == [[0, 1, 1], [1, 1, 1], [0, 1, 1]]

    assert life([[1, 1],
                 [1, 1]], 3) \
        == [[1, 1], [1, 1]]
    assert life([[1, 1],
                 [0, 1]], 1) \
        == [[1, 1], [1, 1]]

    assert life([[1, 0, 1, 0],
                 [0, 1, 0, 1],
                 [1, 0, 0, 1],
                 [0, 0, 1, 1]], 5) \
        == [[0, 0, 1, 0],
            [1, 0, 0, 1],
            [1, 1, 0, 1],
            [1, 1, 0, 0]]


if __name__ == "__main__":
    main()
