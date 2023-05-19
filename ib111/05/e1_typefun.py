from math import pi, isclose
from typing import Tuple, List, Optional

# Otypujte následující funkce tak, aby prošla typová kontrola
# s přiloženými testy.


# Funkce ‹degrees› konvertuje radiány na stupně.

def degrees(radians: float) -> float:
    return (radians * 180) / pi


# Funkce ‹to_list› rozdělí řetězec podle čárek do seznamu.

def to_list(raw: str) -> List[str]:
    return [s.strip() for s in raw.split(',')]


# Funkce ‹diagonal› vytvoří seznam obsahující prvky na diagonále
# matice ‹matrix›.

def diagonal(matrix: List[List[int]]) -> List[int]:
    diag = []
    for i in range(len(matrix)):
        diag.append(matrix[i][i])
    return diag


# Funkci ‹with_id› je v parametru ‹elements› předán seznam dvojic
# (celočíselný klíč, řetězec). Funkce najde prvek s klíčem ‹id_› a
# vrátí odpovídající řetězec.

def with_id(elements: List[Tuple[int, str]], id_: int) -> Optional[str]:
    for element_id, val in elements:
        if id_ == element_id:
            return val
    return None


# Funkce ‹format_student› naformátuje informace o studentovi do
# řetězce. Student je popsán trojicí: učo, jméno a volitelný atribut
# rok ukončení studia.

def format_student(student: Tuple[int , str, Optional[int]]) -> str:
    uco, name, graduated = student
    if graduated is not None:
        return str(uco) + ", " + name + ", " + str(graduated)
    return str(uco) + ", " + name


# Predikát ‹is_increasing› je pravdivý, pokud je seznam celých čísel
# ‹seq› rostoucí.

def is_increasing(seq: List[int]) -> bool:
    for i in range(1, len(seq)):
        if seq[i - 1] >= seq[i]:
            return False
    return True


def main() -> None:
    assert isclose(degrees(pi), 180)
    assert isclose(degrees(pi / 6), 30)

    assert diagonal([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == [1, 5, 9]

    assert to_list("a, b, c") == ['a', 'b', 'c']

    assert with_id([(1, 'a'), (2, 'b'), (3, 'c')], 2) == 'b'

    assert format_student((123456, "Adam", 2018)) == "123456, Adam, 2018"
    assert format_student((123456, "Eva", None)) == "123456, Eva"

    assert is_increasing([1, 2, 3])
    assert not is_increasing([1, 3, 2])


if __name__ == "__main__":
    main()  # mypy-only exercise, this should already pass
