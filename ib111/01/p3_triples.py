# Napište funkci ‹largest_triple›, která najde pythagorejskou
# trojici ⟦(a, b, c)⟧ – totiž takovou, že ⟦a⟧, ⟦b⟧ a ⟦c⟧ jsou
# přirozená čísla a platí ⟦a² + b² = c²⟧ (tzn. tvoří pravoúhlý
# trojúhelník). Hledáme trojici, která:
#
#  1. má největší možný součet ⟦a + b + c⟧,
#  2. hodnoty ⟦a⟧, ⟦b⟧ jsou menší než ‹max_side›.
#
# Výsledkem funkce bude součet ⟦a + b + c⟧, tedy největší možný
# obvod pravoúhlého trojúhelníku, jsou-li obě jeho odvěsny kratší
# než ‹max_side›.
from math import sqrt
def largest_triple(max_side):
    ''''
    largest=0
    abc=0
    
    for c in range (max_side-1):
               
        for i in range (c):
            if sqrt(c**2-(i+1)**2)%1!=0 :
                continue
            else:
                if abc < c+i+1+sqrt(c**2-(i+1)**2):
                    largest = i+1
                    abc = c+i+1+sqrt(c**2-(i+1)**2)
            
    return max_side+largest+sqrt(max_side**2-(largest)**2)
    '''
    a=max_side-1
    b=max_side-1
    abc=0
    
    for i in range(max_side):
        if sqrt(a**2+b**2)%1!=0:
            a-=(1)
        else:
            if a+b+sqrt(a**2+b**2)>abc:
                abc= a+b+sqrt(a**2+b**2)
        for j in range (max_side):
            if sqrt(a**2+b**2)%1!=0:
                b-=(1)
                if b==0:
                    b== max_side
            else: 
                if a+b+sqrt(a**2+b**2)>abc:
                    abc= a+b+sqrt(a**2+b**2)
        
        
    return abc
            
        

def main():
    assert largest_triple(10) == 24
    assert largest_triple(25) == 72
    assert largest_triple(100) == 288
    assert largest_triple(150) == 490
    assert largest_triple(1000) == 3290


if __name__ == "__main__":
    main()
