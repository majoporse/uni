# Jednou ze základních metod digitálního zpracování obrazu je
# detekce hran. V tomto kontextu hranou chápeme oblast s ostrým
# kontrastem: nemusí jít nutně o hranice mezi objekty, ale třeba
# také změny textury, rozhraní mezi světlem a tmou, atd. Hrany se
# v obrázcích detekují na základě velké změny jasu sousedních pixelů
# (více o informací naleznete například ve Wikipedii pod heslem
# „Edge detection“).

# V této úloze si vyzkoušíte zjednodušený způsob, jak nalézt všechny
# hrany v daném obrázku, a vytvořit nový obrázek, který obsahuje
# pouze nalezené hrany.

# Napište (čistou) funkci, která na vstupu dostane obrázek
# reprezentovaný obdélníkovým seznamem seznamů (délky všech
# vnitřních seznamů jsou stejné) celých čísel a vrátí nový obrázek
# stejné velikosti, který obsahuje pouze hrany původního obrázku.
# Konkrétně pixely ve výsledném obrázku, kde na vstupu detekujeme
# hranu, budou mít hodnotu 1 a všechny ostatní hodnotu 0.

# Funkce bude brát krom vstupního obrázku ještě číselný parametr,
# který určí, o kolik se dva pixely musí nejméně lišit, abychom je
# označili za hranu. Konkrétně pak za součást nějaké hrany
# považujeme každý pixel, který se liší od některého ze svých čtyř
# sousedů alespoň o tuto hodnotu.

def find_edges(image, threshold):
    found_edges = []
    for i in range(len(image)):
        found_edges_row = []
        for j in range( len(image[i])):
            if ((abs(image[i][j] - image[i][j+1]) >= threshold) if j+1 < len(image[i]) else False)\
               or ((abs(image[i][j] - image[i][j-1]) >= threshold) if j-1 >= 0 else False)\
               or ((abs(image[i][j] - image[i+1][j]) >= threshold) if i+1 < len(image) else False)\
               or ((abs(image[i][j] - image[i-1][j]) >= threshold) if i-1 >= 0 else False):
                found_edges_row.append(1)
            else:
                found_edges_row.append(0)
        found_edges.append(found_edges_row)
    return found_edges


def main():
    assert find_edges([[1, 1], [1, 1]], 2) == [[0, 0], [0, 0]]
    
    assert find_edges([[1, 1, 1, 3, 3], [1, 1, 3, 3, 3], [1, 1, 1, 3, 3]], 2) \
        == [[0, 0, 1, 1, 0], [0, 1, 1, 0, 0], [0, 0, 1, 1, 0]]
    
    assert find_edges([[1, 1, 1, 3, 3], [1, 1, 3, 3, 3], [1, 1, 1, 3, 3]], 3) \
        == [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
    
    assert find_edges([[1, 1, 1, 2, 2, 2, 1, 2, ], [2, 1, 1, 1, 10, 2, 1, 2],
                       [1, 1, 1, 9, 10, 10, 1, 2], [1, 2, 1, 2, 9, 2, 1, 2],
                       [2, 1, 1, 1, 1, 2, 1, 2], [2, 2, 2, 1, 1, 2, 1, 2]], 6)\
        == [[0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 1, 0], [0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    assert find_edges([[1, 1, 1, 2, 2, 2, 1, 2, ], [2, 1, 1, 1, 10, 2, 1, 2],
                       [1, 1, 1, 9, 10, 10, 1, 2], [1, 2, 1, 2, 9, 2, 1, 2],
                       [2, 1, 1, 1, 1, 2, 1, 2], [2, 2, 2, 1, 1, 2, 1, 2]], 8)\
        == [[0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 1, 1, 0, 1, 1, 0], [0, 0, 0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]


if __name__ == '__main__':
    main()
