# V této ukázce si demonstrujeme «vytváření» seznamu, který bude
# výstupem (čisté) funkce ‹fib›. Seznam bude obsahovat prvních ‹n›
# členů Fibonacciho posloupnosti, které vypočteme už známým postupem
# (viz též ‹fibonacci.py› z části 1).

def fib(n):

    # Seznam budeme budovat v cyklu. Proměnné ‹a› a ‹b› již nebudeme
    # potřebovat, protože máme k dispozici celý seznam, bylo by tedy
    # nehospodárné pamatovat si dva prvky ještě jednou, a to jak z
    # pohledu využití paměti (i když v tomto případě by to nebyl
    # velký prohřešek), ale zejména z pohledu čitelnosti programu.
    # Většinou je nežádoucí uchovávat stejnou informaci na více
    # místech, není potom často jasné, jsou-li obě „místa“ plně
    # ekvivalentní, a pokud ano, tak že se chybou v programu nemůžou
    # rozejít.

    out = [1, 1]

    for i in range(n - 2):

        # Pro výpočet dalšího Fibonacciho čísla využijeme zápis pro
        # indexování seznamu od konce: je-li použitý index záporný,
        # automaticky se k němu přičte délka indexovaného seznamu,
        # tzn. ‹out[-2]› je totéž jako ‹out[len(out) - 2]›.
        # Rozmyslete si, že tento výraz skutečně popisuje
        # předposlední prvek seznamu ‹out›!

        value = out[-1] + out[-2]

        # Přidání na konec existujícího seznamu provedeme voláním
        # «metody» ‹append›. Metody jsou podprogramy, které často
        # leží někde mezi procedurou a čistou funkcí (nicméně i
        # metody můžou být čisté, a naopak můžou mít i charakter
        # procedury). Mají navíc ale jednu speciální vlastnost,
        # v podobě význačného parametru, který píšeme při
        # volání «před» jejich jméno. Následovné volání ‹append› má
        # tedy dva parametry – ‹out› a ‹value›.

        out.append(value)

    # Nyní stojíme před drobným problémem: mohlo se stát, že
    # volající si vyžádal méně než dva prvky posloupnosti, ale my
    # jsme pro pohodlí výpočtu do seznamu vložili první dvě hodnoty.
    # Jedna možnost řešení byla hned na začátku funkce ověřit, zda
    # není ‹n› nula nebo jedna, a rovnou vrátit příslušný seznam
    # (‹[]› nebo ‹[1]›). My tento problém místo toho využijeme,
    # abychom si ukázali, jak ze stávajícího seznamu hodnoty navíc
    # odstranit. Rozmyslete si, že tělo cyklu se provede skutečně
    # právě jednou, je-li ‹n = 1› a dvakrát, je-li ‹n = 0›. Metoda
    # ‹pop› (bez dalších parametrů) odstraní ze seznamu poslední
    # prvek.

    while len(out) > n:
        out.pop()

    return out


# Jako obvykle, program zakončíme několika testy, abychom se
# ujistili, že námi implementovaná funkce pracuje (aspoň v některých
# případech) správně.

def main():  # demo
    assert fib(0) == []
    assert fib(1) == [1]
    assert fib(2) == [1, 1]
    assert fib(3) == [1, 1, 2]
    assert fib(5) == [1, 1, 2, 3, 5]
    assert fib(9) == [1, 1, 2, 3, 5, 8, 13, 21, 34]


if __name__ == "__main__":
    main()
