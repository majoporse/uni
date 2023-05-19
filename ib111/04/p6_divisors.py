# Napište čistou funkci, která na vstupu dostane dvě celá kladná
# čísla ‹rows› a ‹cols› a vrátí tabulku (dvourozměrný seznam)
# o ‹rows› řádcích a ‹cols› sloupcích. V buňce v řádku ‹y› a sloupci
# ‹x› bude počet společných dělitelů čísel ‹x› a ‹y›. Levý horní roh
# má souřadnice ‹x = y = 1›.

# Například pro vstup ‹rows = 4›, ‹cols = 2› dostaneme tabulku ‹[[1,
# 1], [1, 2], [1, 1], [1, 2]]›.
def dividors (a,b):
    count = 1
    if b>a:
        a,b = b,a
    for i in range(2, b+1):
        if b%i == 0 and a%i == 0 :
            count += 1
    return count

def common_divisors(rows, cols):
    table = []
    for i in range (rows):
        tablerow = []
        for j in range (cols):      
            tablerow.append(dividors(i+1,j+1))
        table.append(tablerow)
    return table


def main():
    assert common_divisors(4, 2) == [[1, 1], [1, 2], [1, 1], [1, 2]]
    assert common_divisors(1, 1) == [[1]]
    assert common_divisors(1, 8) == [[1, 1, 1, 1, 1, 1, 1, 1]]
    assert common_divisors(5, 1) == [[1], [1], [1], [1], [1]]
    assert common_divisors(6, 6) == [[1, 1, 1, 1, 1, 1],
                                     [1, 2, 1, 2, 1, 2],
                                     [1, 1, 2, 1, 1, 2],
                                     [1, 2, 1, 3, 1, 2],
                                     [1, 1, 1, 1, 2, 1],
                                     [1, 2, 2, 2, 1, 4]]
    assert common_divisors(2, 4) == [[1, 1, 1, 1],
                                     [1, 2, 1, 2]]


if __name__ == '__main__':
    main()
