from typing import Tuple, List


# † Představte si bludiště, které se skládá z chodníků a rozcestí.
# Každý chodník začíná buď vstupem do bludiště nebo na nějakém
# rozcestí, a je buď slepý, končí východem z bludiště, nebo vede na
# nové rozcestí. Každé rozcestí má tedy jeden „příchozí“ chodník,
# který je ten jediný, po kterém se na něj lze od vchodu dostat, a
# několik chodníků „odchozích“ po kterých lze pokračovat.
#
# Jakkoliv budete bludištěm chodit, nemůže se tedy stát, že se
# vrátíte na rozcestí, kde už jste byli, aniž byste se vraceli po
# vlastních stopách.
#
# Aby se nám s bludištěm lépe pracovalo, každé rozcestí má jméno
# (řetězec). Chodník je pak zadaný jako dvojice (odkud, kam).
# Hodnota „odkud“ může být buď řetězec ‹entry›, nebo název rozcestí.
# Hodnota „kam“ může být buď řetězec ‹blind›, řetězec ‹exit›, nebo
# název rozcestí. Z každého rozcestí vede aspoň jeden chodník.
# Bludiště je zadané jako seznam chodníků.
#
# Vaším úkolem je zjistit, jakým nejmenším počtem chodníků musíme
# projít, abychom se dostali k nějakému východu. Vstup do bludiště
# je pouze jeden, východ je aspoň jeden.

def shortest_path(labyrinth: List[Tuple[str, str]]) -> int:
    pass


def main() -> None:
    assert shortest_path([("entry", "exit")]) == 1
    assert shortest_path([("entry", "A"), ("A", "exit")]) == 2
    assert shortest_path([("entry", "A"), ("A", "B"),
                          ("B", "exit"), ("A", "exit")]) == 2
    assert shortest_path([("entry", "A"), ("A", "B"),
                          ("B", "blind"), ("A", "exit")]) == 2
    assert shortest_path([("entry", "A"), ("A", "B"),
                          ("B", "exit"), ("A", "blind")]) == 3
    assert shortest_path([("entry", "A"), ("A", "B"),
                          ("A", "C"), ("B", "blind"),
                          ("C", "exit")]) == 3
    assert shortest_path([("A", "B"), ("entry", "A"),
                          ("A", "C"), ("B", "blind"),
                          ("C", "exit")]) == 3


if __name__ == '__main__':
    main()
