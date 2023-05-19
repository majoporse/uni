# Napište funkci, která vytvoří číslo zřetězením ‹count› po sobě
# jdoucích kladných čísel počínaje zadaným číslem ‹start›.  Tato
# čísla zřetězte vyjádřená v binární soustavě. Například volání
# ‹joined(1, 3)› zřetězí sekvenci ⟦1₂ = 1⟧, ⟦(10)₂ = 2⟧ a ⟦(11)₂ =
# 3⟧ vrátí číslo ⟦(11011)₂ = 27⟧. V Pythonu lze binární čísla přímo
# zapisovat v tomto tvaru: ‹0b11011› (podobně lze stejné číslo
# zapsat v šestnáctkové soustavě zápisem ‹0x1b› nebo osmičkové jako
# ‹0o33›).
from math import log
def joined(start, count):

    def to_binary(x):
        powernumber = 0
        converted_number = 0
        n=1
        m=0
        while powernumber < x:
            powernumber = 2**n
            n += 1
        while powernumber >= 2**m:
            converted_number += (x //(powernumber//2**m))*(10**((log(powernumber//2**m, 2))))
            x -= (x //(powernumber//2**m))*powernumber//2**m
            m += 1
        return converted_number
    
    def get_digits(x):
        digits = 0
        
        while x>0:
            x//=10
            digits +=1
        return digits
    
    number = 0
    totaldigits = 0
    
    for i in range(count):
        totaldigits += get_digits(to_binary(start+i))
        
    for i in range(count):
        totaldigits -= get_digits(to_binary(start+i))
        number += to_binary(start+i) * 10**totaldigits
    
   
    def to_base10(x):
        n=0
        number2 = 0
        while x>0:
            number2 += x%10*2**n
            x//=10
            n+=1
        return number2
    
            
    result = to_base10(number)
    
    return result

    
            
            

            


def main():
    assert joined(1, 3) == 0b11011
    assert joined(10, 4) == 0b1010101111001101
    assert joined(8, 5) == 0b10001001101010111100
    assert joined(99, 2) == 0b11000111100100
    assert joined(999, 3) == 0b111110011111111010001111101001
    assert joined(1111, 1) == 0b10001010111


if __name__ == "__main__":
    main()
