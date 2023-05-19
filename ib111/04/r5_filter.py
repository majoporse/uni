# † «Mean filter» je běžný filtr sloužící na odstranění drobných vad
# z obrázku. Funguje tak, že lokálně přílišně se odlišující pixely
# považuje za chybné a napravuje je přiblížením jejich hodnoty
# hodnotám okolních pixelů. To realizuje tak, že každý pixel nahradí
# průměrem jeho původní hodnoty s hodnotami okolních pixelů.

# Napište proceduru, která v parametru dostane obrázek reprezentován
# obdélníkovým dvourozměrným seznamem (délky všech vnitřních seznamů
# jsou stejné) a tento obrázek upraví aplikací mean filtru. Nové
# hodnoty jednotlivých pixelů přesněji spočítá tak, že zaokrouhlí
# průměr hodnot daného pixelu a všech jeho osmi sousedních pixelů,
# přičemž za sousední považujeme všechny pixely, které se ho
# dotýkají stranou nebo rohem. (Pro zaokrouhlování použijte
# vestavěnou funkci ‹round›.)

def mean_filter(image):
    pass


def main():
    check_mean_filter([[1]], [[1]])
    check_mean_filter([[1, 1], [1, 1]], [[1, 1], [1, 1]])
    check_mean_filter([[1, 2], [3, 4]], [[2, 2], [2, 2]])
    check_mean_filter([[3, 2, 4]], [[2, 3, 3]])
    check_mean_filter([[1, 1], [3, 3]], [[2, 2], [2, 2]])
    check_mean_filter([[5, 8, 10, 12], [1, 2, 3, 4]],
                      [[4, 5, 6, 7], [4, 5, 6, 7]])
    check_mean_filter([[1, 2, 3], [3, 2, 4], [7, 8, 9], [4, 5, 6]],
                      [[2, 2, 3], [4, 4, 5], [5, 5, 6], [6, 6, 7]])


def check_mean_filter(original_image, expected_result):
    mean_filter(original_image)
    assert original_image == expected_result


if __name__ == '__main__':
    main()
