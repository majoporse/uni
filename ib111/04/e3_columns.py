# Implementujte proceduru, která v parametru dostane:
#
#  • neprázdný dvourozměrný seznam (ve tvaru obdélníku: délky všech
#    vnitřních seznamů jsou stejné), který reprezentuje tabulku, ve
#    které vnitřní seznamy tvoří řádky, a dále
#  • seznam dvojic čísel sloupců (můžete se spolehnou, že daná čísla
#    vždy označují existující sloupce dané tabulky), které v dané
#    tabulce vymění.
#
# Například po použití této procedury se seznamem dvojic sloupců
# ‹[(1, 2)]› na seznam ‹[[1, 2, 3], [4, 5, 6], [7, 8, 9]]› tento
# změní na ‹[[1, 3, 2], [4, 6, 5], [7, 9, 8]]›.

def swap_columns(table, cols_to_swap):
    pass


def main():
    check_swap_columns([[1, 2, 3], [4, 5, 6], [7, 8, 9]], [(1, 2)],
                       [[1, 3, 2], [4, 6, 5], [7, 9, 8]])
    check_swap_columns([[1, 2]], [(0, 0)], [[1, 2]])
    check_swap_columns([["a", "b", "c"], ["d", "e", "f"]], [(1, 0)],
                       [["b", "a", "c"], ["e", "d", "f"]])
    check_swap_columns([[1, 2, 3, 10], [4, 5, 6, 11], [7, 8, 9, 12]],
                       [(1, 2), (0, 3)], [[10, 3, 2, 1], [11, 6, 5, 4],
                                          [12, 9, 8, 7]])
    check_swap_columns([[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5]],
                       [(0, 1), (3, 2), (4, 5)], [[1, 0, 3, 2, 5, 4],
                                                  [1, 0, 3, 2, 5, 4]])
    check_swap_columns([["a", "b", "c"], ["d", "e", "f"]], [(0, 1), (1, 2)],
                       [["b", "c", "a"], ["e", "f", "d"]])


def check_swap_columns(table, cols_to_swap, expected_result):
    swap_columns(table, cols_to_swap)
    assert table == expected_result


if __name__ == '__main__':
    main()
