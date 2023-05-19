from typing import List, Tuple
import os
import csv

# Napište podprogram ‹names_sorted›, který ze souboru s cestou
# ‹filename› načte jména, seřadí je primárně podle příjmení,
# sekundárně podle křestního jména a seřazená jména vrátí jako
# seznam řetězců.
#
# Soubor je ve formátu CSV vždy se dvěma sloupci: jméno a příjmení.
# Soubor může obsahovat prázdné řádky – tyto ignorujte.

def names_sorted(filename: str) -> List[str]:
    result = []
    with open(filename, "r", encoding = "utf-8") as file:
        csv_reader = csv.reader(file)
        
        for line in csv_reader:
            if len(line) == 2:
                result.append((line[1], line[0]))        
    result.sort()
    return [line[1] + ' ' +line[0] for line in result]

# Dále napište proceduru ‹format_names›, která uloží jména ze
# souboru s cestou ‹source› seřazená primárně podle příjmení,
# sekundárně podle křestního jména do souboru s cestou ‹dest›.
# Vstupní i výstupní soubor budou ve formátu CSV.

def format_names(source: str, dest: str) -> None:
    result = []
    with open(source, "r", encoding = "utf-8") as file:
        csv_reader = csv.reader(file)
        
        for line in csv_reader:
            if len(line) == 2:
                result.append((line[1], line[0]))        
    result.sort()
    with open(dest,"w", encoding = 'utf-8') as file:
        csv_writer = csv.writer(file)
        for a in result:
            csv_writer.writerow([(a[1],a[0])])

def main() -> None:
    test_simple = ('zz.names_simple.csv',
                   ['Klára Kočí', 'Bedřich Novák', 'Jan Novák'])

    test_long = ('zz.names_long.csv',
                 ['Král Beran', 'Květoslav Beran', 'Jaromír Král',
                  'Marián Král', 'Zdeněk Král', 'Havel Kubík',
                  'Vendelín Kubík', 'Jaromír Málek', 'Zdeněk Němec',
                  'Havel Rýpal'])

    assert names_sorted(test_simple[0]) == test_simple[1]
    assert names_sorted(test_long[0]) == test_long[1]

    assert test_format(test_simple)
    assert test_format(test_long)


def test_format(test: Tuple[str, List[str]]) -> bool:
    dest = 'names-testfile.csv'
    if os.path.exists(dest):
        os.remove(dest)

    expected = []
    for name in test[1]:
        expected.append(name.replace(' ', ','))

    format_names(test[0], dest)
    assert os.path.exists(dest)

    with open(dest, 'r', encoding='UTF8') as result:
        lines = [line.rstrip() for line in result]
        assert lines == expected

    if os.path.exists(dest):
        os.remove(dest)

    return True


if __name__ == '__main__':
    main()
