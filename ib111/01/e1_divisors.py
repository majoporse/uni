# Napište funkci, která vrátí počet různých kladných dělitelů
# kladného celého čísla ‹number› (např. číslo 12 je dělitelné 1, 2,
# 3, 4, 6 a 12 – výsledek ‹divisors(12)› bude tedy 6.

def divisors(number):
    n=0
    pocetdelitelov=0
    while n<number:
        n+=1
        if number%n==0:
            pocetdelitelov+=1
    return (pocetdelitelov)


def main():
    assert divisors(1) == 1
    assert divisors(2) == 2
    assert divisors(3) == 2
    assert divisors(4) == 3
    assert divisors(5) == 2
    assert divisors(12) == 6
    assert divisors(16) == 5
    assert divisors(18) == 6
    assert divisors(42) == 8
    assert divisors(100) == 9
    assert divisors(127) == 2
    assert divisors(1024) == 11
    assert divisors(1069) == 2


if __name__ == "__main__":
    main()
