# Napište predikát, který rozhodne, zda lze dané číslo ‹num› napsat
# jako součet ⟦∑ᵢ₌₁ⁿaᵢ²⟧, kde ⟦n⟧ je zadáno parametrem ‹count› a
# ⟦aᵢ⟧ jsou po dvou různá kladná čísla. Jinými slovy, lze ‹num›
# zapsat jako součet ‹count› druhých mocnin různých kladných čísel?

def is_sum_of_squares(num: int, count: int) -> bool:
    pass


def main() -> None:
    assert is_sum_of_squares(42, 3)
    assert not is_sum_of_squares(42, 2)
    assert not is_sum_of_squares(18, 2)
    assert not is_sum_of_squares(100, 3)
    assert is_sum_of_squares(100, 5)
    assert not is_sum_of_squares(1000, 13)


if __name__ == '__main__':
    main()
