import os
import shutil
from typing import List
from zipfile import ZipFile


# Napište proceduru ‹concat_zip›, která spojí obsahy všech zip
# archivů ze složky ‹directory› do jediného archivu s názvem
# ‹filename›. Pro tuto úlohu můžete použít knihovny ‹zipfile› a
# ‹os›. Předpokládejte, že mezi soubory v jednotlivých archivech
# nedochází ke konfliktům.

def concat_zip(directory: str, filename: str) -> None:
    pass


def main() -> None:
    test('./zt.concat/small/', 'result.zip',
         ['day.csv', 'month.csv', 'time.csv',
          'year.csv', 'country.csv',
          'country_full.csv'])
    test('./zt.concat/big/', 'result.zip',
         ['text/', 'text/other.txt', 'text/entry.txt', 'text/nested/',
          'text/nested/nested.txt', 'text/lorem.txt', 'color_srgb.csv',
          'color_web_safe.csv', 'color_x11.csv'])


def test(path: str, dst: str, expected: List[str]) -> None:
    if os.path.exists(dst):
        os.remove(dst)
    if os.path.exists('zt.concat'):
        shutil.rmtree('zt.concat')
    with ZipFile('zz.concat.zip', 'r') as zip_ref:
        zip_ref.extractall()
    concat_zip(path, dst)
    assert os.path.exists(dst)
    with ZipFile(dst, 'r') as zip:
        assert set(zip.namelist()) == set(expected)
    if os.path.exists(dst):
        os.remove(dst)


if __name__ == "__main__":
    main()
