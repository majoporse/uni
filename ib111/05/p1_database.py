from typing import List, Tuple, Optional

# V této úloze budete pracovat s databázovou tabulkou. Tabulka je
# dvojice složená z «hlavičky» a seznamu «záznamů». «Hlavička»
# obsahuje seznam názvů sloupců. Jeden záznam je tvořen seznamem
# hodnot pro jednotlivé sloupce tabulky (pro jednoduchost uvažujeme
# jenom hodnoty typu řetězec). Ne všechny hodnoty v záznamech musí
# být vyplněny – v tom případě mají hodnotu ‹None›.


# Vaším úkolem bude nyní otypovat a implementovat následující
# funkce. Funkce ‹header› vrátí hlavičku tabulky ‹table›.
datatable = Tuple[List[str], List[List[Optional[str]]]]


def get_header(table: datatable) -> List[str]:
    return table[0]


# Funkce ‹records› vrátí seznam záznamů z tabulky ‹table›.


def get_records(table: datatable) -> List[List[Optional[str]]]:
    return table[1]


# Procedura ‹add_record› přidá záznam ‹record› na konec tabulky
# ‹table›. Můžete předpokládat, že záznam ‹record› bude mít stejný
# počet sloupců jako tabulka.

def add_record(record: List[Optional[str]], table: datatable) -> datatable:
    records = table[1]
    records.append(record)
    return table

# Predikát ‹is_complete› je pravdivý, neobsahuje-li tabulka ‹table›
# žádnou hodnotu ‹None›.


def is_complete(table: datatable) -> bool:
    for i in range(len(table)):
        if table[i] == []:
            continue
        for j in range(len(table[i])):
            if table[i][j] == []:
                continue
            else:
                for k in range(len(table[i][j])):
                    if table[i][j][k] is None:
                        return False
    return True

# Funkce ‹index_of_column› vrátí index sloupce se jménem ‹name›.
# Můžete předpokládat, že sloupec s jménem ‹name› se v tabulce
# nachází. První sloupec má index 0.


def index_of_column(name: str, header: List[str]) -> int:
    for i in range(len(header)):
        if name == header[i]:
            position = i
    return position

# Funkce ‹values› vrátí seznam platných hodnot (tzn. takových, které
# nejsou ‹None›) v sloupci se jménem ‹name›. Můžete předpokládat, že
# sloupec se jménem ‹name› se v tabulce nachází.


def values(name: str, table: datatable) -> List[str]:
    names: List[str] = []
    lower_name = name.lower()
    upper_name = name.upper()
    for j in range(len(table[1])):
        if table[1][j] == []:
            continue
        else:
            for k in range(len(table[1][j])):
                current = table[1][j][k]
                if current is not None:
                    if lower_name in current or upper_name in current:
                        names.append(current)
    return names

# Procedura ‹drop_column› smaže sloupec se jménem ‹name› z tabulky
# ‹table›. Můžete předpokládat, že sloupec se jménem ‹name› se
# v tabulce nachází.


def drop_column(name: str, table: datatable) -> None:
    for i in range(len(table[0])):
        if table[0][i] == name:
            position = i
    table[0].pop(position)
    for i in range(len(table[1])):
        table[1][i].pop(position)


def main() -> None:
    from copy import deepcopy
    test_table = Tuple[List[str], List[List[Optional[str]]]]

    empty: test_table = (["A", "B", "C", "D"], [])
    table: test_table = (["A", "B", "C"],
                         [["a1", "b1", None], ["a2", "b2", "c2"],
                          ["a3", None, "c3"]])
    complete: test_table = (["A", "B", "C"],
                            [["a1", "b1", "c1"], ["a2", "b2", "c2"]])

    # header test
    assert get_header(empty) == empty[0]
    assert get_header(table) == table[0]

    # records test
    assert get_records(empty) == empty[1]
    assert get_records(table) == table[1]

    # add_record test
    empty_copy = deepcopy(empty)
    add_record(["a", "b", "c", "d"], empty_copy)
    assert empty_copy == (['A', 'B', 'C', 'D'], [['a', 'b', 'c', 'd']])

    table_copy = deepcopy(table)
    add_record(["a4", None, None], table_copy)
    assert table_copy == (['A', 'B', 'C'],
                          [['a1', 'b1', None], ['a2', 'b2', 'c2'],
                           ['a3', None, 'c3'], ['a4', None, None]])

    # is_complete test
    assert is_complete(empty)
    assert not is_complete(table)
    assert is_complete(complete)

    # index_of_column test
    assert index_of_column("A", table[0]) == 0
    assert index_of_column("B", table[0]) == 1
    assert index_of_column("C", table[0]) == 2
    assert index_of_column("B", empty[0]) == 1
    assert index_of_column("D", empty[0]) == 3

    # values test
    assert values("A", table) == ["a1", "a2", "a3"]
    assert values("B", table) == ["b1", "b2"]
    assert values("C", table) == ["c2", "c3"]
    assert values("B", empty) == []

    # drop_column test
    table_copy = deepcopy(table)
    drop_column("A", table_copy)
    assert table_copy == (['B', 'C'],
                          [['b1', None], ['b2', 'c2'], [None, 'c3']])

    table_copy = deepcopy(table)
    drop_column("B", table_copy)
    assert table_copy == (['A', 'C'],
                          [['a1', None], ['a2', 'c2'], ['a3', 'c3']])

    drop_column("D", empty)
    assert empty == (['A', 'B', 'C'], [])


if __name__ == "__main__":
    main()
