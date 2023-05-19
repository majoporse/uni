# Naprogramujte (čistou) funkci, která ze dvou vzestupně seřazených
# seznamů čísel ‹a›, ‹b› vytvoří nový vzestupně seřazený seznam,
# který bude obsahovat všechny prvky z ‹a› i ‹b›. Nezapomeňte, že
# nesmíte modifikovat vstupní seznamy (jinak by funkce nebyla
# čistá). Pokuste se funkci naprogramovat «efektivně».

# «Pozor:» Při řešení nepoužívejte zabudované funkce pro řazení
# (funkce ‹merge› je mimo jiné pomocná funkce algoritmu merge sort,
# bylo by tedy absurdní zde sekvenci celou řadit). Řešení postavené
# na zabudované řadící funkci «nebude uznáno» jako příprava.

def merge(a, b):
    new = []
    i = 0
    j = 0
    while j < len(b) and i < len(a):
        if a[i] < b[j]:
            new.append(a[i])
            i += 1
        else:
            new.append(b[j])
            j += 1
    if i == len(a):
        for k in range(j, len(b)):
            new.append(b[k])
    else:
        for k in range(i, len(a)):
            new.append(a[k])
    return new


def main():
    assert merge([1, 2, 3], [1, 2, 3]) == [1, 1, 2, 2, 3, 3]
    assert merge([0, 2, 4, 6, 8], [1, 3, 5, 7, 9]) \
        == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert merge([], []) == []
    assert merge([], [1, 2]) == [1, 2]
    assert merge([1, 2], []) == [1, 2]
    assert merge([1, 5, 10], [-1, 2, 3, 4, 6, 10, 11]) \
        == [-1, 1, 2, 3, 4, 5, 6, 10, 10, 11]


if __name__ == "__main__":
    main()
