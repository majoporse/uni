# Napište funkci ‹delete_to_maximal›, která pro dané číslo ‹number›
# najde největší možné číslo, které lze získat smazáním jedné
# desítkové cifry.
from math import log, floor


def delete_to_maximal(number):
    length = floor(log(number, 10))+1
    biggest = 0
    for i in range (1, length+1):
        a = (number //10**(i-1))%10
        number-= a*10**(i-1)
        
        
        for j in range (i, length):
            b = (number //10**(length -j))%10
            number += b*10**(length-j)
            
            
        if number > biggest:
            biggest = number
            
            
    return biggest


# Napište funkci ‹delete_k_to_maximal›, která pro dané číslo
# ‹number› najde největší možné číslo, které lze získat smazáním
# (vynecháním) ‹k› desítkových cifer.

def delete_k_to_maximal(number, k):
    for i in range (k):
        delete_to_maximal(number)
    return number

def main():
    assert delete_to_maximal(548768) == 5
    assert delete_to_maximal(45) == 5
    assert delete_to_maximal(100) == 10
    assert delete_to_maximal(123) == 23
    assert delete_to_maximal(4312) == 432
    assert delete_to_maximal(1231) == 231
    assert delete_to_maximal(2331) == 331

    assert delete_k_to_maximal(2331, 2) == 33
    assert delete_k_to_maximal(22331, 2) == 331
    assert delete_k_to_maximal(12345, 4) == 5
    assert delete_k_to_maximal(1234554321, 8) == 55
    assert delete_k_to_maximal(12312123123, 4) == 33123123
    assert delete_k_to_maximal(123321123321, 4) == 33223321
    assert delete_k_to_maximal(11181118111, 9) == 88


if __name__ == "__main__":
    main()
