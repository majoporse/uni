# V této úloze naprogramujeme trojici (čistých) funkcí, které slouží
# pro práci s číselnými soustavami. Reprezentaci čísla v nějaké
# číselné soustavě budeme ukládat jako dvojici ‹(base, digits)›, kde
# ‹base› je hodnota typu ‹int›, která reprezentuje základ soustavy,
# a ‹digits› je seznam cifer v této soustavě, kde každý prvek je
# hodnota typu ‹int›, která spadá do rozsahu [0, ‹base› - 1]. Index
# seznamu ‹digits› odpovídá příslušné mocnině ‹base›. Například:
#
#  • ‹(10, [2, 9])› je zápis v desítkové soustavě a interpretujeme
#    jej jako ‹2 * 1 + 9 * 10›, co odpovídá číslu ‹92›
#  • ‹(7, [2, 1])› je zápis v sedmičkové soustavě a kóduje
#    ‹2 * 1 + 1 * 7 = 9›

# První funkce implementuje převod čísla ‹number› do ciferné
# reprezentace v soustavě se základem ‹base›:

def to_digits(number, base):
    my_number = []
    a = number
    while a:
        my_number.append(a % base)
        a //= base
    return (base, my_number)


# Další funkce provádí převod opačným směrem, z ciferné
# reprezentace ‹digits› vytvoří hodnotu typu ‹int›:

def from_digits(digits):
    n = 0
    base10 = 0
    base, number = digits
    for i in number:
        base10 += i * base ** n
        n += 1
    return base10

# Konečně funkce ‹convert_digits› převede ciferný zápis z jedné
# soustavy do jiné soustavy. Nápověda: tato funkce je velmi
# jednoduchá.


def convert_digits(digits, base):
    return to_digits(from_digits(digits), base)


def main():
    assert to_digits(92, 10) == (10, [2, 9])
    assert to_digits(9, 7) == (7, [2, 1])
    assert to_digits(33, 16) == (16, [1, 2])
    assert to_digits(10, 2) == (2, [0, 1, 0, 1])
    assert convert_digits((16, [1, 2]), 10) == (10, [3, 3])
    assert to_digits(33, 7) == (7, [5, 4])
    assert from_digits((7, [5, 4])) == 33
    assert from_digits((3, [1, 0, 1])) == 10
    assert from_digits(to_digits(1382, 24)) == 1382

    for base in range(2, 12):
        for n in range(2, 200):
            assert from_digits(to_digits(n, base)) == n


if __name__ == "__main__":
    main()
