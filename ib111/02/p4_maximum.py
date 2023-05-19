# Napište funkci, která najde celé číslo ‹x›, které leží mezi
# hodnotami ‹low› a ‹high› (včetně), a pro které vrátí funkce ‹poly›
# maximální hodnotu (tzn. libovolné ⟦x⟧ takové, že pro všechny ⟦x'⟧
# platí ⟦f(x) ≥ f(x')⟧, kde ⟦f⟧ je funkce, kterou počítá podprogram
# ‹poly›).

def poly(x):
    return 10 + 30 * x - 15 * x ** 3 + x ** 5


def maximum(low, high):
    record = 0
    for i in range(low, high+1):
        if poly(i) > poly(record):
            record = i
    return record


def main():
    assert maximum(0, 5) == 5
    assert maximum(0, 2) == 1
    assert maximum(-5, -1) == -3
    assert maximum(-2, 2) == -2
    assert maximum(-10, 10) == 10


if __name__ == "__main__":
    main()
