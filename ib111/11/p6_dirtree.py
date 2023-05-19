from typing import List
import os
import shutil


# V této úloze budete pracovat s reprezentací adresářové struktury.
# Každý adresář má své jméno ‹name› a seznam podadresářů ‹dirs›.

class Directory:
    def __init__(self, name: str, dirs: List['Directory']):
        self.name = name
        self.dirs = dirs


# Implementujte proceduru ‹create_dirtree›, která v souborovém
# systému v adresáři s cestou ‹path› vytvoří adresářovou strukturu
# podle zadané struktury ‹tree›.

def create_dirtree(path: str, tree: Directory) -> None:
    pass


# Dále implementujte podprogram ‹load_dirtree›, který načte
# adresářovou hierarchii ze souborového systému do stromové
# struktury popsané třídou ‹Directory›. Kořenem výsledné struktury
# bude adresář s cestou ‹path›.

def load_dirtree(path: str) -> Directory:
    pass


def main() -> None:
    test_create_dirtree()
    test_load_dirtree()


def test_load_dirtree() -> None:
    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'zt.dirtree')
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    # simple test
    os.makedirs(test_dir, exist_ok=True)
    root = load_dirtree(test_dir)
    assert root.name == 'zt.dirtree'
    assert root.dirs == []

    open(os.path.join(test_dir, 'ignore.txt'), 'w').close()

    root = load_dirtree(test_dir)
    assert root.name == 'zt.dirtree'
    assert root.dirs == []

    # small test
    os.makedirs(os.path.join(test_dir, 'a'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'b'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'c'), exist_ok=True)

    open(os.path.join(test_dir, 'a', 'ignore.txt'), 'w').close()

    root = load_dirtree(test_dir)
    assert root.name == 'zt.dirtree'

    names = [child.name for child in root.dirs]
    assert sorted(names) == ['a', 'b', 'c']
    for child in root.dirs:
        assert child.dirs == []

    # big test
    os.makedirs(os.path.join(test_dir, 'a', 'aa', 'aaa', 'aaaa'),
                exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'a', 'aa', 'aaa', 'aaab'),
                exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'a', 'aa', 'aaa', 'aaac'),
                exist_ok=True)

    os.makedirs(os.path.join(test_dir, 'b', 'ba'), exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'b', 'bb'), exist_ok=True)

    os.makedirs(os.path.join(test_dir, 'd', 'da', 'daa', 'daaa'),
                exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'd', 'da', 'dab', 'daba'),
                exist_ok=True)
    os.makedirs(os.path.join(test_dir, 'd', 'da', 'dab', 'dabb'),
                exist_ok=True)

    open(os.path.join(test_dir, 'd', 'da', 'ignore.txt'), 'w').close()

    root = load_dirtree(test_dir)

    names = [child.name for child in root.dirs]
    assert sorted(names) == ['a', 'b', 'c', 'd']

    for child in root.dirs:
        if child.name == 'a':
            assert len(child.dirs) == 1
            assert child.dirs[0].name == 'aa'
            assert len(child.dirs[0].dirs) == 1
            assert child.dirs[0].dirs[0].name == 'aaa'
            names = [leaf.name for leaf in child.dirs[0].dirs[0].dirs]
            assert sorted(names) == ['aaaa', 'aaab', 'aaac']
            for leaf in child.dirs[0].dirs[0].dirs:
                assert leaf.dirs == []
        if child.name == 'b':
            names = [leaf.name for leaf in child.dirs]
            assert sorted(names) == ['ba', 'bb']
            for leaf in child.dirs:
                assert leaf.dirs == []
        if child.name == 'c':
            assert child.dirs == []
        if child.name == 'd':
            assert len(child.dirs) == 1
            assert child.dirs[0].name == 'da'
            assert len(child.dirs[0].dirs) == 2
            names = [node.name for node in child.dirs[0].dirs]
            assert sorted(names) == ['daa', 'dab']
            for node in child.dirs[0].dirs:
                if node.name == 'daa':
                    assert len(node.dirs) == 1
                    assert node.dirs[0].name == 'daaa'
                    assert node.dirs[0].dirs == []
                if node.name == 'dab':
                    names = [leaf.name for leaf in node.dirs]
                    assert sorted(names) == ['daba', 'dabb']
                    for leaf in node.dirs:
                        assert leaf.dirs == []


def test_create_dirtree() -> None:
    cwd = os.getcwd()
    test_dir = os.path.join(cwd, 'dirtree-test')
    # simple test
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    create_dirtree(cwd, Directory('dirtree-test', []))
    assert os.listdir(test_dir) == []

    # create small dirtree
    create_dirtree(
        test_dir,
        Directory('small',
                  [Directory('a', []), Directory('b', [])]))

    small = os.path.join(test_dir, 'small')
    assert os.path.exists(small)

    assert sorted(os.listdir(small)) == ['a', 'b']
    assert os.listdir(os.path.join(small, 'a')) == []
    assert os.listdir(os.path.join(small, 'b')) == []

    create_dirtree(  # create deeper dirtree
        test_dir,
        Directory('big', [
            Directory('a', []),
            Directory('b', [
                Directory('ba', [
                    Directory('baa', [Directory('baaa', [])]),
                    Directory('bab', [
                        Directory('baba', []),
                        Directory('babb', [Directory('babba', [])])
                    ])
                ])
            ]),
            Directory('c', [
                Directory('ca', []),
                Directory('cb', []),
                Directory('cc', []),
                Directory('cd', []),
                Directory('ce', [])
            ]),
            Directory('d', [])
        ]))

    assert os.path.exists(small)

    big = os.path.join(test_dir, 'big')
    assert os.path.exists(big)

    assert sorted(os.listdir(big)) == ['a', 'b', 'c', 'd']
    assert os.listdir(os.path.join(big, 'a')) == []
    assert os.listdir(os.path.join(big, 'b')) == ['ba']
    assert sorted(os.listdir(os.path.join(
        big, 'c'))) == ['ca', 'cb', 'cc', 'cd', 'ce']
    assert os.listdir(os.path.join(big, 'd')) == []

    ba = os.path.join(big, 'b', 'ba')
    assert sorted(os.listdir(ba)) == ['baa', 'bab']
    assert os.listdir(os.path.join(ba, 'baa')) == ['baaa']
    assert os.listdir(os.path.join(ba, 'baa', 'baaa')) == []
    assert sorted(os.listdir(os.path.join(ba, 'bab'))) == ['baba', 'babb']
    assert os.listdir(os.path.join(ba, 'bab', 'baba')) == []
    assert os.listdir(os.path.join(ba, 'bab', 'baba')) == []

    assert os.listdir(os.path.join(ba, 'bab', 'babb')) == ['babba']
    assert os.listdir(os.path.join(ba, 'bab', 'babb', 'babba')) == []

    c = os.path.join(big, 'c')
    assert os.listdir(os.path.join(c, 'ca')) == []
    assert os.listdir(os.path.join(c, 'cb')) == []
    assert os.listdir(os.path.join(c, 'cc')) == []
    assert os.listdir(os.path.join(c, 'cd')) == []
    assert os.listdir(os.path.join(c, 'ce')) == []

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


if __name__ == '__main__':
    main()
