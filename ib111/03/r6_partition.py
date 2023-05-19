# † Naprogramujte proceduru ‹partition›, která na vstup dostane
# seznam čísel ‹data› a platný index ‹idx›. Pro pohodlnost hodnotu
# ‹data[idx]› nazveme ‹pivot›.
#
# Procedura přeuspořádá seznam tak, že přesune prvky menší než
# ‹pivot› před ‹pivot› a prvky větší než ‹pivot› za ‹pivot›.
#
# Po transformaci bude tedy seznam «pomyslně» rozdělen na tři části:
#
#   • čísla menší než ‹pivot›
#   • pivot
#   • čísla větší než ‹pivot›
#
# Relativní pořadí prvků v první a poslední části není definováno,
# takže oba následovné výsledky pro seznam ‹[3, 4, 1, 2, 0]› a index
# ‹0› jsou správné: ‹[1, 0, 2, 3, 4]› nebo ‹[1, 2, 0, 3, 4]›.

# Při řešení nepoužívejte zabudované funkce pro řazení (funkce
# ‹partition› je mimo jiné pomocná funkce algoritmu quicksort, bylo
# by tedy absurdní zde sekvenci celou řadit).

def partition(data, idx):
    pass


def main():
    # Datový typ ‹set› používáme, abychom ze seznamu vytvořili
    # množinu – potřebujeme se vypořádat s neurčitostí pořadí prvků
    # v prefixu resp. sufixu po volání procedury ‹partition›. O typu
    # ‹set› se více dozvíte později.

    run_test([3, 4, 6, 2, 5], 4, set([2, 3, 4]), set([6]))
    run_test([0, 1, 3, 4, 6, 2, 5], 4, set([0, 1, 3, 4, 5, 2]), set([]))
    run_test([0, 1, 3, 4, 6, 2, 5], 2, set([0, 1, 2]), set([4, 5, 6]))
    run_test([0, 2, 1, 5, 6, 9], 0, set([]), set([2, 1, 5, 6, 9]))
    run_test([0, 2, 1, 5, 6, 9], 3, set([0, 1, 2]), set([6, 9]))
    run_test([6, 9, 3, 0, 1], 2, set([0, 1]), set([6, 9]))


def run_test(data, idx, prefix, postfix):
    pivot = data[idx]
    partition(data, idx)
    assert set(data[:len(prefix)]) == prefix
    assert data[len(prefix)] == pivot
    assert set(data[len(prefix) + 1:]) == postfix


if __name__ == "__main__":
    main()
