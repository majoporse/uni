import os
import shutil
import zipfile
from typing import List


# Implementujte proceduru ‹split_file›, která rozdělí textový soubor
# s cestou ‹path› na menší soubory tak, že každý soubor bude mít
# ‹max_lines› řádků (poslední soubor může mít řádků méně).

# Vytvořené soubory pojmenujte tak, že k cestě originálního soubor
# přidáte pořadové číslo oddělené podtržítkem. Příponu ‹.txt›
# zachovejte. Například pro vstupní soubor ‹data/text.txt› ukládejte
# výstup do souborů ‹data/text_1.txt›, ‹data/text_2.txt› atd. Jeden
# výstupní soubor vytvořte i v případě, že je vstup prázdný.
# Procedura vrátí seznam vytvořených souborů v pořadí od prvního.

def split_file(path: str, max_lines: int) -> List[str]:
    with open(path) as file:
        current = ''
        x = 1
        for (index, line) in enumerate(file):
            if index > 0 and index % max_lines == 0:
                with open(f'{path[:-4]}_{x}.txt', "w") as file2:
                    x += 1
                    file2.write(current)
                    current = ''
            current += line

        if current != '' or x == 1:
            with open(f'{path[:-4]}_{x}.txt', "w") as file2:
                x += 1
                file2.write(current)

        return [f'{path[:-4]}_{y}.txt' for y in range(1, x)]


def main() -> None:
    if os.path.exists('zt.split'):
        shutil.rmtree('zt.split')
    with zipfile.ZipFile('zx.split.zip', 'r') as zip_ref:
        zip_ref.extractall()

    test_split('zz.lorem', 10, 5)
    test_split('zz.lorem', 19, 3)
    test_split('zz.lorem', 75, 1)
    test_split('zz.empty', 5, 1)
    test_split('zz.lorem', 3, 17)


def test_split(source: str, size: int, expected: int) -> None:
    assert os.path.exists(source + '.txt')
    testfile = 'split.txt'

    if os.path.exists('scratch'):
        shutil.rmtree('scratch')
    os.mkdir('scratch')
    os.chdir('scratch')
    shutil.copyfile('../' + source + '.txt', testfile)

    result = split_file(testfile, size)
    assert len(result) == expected

    for i, res in enumerate(result):
        name = 'split_' + str(i + 1) + '.txt'
        expect = source + str(size) + str(i + 1) + '.txt'
        assert os.path.basename(res) == name, f"{res} ~ {name}"
        assert os.path.exists(res), f"file {res} does not exist"
        with open(res) as f_res:
            with open('../zt.split/' + expect) as f_expect:
                assert f_res.read() == f_expect.read()

    os.chdir('..')


if __name__ == '__main__':
    main()
