# Napište funkci ‹sum_of_multiples› s parametrem ‹n›, která spočítá
# sumu kladných čísel ⟦aᵢ⟧, kde ⟦aᵢ ≤⟧ ‹n› a zároveň ⟦3 | aᵢ⟧ nebo
# ⟦5 | aᵢ⟧ (t.j. každé ⟦aᵢ⟧ je dělitelné třemi nebo pěti). Například
# pro ‹n = 10› je očekávaný výsledek ⟦33 = 3 + 5 + 6 + 9 + 10⟧.

def sum_of_multiples(n):
    a=0
    sucet=0
    while a<n:
        a+=1
        if a%3==0 or a%5==0:
            sucet+=a
    return(sucet)

def main():
    assert sum_of_multiples(10) == 33
    assert sum_of_multiples(13) == 45
    assert sum_of_multiples(14) == 45
    assert sum_of_multiples(16) == 60
    assert sum_of_multiples(100) == 2418
    assert sum_of_multiples(1000) == 234168


if __name__ == "__main__":
    main()
