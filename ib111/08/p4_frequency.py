from typing import List


# Implementujte čistou funkci ‹frequency_sort›, která podle
# frekvencí výskytu seřadí hodnoty v seznamu ‹values›. Hodnoty se
# stejnou frekvencí výskytu nechť jsou seřazeny vzestupně podle
# hodnoty samotné. Výsledný seznam bude obsahovat každou hodnotu
# právě jednou.

def frequency_sort(values: List[int]) -> List[int]:
    freq_dict = {}
    for num in values:
        freq_dict[num] = freq_dict.get(num,0) + 1

    result = []
    freq_list = list(freq_dict.items())
    for i in range(len(freq_list) - 1):
        for j in range(len(freq_list) - i - 1):
            (x, y) = freq_list[j]
            (x1, y1) = freq_list[j+1]
            if y < y1 or y == y1 and x > x1:
                freq_list[j], freq_list[j+1] = freq_list[j+1], freq_list[j]

    for (x,y) in freq_list:
        result.append(x)

    return result
        
            


def main() -> None:
    assert frequency_sort([1, 3, 2, 4]) == [1, 2, 3, 4]
    assert frequency_sort([5, 6, 2, 5, 3, 3, 6, 5, 5, 6, 5]) == [5, 6, 3, 2]
    assert frequency_sort([1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 5, 5,
                           5, 4, 4, 4, 4, 4, 4]) == [4, 3, 2, 5, 1]
    records = [1, 2, 2, 2, 3, 3]
    assert frequency_sort(records) == [2, 3, 1]
    assert records == [1, 2, 2, 2, 3, 3]


if __name__ == "__main__":
    main()
