from typing import List, Tuple

# «Flood fill» je algoritmus z oblasti rastrové grafiky, který
# vyplní souvislou jednobarevnou plochy nějakou jinou barvou.
# Postupuje tak, že nejdříve na novou barvu obarví pozici, na které
# začíná, dále se pokusí obarvit její sousedy (pozice jiné, než
# cílové barvy se neobarvují), a podobně pokračuje se sousedy těchto
# sousedů, atd. Zastaví se, dojde-li na okraj obrázku, nebo narazí
# na pixel, který nemá žádné nové stejnobarevné sousedy.

# Napište proceduru, která na vstupu dostane plochu reprezentovanou
# obdélníkovým seznamem seznamů (délky všech vnitřních seznamů jsou
# stejné), počáteční pozici (je zaručeno, že se bude jednat o platné
# souřadnice), a cílovou barvu, na kterou mají být vybrané pozice
# přebarveny.

Position = Tuple[int, int]
Area = List[List[int]]


def check_position(x: int, y: int, area: Area, colour: int) -> List[int]:
    result: List[int] = []

    if x + 1 < len(area):
        if area[x + 1][y] == colour:
            result += (x + 1, y)
    if x - 1 >= 0:
        if area[x - 1][y] == colour:
            result += (x - 1, y)
    if y + 1 < len(area[0]):
        if area[x][y + 1] == colour:
            result += (x, y + 1)
    if y - 1 >= 0:
        if area[x][y - 1] == colour:
            result += (x, y - 1)
    return result


def flood_fill(area: Area, start: Position, colour: int) -> None:
    x, y = start
    start_colour = area[x][y]
    stack_x: List[int] = []
    stack_y: List[int] = []
    moves = [1]

    while True:
        area[x][y] = colour
        moves = check_position(x, y, area, start_colour)

        if stack_x == [] and stack_y == [] and moves == []:
            break

        if len(moves) == 0:
            x = stack_x.pop()
            y = stack_y.pop()

        else:
            stack_x.append(x)
            stack_y.append(y)
            x = moves[0]
            y = moves[1]


def main() -> None:
    check_flood([[0]], (0, 0), 1, [[1]])
    check_flood([[0, 0, 1, 1, 1, 0]], (0, 3), 2, [[0, 0, 2, 2, 2, 0]])
    check_flood([[0, 0, 1, 1, 1, 0]], (0, 0), 2, [[2, 2, 1, 1, 1, 0]])
    check_flood([[1, 2, 3, 4],
                 [1, 1, 1, 1],
                 [2, 2, 2, 1],
                 [5, 5, 1, 1]],
                (1, 1), 8,
                [[8, 2, 3, 4],
                 [8, 8, 8, 8],
                 [2, 2, 2, 8],
                 [5, 5, 8, 8]])

    check_flood([[1, 2, 3, 4],
                 [1, 1, 1, 1],
                 [2, 2, 2, 1],
                 [1, 5, 1, 1]],
                (1, 1), 8,
                [[8, 2, 3, 4],
                 [8, 8, 8, 8],
                 [2, 2, 2, 8],
                 [1, 5, 8, 8]])


def check_flood(area: Area, start: Position,
                new_colour: int, expected_result: Area) -> None:
    flood_fill(area, start, new_colour)
    assert area == expected_result


if __name__ == '__main__':
    main()
