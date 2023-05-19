from typing import Tuple, Optional

# V této úloze budeme implementovat simulaci procházky po 2D mřížce.
# Pro reprezentaci pozice v mřížce budeme používat uspořádanou
# dvojici ⟦(x, y)⟧.

Position = Tuple[int, int]

# Cesta procházky je zadaná jako řetězec ‹path›, který se skládá
# z příkazů ‹←› / ‹→› pro pohyb doleva a doprava (po ose ⟦x⟧) a ‹↑›
# / ‹↓› pro pohyb nahoru a dolů (po ose ⟦y⟧). Souřadnice rostou ve
# směru doprava na ⟦x⟧-ové ose a nahoru na ⟦y⟧-ové ose.

# Napište čistou funkci ‹walk›, která vrátí finální pozici pro
# procházku ‹path› z počáteční pozice ‹start›.


def walk(path: str, start: Position) -> Position:
    x,y = start
    for direction in path:
        if direction == '←':
            x -= 1
        elif direction == '→':
            x += 1
        elif direction == '↑':
            y += 1
        elif direction == '↓':
            y -= 1
    return (x,y)

# Dále napište čistou funkci ‹meet›, která vrátí pro dvojici cest
# ‹path_1›, ‹path_2› a počátků ‹start_1› a ‹start_2›, první pozici
# na které se procházky potkají. Procházky se provádí synchronně,
# tj. kroky se vykonávají najednou pro obě procházky. Pokud se
# procházky nepotkají, funkce vrátí ‹None›.

def meet(path_1: str, path_2: str, start_1: Position,
         start_2: Position) -> Optional[Position]:
    pos1 = walk(path_1,start_1)
    pos2 = walk(path_2,start_2)
    return  pos1 if pos1 == pos2 else None 


def main() -> None:
    assert walk("→→", (0, 0)) == (2, 0)
    assert walk("←↑→↓", (0, 0)) == (0, 0)
    assert walk("←←↑↑→↑↑→→↓→→→↑↑", (2, 3)) == (6, 8)
    assert walk("↑←↑→↑→", (-1, -3)) == (0, 0)

    assert meet("→→", "←←", (-1, 0), (1, 0)) == (0, 0)
    assert meet("←", "↓", (1, 0), (0, 1)) == (0, 0)

    assert meet("←↑→↓", "→↓←↑", (1, 0), (0, 1)) is None
    assert meet("↓↓↓↓↓↓", "↓↓↓↓↓↓", (1, 0), (0, 0)) is None

    assert meet("→↓→↓→↑←←→↓↓→", "↑→→↓→↓→↓→↑→←←",
                (2, 2), (-1, 1)) == (4, 0)


if __name__ == '__main__':
    main()
