import re
import os
import zipfile
import shutil
from typing import List


# Implementujte podprogram ‹count_words›, který vrátí počet slov ze
# souboru s cestou ‹path›, které splňují vzor ‹pattern› zadaný jako
# regulární výraz. Při zpracování ignorujte interpunkci (pro
# jednoduchost pouze tečky a čárky).

def count_words(path: str, pattern: str) -> int:
    with open(path) as file1:
        file = file1.read()
        file = file.replace(".", "")
        file = file.replace(',', '')
        count = 0
        word_list = file.split()
        for word in word_list:
            if re.search(pattern, word):
                count += 1
    return count


# Dále implementujte proceduru ‹delete_lines›, která:
#
#  1. načte soubor z cesty ‹path›,
#  2. smaže všechny řádky, které obsahují alespoň jedno slovo
#     splňující nějaký ze vzorů ‹patterns›,
#  3. výsledek zapíše do souboru s cestou ‹dest›.
#
# Opět při zpracování ignorujte interpunkci. Prázdné řádky
# zachovejte. Soubor zpracovávejte po řádcích (nenačítejte jej do
# paměti celý najednou).

def delete_lines(path: str, dest: str, patterns: List[str]) -> None:
    with open(path, "r") as file1:
        with open(dest, "w") as file:

            for line in file1:
                line = str(line)
                clean_line = line.replace(".", "")
                clean_line = clean_line.replace(',', '')
                line_list = clean_line.split()
                remove = False
                for word in line_list:
                    for pattern in patterns:
                        if re.search(pattern, word):
                            remove = True
                            break
                    if remove:
                        break
                if not remove:
                    file.write(line)


def main() -> None:
    tests_count_words()
    tests_delete_lines()


def tests_count_words() -> None:
    assert count_words('zz.lorem.txt', '(?i)lorem') == 4
    assert count_words('zz.lorem.txt', 'Quisque') == 5
    assert count_words('zz.lorem.txt', 'ius$') == 3
    assert count_words('zz.lorem.txt', 'tus$') == 9
    assert count_words('zz.lorem.txt', 'python') == 0
    assert count_words('zz.lorem.txt', 'f[a-z]*s') == 15
    assert count_words('zz.lorem.txt', 'C[a-z]*s') == 2
    assert count_words('zz.lorem.txt', 'm[a-z]*s') == 34


def test_delete_lines(source: str, expected: str, patterns: List[str]) -> None:
    assert os.path.exists(source)
    testfile = 'delete-lines-test.txt'
    shutil.copyfile(source, testfile)

    testdst = 'delete-lines-result.txt'
    delete_lines(testfile, testdst, patterns)
    assert os.path.exists(testdst)

    assert os.path.exists(expected)
    with open(testdst) as f_testdst, open(expected) as f_expected:
        assert f_testdst.read() == f_expected.read(), \
            f"your result is in {testdst} and expected result in {expected}"

    assert os.path.exists(testfile)
    os.remove(testfile)
    os.remove(testdst)


def tests_delete_lines() -> None:
    if os.path.exists('zx.patterns'):
        shutil.rmtree('zx.patterns')
    with zipfile.ZipFile('zx.patterns.zip', 'r') as zip_ref:
        zip_ref.extractall()

    test_delete_lines('zz.lorem.txt',
                      'zx.patterns/delete-lines-result-1.txt',
                      ['(?i)lorem'])
    test_delete_lines('zz.lorem.txt',
                      'zz.lorem.txt',
                      ['python'])
    test_delete_lines('zz.lorem.txt',
                      'zx.patterns/delete-lines-result-1.txt',
                      ['test', '(?i)lorem', 'python', 'del*ete'])
    test_delete_lines('zz.lorem.txt',
                      'zx.patterns/delete-lines-result-2.txt',
                      ['tus$', 'm[a-z]*s', 'del*ete', 'am$', '^am'])
    test_delete_lines('zz.lorem.txt',
                      'zx.patterns/delete-lines-result-3.txt',
                      ['Quisque', '(?i)lorem'])
    if os.path.exists('zx.patterns'):
        shutil.rmtree('zx.patterns')


if __name__ == '__main__':
    main()
