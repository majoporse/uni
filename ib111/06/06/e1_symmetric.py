from typing import Set, Tuple


# Jak jistě víte, binární relací nad danou množinou ⟦A⟧ je každá
# množina dvojic prvků z množiny ⟦A⟧, tzn. relace nad ⟦A⟧ je
# podmnožina kartézského součinu ⟦A × A⟧. Daná relace se pak nazývá
# symetrická, platí-li pro všechny dvojice ⟦(a, b)⟧ z této relace,
# že se v relaci zároveň nachází i dvojice ⟦(b, a)⟧. V této úloze
# budeme pracovat s relacemi nad celými čísly.

# Napište predikát, kterého hodnota bude ‹True› dostane-li
# v parametru symetrickou relaci, ‹False› jinak.

def is_symmetric(relation: Set[Tuple[int, int]]) -> bool:
    for (a, b) in relation:
        if (b, a) not in relation:
            return False
    return True
    
    
    


def main() -> None:
    assert is_symmetric({(1, 2), (2, 1)})
    assert is_symmetric(set())
    assert is_symmetric({(1, 2), (3, 4), (4, 3), (2, 1)})

    assert not is_symmetric({(1, 2)})
    assert not is_symmetric({(1, 2), (2, 3)})
    assert not is_symmetric({(1, 2), (3, 4), (2, 3), (4, 5)})


if __name__ == '__main__':
    main()
