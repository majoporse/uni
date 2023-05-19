from typing import List, Tuple
import os
import zipfile
import shutil


# Implementujte podprogram ‹bounds›, který vrátí minimální a
# maximální hodnotu v sloupci s indexem ‹column› v tabulce ze
# souboru s cestou ‹path›. Sloupce jsou indexovány od 0. Tabulka je
# zadána po řádcích kde hodnoty jsou odděleny mezerami. Například
# volání ‹bounds› s následující tabulkou pro sloupec 1 vrátí dvojici
# ‹(4, 9)›:
#
#     5 9 2 8
#     9 4 7 3
#     3 8 6 5

def bounds(path: str, column: int) -> Tuple[int, int]:
    pass


# Dále implementujte podprogram ‹min_column›, který spočte index
# sloupce, kterého hodnoty jsou v součtu nejmenší. Pro předcházející
# příklad je to sloupec 2.

def min_column(path: str) -> int:
    pass


def main() -> None:
    test_folder = 'zt.spreadsheet'
    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)
    with zipfile.ZipFile('zz.spreadsheet.zip', 'r') as zip_ref:
        zip_ref.extractall()

    expected = [(3, 9), (4, 9), (2, 7), (3, 8)]
    test_bounds(test_folder + '/sheet-1.txt', expected)

    expected = [(7, 83), (8, 82), (28, 98), (9, 81), (0, 89), (6, 99)]
    test_bounds(os.path.join(test_folder, 'sheet-2.txt'), expected)

    expected = [(131, 4228), (43, 4490), (47, 5525), (155, 4890), (64, 3653),
                (78, 3314), (165, 3794), (96, 4842), (54, 3259), (75, 4040),
                (72, 4825), (138, 5070), (60, 5173), (51, 4888), (79, 4813),
                (77, 5594)]
    test_bounds(os.path.join(test_folder, 'sheet-3.txt'), expected)

    assert min_column(os.path.join(test_folder, 'sheet-1.txt')) == 2
    assert min_column(os.path.join(test_folder, 'sheet-2.txt')) == 4
    assert min_column(os.path.join(test_folder, 'sheet-3.txt')) == 5

    if os.path.exists(test_folder):
        shutil.rmtree(test_folder)


def test_bounds(path: str, expected: List[Tuple[int, int]]) -> None:
    for idx, val in enumerate(expected):
        assert bounds(path, idx) == val


if __name__ == "__main__":
    main()
