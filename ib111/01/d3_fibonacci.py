# (Čistá) funkce ‹fib› počítá ‹n›-tý prvek tzv. Fibonacciho
# posloupnosti, dané předpisem: ⟦f(1) = f(2) = 1, f(n) = f(n - 1) +
# f(n - 2)⟧ -- každý prvek této posloupnosti je tedy součtem
# předchozích dvou (s výjimkou prvních dvou, které jsou pevně dané).
#
# Zkusíte-li si posloupnost napsat na papír (1, 1, 2, 3, 5, …),
# zřejmě zjistíte, že nejjednodušší způsob jak to udělat, je sečíst
# vždy poslední dvě už napsaná čísla a výsledek připsat na konec
# vznikajícího seznamu. Na dřívější čísla se už nemusíme znovu
# dívat: pro výpočet dalšího prvku potřebujeme vidět právě dva
# předchozí prvky. Můžete tedy vzít gumu, a po připsání jednoho
# čísla na konec smazat jedno číslo ze začátku – ani s tímto
# opatřením nebudete mít s výpočtem žádný problém. Na papíře budou v
# každém momentě 2 nebo 3 čísla, podle toho, kde se ve výpočtu
# nacházíte.
#
# Tuto myšlenku využijeme pro zápis algoritmu: budeme
# potřebovat dvě «proměnné», které budou reprezentovat ony dvě
# „naposled zapsaná“ čísla na konci posloupnosti (protože někdy máme
# ale na papíře čísla 3, budeme ve skutečnosti občas potřebovat
# ještě jednu – dočasnou – proměnnou).
#
# Protože postup výpočtu sleduje fixní seznam kroků, který se dokola
# opakuje, použijeme navíc «cyklus».

def fib(n):

    # Proměnná ‹a› reprezentuje předposlední a proměnná ‹b› poslední
    # vypočtené Fibonacciho číslo. Na začátku jsme na papír napsali
    # dvě jedničky – jedná se o ony pevně dané první dva prvky
    # posloupnosti.

    a = 1
    b = 1

    # Zatím jsme „vypočítali“ první a druhé Fibonacciho číslo.
    # Zajímá-li nás ‹n›-té číslo, musíme připsat dalších ‹n - 2›
    # čísel, aby platilo, že poslední číslo je to, které nás zajímá.
    # V každé iteraci následujícího cyklu provedeme výpočet jednoho
    # dalšího čísla (a umazání prvního čísla).

    for i in range(n - 2):

        # Do nové (dočasné) proměnné ‹c› si vypočteme další
        # Fibonacciho číslo. Po tomto příkazu bude proměnná ‹a›
        # obsahovat třetí číslo od konce aktuálně „zapsaného“
        # seznamu, proměnná ‹b› číslo předposlední a proměnná ‹c›
        # číslo poslední. Jsme nyní v situaci, kdy si pamatujeme
        # zároveň 3 čísla.

        c = a + b

        # „Zapomenutí“ prvního čísla realizujeme tak, že „nové“
        # poslední dvě čísla (nyní ‹b› a ‹c›) uložíme do proměnných
        # ‹a› a ‹b›. Hodnotou uloženou v (dočasné) proměnné ‹c› se
        # nebudeme dále zabývat – v další iteraci cyklu proměnnou
        # ‹c› přepíšeme novou dočasnou hodnotou.  Zamyslete se, zda
        # je pořadí následujících dvou příkazů důležité, a proč.

        a = b
        b = c

    # Jak jsme zmínili na začátku, proměnná ‹b› reprezentuje poslední
    # vypočtené Fibonacciho číslo (s výjimkou krátkého okamžiku
    # uprostřed cyklu). Protože jsme vypočetli právě ‹n› čísel,
    # poslední z vypočtených čísel je ‹n›-té, a tedy proměnná ‹b›
    # obsahuje kýžený výsledek funkce ‹fib›.

    return b


def main():  # demo
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(3) == 2
    assert fib(5) == 5
    assert fib(9) == 34
    assert fib(11) == 89
    assert fib(20) == 6765
    assert fib(40) == 102334155


if __name__ == "__main__":
    main()
