# Napište čistou funkci ‹gcd›, která pro zadaná kladná čísla nalezne
# jejich největšího společného dělitele. Použijte naivní algoritmus
# (tedy takový, který bude zkoušet všechny možnosti, počínaje
# největším vhodným kandidátem).

def gcd(x1, x2):
    number_1 = x1
    number_2 = x2
    i=1
    
    if x1<x2:
        number_1 = x2
        number_2 = x1
        
    divider = number_2
    
    while number_1 % (divider/i) != 0:
        i+=1
        
    return divider//i


def main():
    #assert gcd(5, 5) == 5
    #assert gcd(5, 10) == 5
    assert gcd(6, 15) == 3
    assert gcd(18, 15) == 3
    assert gcd(12, 1) == 1


if __name__ == "__main__":
    main()
