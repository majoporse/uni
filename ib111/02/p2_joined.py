# Napište funkci, která vytvoří číslo zřetězením ‹count› po sobě
# jdoucích kladných čísel počínaje zadaným číslem ‹start›.  Tato
# čísla zřetězte vyjádřená v binární soustavě. Například volání
# ‹joined(1, 3)› zřetězí sekvenci ⟦1₂ = 1⟧, ⟦(10)₂ = 2⟧ a ⟦(11)₂ =
# 3⟧ vrátí číslo ⟦(11011)₂ = 27⟧. V Pythonu lze binární čísla přímo
# zapisovat v tomto tvaru: ‹0b11011› (podobně lze stejné číslo
# zapsat v šestnáctkové soustavě zápisem ‹0x1b› nebo osmičkové jako
# ‹0o33›).
def length(number):
    count = 0
    while number > 0 :
        number //= 2
        count += 1
    return count


def joined(start, count):
    bank = 0
    for i in range (start, start + count):
        bank = bank * 2 ** length(i) + i
    return bank
    

def main():
    assert joined(1, 3) == 0b11011
    assert joined(10, 4) == 0b1010101111001101
    assert joined(8, 5) == 0b10001001101010111100
    assert joined(99, 2) == 0b11000111100100
    assert joined(999, 3) == 0b111110011111111010001111101001
    assert joined(1111, 1) == 0b10001010111


if __name__ == "__main__":
    main()
