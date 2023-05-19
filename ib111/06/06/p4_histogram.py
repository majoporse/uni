from typing import List, Dict


# Napište (čistou) funkci, která na vstupu dostane signál ‹signal›
# reprezentovaný seznamem celočíselných amplitud (vzorků).
# Výsledkem bude statistika tohoto signálu, kterou vytvoří
# následujícím způsobem:

#  1. funkce signál nejdříve očistí od všech vzorků s amplitudou
#     větší než ‹max_amplitude› a menších než ‹min_amplitude›,
#  2. následně jej převzorkuje tak, že sloučí každých ‹bucket›
#     vzorků (poslední vzorek může být nekompletní) do jednoho
#     vypočtením jejich průměru a jeho následným zaokrouhlením
#     (pomocí vestavěné funkce ‹round›),
#  3. nakonec spočítá, kolikrát se v upraveném signálu objevují
#     jednotlivé amplitudy, a vrátí slovník, kde klíč bude amplituda
#     a hodnota bude počet jejích výskytů.

def histogram(data: List[int], max_amplitude: int,
              min_amplitude: int, bucket: int) -> Dict[int, int]:
    cleaned_data = []
    for i in range(len(data)):
        if data[i] in range(min_amplitude, max_amplitude):
            cleaned_data.append(data[i])

    result = {}
    for i in range(0, len(cleaned_data),bucket):
        bucket_sum = []
        for j in range(bucket):
            if i+j > len(cleaned_data)-1:
                continue
            else:
                bucket_sum.append(cleaned_data[i+j])
        bucket_sum = round(sum(bucket_sum) / len(bucket_sum))
        if bucket_sum in range(min_amplitude, max_amplitude):
            result[bucket_sum] = result.get(bucket_sum,0) + 1
    return result


def main() -> None:
    assert histogram([1, 1, 1], 5, 0, 1) == {1: 3}
    assert histogram([1, 1, 1, 1], 5, 0, 2) == {1: 2}
    assert histogram([1, 2, 3, 4, 5], 5, 2, 2) == {2: 1, 4: 1}
    assert histogram([1, 2, 9, 2, 10, 1, 1, 1, 1], 8, 1, 3) == {2: 1, 1: 2}
    assert histogram([], 1, 2, 5) == {}
    assert histogram([1, 1, 1, 8, 8, 8], 5, 3, 10) == {}
    assert histogram([1, 2, 3, 4], 2, 5, 3) == {}
    assert histogram([1, 2, 3, 4, 5], 10, 1, 7) == {3: 1}


if __name__ == '__main__':
    main()
