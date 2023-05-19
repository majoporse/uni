from math import sqrt

# Tento příklad bude mírně nekonvenční v tom, že nebudete
# programovat nové funkce. Vaším úkolem bude naopak poznat, co
# zadaná funkce počítá a napsat testy, které Vaši hypotézu ověří.
# Každá funkce zde zadaná je predikát a většina má nějakou vstupní
# podmínku. Samotné funkce i proměnné v nich jsou záměrně
# pojmenované tak, aby Vám názvy nic neřekly.


def f_1(x, y):
    assert y >= 1
    assert x >= 1
    a = 0
    b = 1
    while x > 1:
        c = a + b
        a = b
        b = c
        x -= 1
    return b == y


def test_f_1():
    pass


def f_2(x, y):
    assert x > 0
    b = 1
    a = x // 2
    while a >= b:
        if x % b == 0:
            y -= 1
        b += 1
    return y <= 1


def test_f_2():
    pass


def f_3(x, y):
    assert x > 0 and y > 0
    a = 1
    b = 0
    while a <= max(x, y):
        if x % a == 0:
            b += 1
        if y % a == 0:
            b -= 1
        a += 1
    return b > 0


def test_f_3():
    pass


def f_4(x, y):
    for z in range(1, x):
        b = True
        for i in range(2, int(sqrt(z)) + 1):
            if z % i == 0:
                b = False
        if b:
            y -= 1
    return y == 0


def test_f_4():
    pass


def f_5(x):
    assert x >= 0
    y = 0
    z = x
    while z > 0:
        y = y * 7 + z % 7
        z = z // 7
    return x == y


def test_f_5():
    pass


def f_6(x, y):
    assert x >= 0
    z = 0
    while x > 0:
        z = z * 2 + (x % 2)
        x = x // 2
    return y == z


def test_f_6():
    pass


def f_7(x, y):
    assert x >= 0
    z = 2
    while x > 1:
        if x % z == 0:
            y -= 1
        while x % z == 0:
            x = x // z
        z += 1
    return y == 0


def test_f_7():
    pass


def f_8(x, y, z):
    assert x > 0 and y > 0
    d = 2
    r = 0
    while x > 1 and y > 1:
        if x % d == 0 and y % d == 0:
            x = x // d
            y = y // d
            r += 1
        while x % d == 0:
            x = x // d
        while y % d == 0:
            y = y // d
        d += 1
    return r == z


def test_f_8():
    pass


def main():
    test_f_1()
    test_f_2()
    test_f_3()
    test_f_4()
    test_f_5()
    test_f_6()
    test_f_7()
    test_f_8()
