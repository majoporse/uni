from typing import List

# S polynomy jsme se už setkali dvakrát, v kapitolách 5 a 7. Ještě
# jednou si připomeňme, jak polynomy vypadají:
#
#  ⟦  P(x) = aₙxⁿ + … + a₂x² + a₁x + a₀ = ∑₀ⁿ aᵢxⁱ ⟧
#
# Tentokrát budeme pracovat s řetězcovou reprezentací polynomů,
# která vypadá jako výše uvedený zápis, pouze místo ⟦aᵢ⟧ bude
# obsahovat konkrétní koeficienty. Pro lepší čitelnost budeme navíc
# požadovat, aby byly záporné koeficienty v řetězci zapsané jako
# ⟦5x² - 7x⟧, nikoliv jako ⟦5x² + -7x⟧. Vaším úkolem je napsat
# dvojici funkcí: ‹poly_to_str›, která převede seznam koeficientů na
# řetězec a ‹str_to_poly› která realizuje opačnou konverzi.
# Koeficienty budou v seznamech v pořadí ⟦aᵢ⟧ na indexu ⟦n - i⟧.


def poly_to_str(poly: List[int]) -> str:
    pass


def str_to_poly(string: str) -> List[int]:
    pass


def main() -> None:
    p432 = str_to_poly("4x² + 3x + 2")
    p402 = str_to_poly("4x² + 2")
    p400 = str_to_poly("4x²")
    pn402 = str_to_poly("- 4x² + 2")
    pn40n2 = str_to_poly("- 4x² - 2")
    pn4n3n2 = str_to_poly("- 4x² - 3x - 2")
    p50000 = str_to_poly("5x⁴")
    pn10 = str_to_poly("- x")
    p0 = str_to_poly("0")

    assert p432 == [4, 3, 2]
    assert p402 == [4, 0, 2]
    assert p400 == [4, 0, 0]
    assert pn402 == [-4, 0, 2]
    assert pn40n2 == [-4, 0, -2]
    assert pn4n3n2 == [-4, -3, -2]
    assert p50000 == [5, 0, 0, 0, 0]
    assert pn10 == [-1, 0]
    assert p0 == [0]

    assert poly_to_str(p432) == "4x² + 3x + 2"
    assert poly_to_str(p402) == "4x² + 2"
    assert poly_to_str(p400) == "4x²"
    assert poly_to_str(pn402) == "- 4x² + 2"
    assert poly_to_str(pn40n2) == "- 4x² - 2"
    assert poly_to_str(pn4n3n2) == "- 4x² - 3x - 2"
    assert poly_to_str(p50000) == "5x⁴"
    assert poly_to_str(pn10) == "- x"
    assert poly_to_str(p0) == "0"


if __name__ == '__main__':
    main()
