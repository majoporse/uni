# Napište (čistou) funkci, která pro zadaný seznam nezáporných čísel
# ‹data› vrátí nový seznam obsahující dvojice – číslo a jeho
# četnost. Výstupní seznam musí být seřazený vzestupně dle první
# složky. Můžete předpokládat, že v ‹data› se nachází pouze celá
# čísla z rozsahu [0, 100] (včetně).

def histogram(data):
    data.sort()
    histogram = []
    count = 1
    i = -1
    while i+2 < len(data):
        i += 1
        if data[i] == data[i+1]:
            count += 1
            continue
        histogram.append((data[i], count))
        if i+2 >= len(data):
            continue
        count = 1
    if len(data) == 0:
        return []
    if data[-1] == data[-2]:
        histogram.append((data[-1], count))
    else:
        histogram.append((data[-1], 1))
    return histogram


def main():
    assert histogram([1, 2, 3, 2, 1]) == [(1, 2), (2, 2), (3, 1)]
    assert histogram([7, 1, 7, 1, 5]) == [(1, 2), (5, 1), (7, 2)]
    assert histogram([1, 1, 1]) == [(1, 3)]
    assert histogram([]) == []


if __name__ == "__main__":
    main()
