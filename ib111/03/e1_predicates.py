# Napište predikát ‹all_greater_than›, který je pravdivý, právě
# když jsou všechna čísla v seznamu ‹sequence› větší než ‹n›.

def all_greater_than(sequence, n):
    for i in sequence:
        if i < n:
            return False
    return True


# Dále napište predikát ‹any_even›, který je pravdivý, je-li
# v seznamu ‹sequence› aspoň jedno sudé číslo.

def any_even(sequence):
    for i in sequence:
        if i % 2 == 0:
            return True
    return False


def main():
    assert all_greater_than([1, 2, 0, -1, 1, 14], -3)
    assert not all_greater_than([1, 2, 0, -1, 1, 14], 14)
    assert all_greater_than([], -100)
    assert all_greater_than([], 100)
    assert all_greater_than([12, 21, 14, 10], 7)
    assert all_greater_than([1, 2, 14, 10], -25)
    assert not all_greater_than([-5, -6, -10, -9], -4)
    assert all_greater_than([-5, -6, -10, -9], -40)

    assert not any_even([])
    assert any_even([2])
    assert any_even([1, 2])
    assert not any_even([1, 3])


if __name__ == "__main__":
    main()
