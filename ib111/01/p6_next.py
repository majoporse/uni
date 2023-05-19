# Napište funkci, která pro zadané číslo ‹number› najde nejbližší větší
# číslo, které je násobkem čísla ‹k›.

def next_multiple(number, k):
    n=0
    while k * n <= number :
        n+=1
    return k*n


# Dále napište funkci, která pro zadané číslo ‹number› najde
# nejbližší větší prvočíslo.

def next_prime(number):
    n = number
    isprime = False
    while  isprime :
        
        for  i in range(n):
            
            if n % i == 0:
                isprime = False
                break
            if i == n-1:
                isprime = True
        n += 1
    return n


def main():
    assert next_multiple(1, 2) == 2
    assert next_multiple(10, 7) == 14
    assert next_multiple(10, 5) == 15
    assert next_multiple(54, 6) == 60
    assert next_multiple(131, 29) == 145
    assert next_multiple(123, 112) == 224
    assert next_multiple(423, 90) == 450

    assert next_prime(1) == 2
    assert next_prime(2) == 3
    assert next_prime(3) == 5
    assert next_prime(4) == 5
    assert next_prime(11) == 13
    assert next_prime(12) == 13


if __name__ == "__main__":
    main()
