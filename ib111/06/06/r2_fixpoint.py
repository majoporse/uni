from typing import Set


# Mějme funkci ‹f›, která pro dané celé číslo ‹a› vrátí množinu
# obsahující ‹a›, ‹a // 2› a ‹a // 7›. Použitím této funkce na
# množině pak míníme její použití na každém prvku dané množiny a
# následné sjednocení všech obdržených výsledků.

# Napište (čistou) funkci, která na množinu ze svého argumentu
# použije ‹f›, dále použije ‹f› na obdržený výsledek a takto bude
# pokračovat až dojde do bodu, kdy se dalším použitím ‹f› daná
# množina už nezmění. Výsledkem bude počet aplikací ‹f› na množinu,
# které bylo potřeba provést, než se proces zastavil.

# Například z množiny ‹{1, 5, 6}› vznikne první aplikací popsané
# funkce množina ‹{0, 1, 2, 3, 5, 6}›:
#
#  • hodnota ‹1› se zobrazila na ‹{1, 1 // 2 = 0, 1 // 7 = 0}›,
#  • hodnota ‹5› na ‹{5, 5 // 2 = 2, 5 // 7 = 0}›, a konečně
#  • hodnota ‹6› na ‹{6, 6 // 2 = 3, 6 // 7 = 0}›.
#
# Po další aplikaci se už množina nijak nezmění, proto je výsledkem
# číslo jedna.



def fixpoint(starting_set: Set[int]) -> int:
    result = starting_set.copy()
    count = 0
    length = 0
    while len(result) > length:
        length = len(result)
        
        
        for i in list(result):
            result.add(i)
            result.add(i//2)
            result.add(i//7)
        if length < len(result):
            count += 1
    return count

def main() -> None:
    assert fixpoint({1, 5, 6}) == 1
    assert fixpoint({0, 1}) == 0
    assert fixpoint(set()) == 0
    assert fixpoint({8, 13, 7}) == 2
    assert fixpoint({13, 17, 29}) == 2
    assert fixpoint({13, 47}) == 4


if __name__ == '__main__':
    main()
