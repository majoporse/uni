# Polybiův čtverec je metoda kódováni, známa již ve starověkém
# Řecku, založená na převádění zprávy z původní abecedy do jiné
# abecedy o méně znacích. Abecedu původních zpráv uspořádáme do
# čtverce (pokud počet znaků abecedy není druhou mocninou, typicky
# zůstává ve čtverci příslušný počet prázdných pozic) a
# jednotlivé znaky zprávy pak kódujeme dvojicí souřadnic pozice, na
# které se daný znak nachází ve vzniklém čtverci. Konkrétně kódovací
# čtverec vytváříme tak, že do nejmenšího čtverce, do kterého se
# daná abeceda vejde, postupně, začínaje z levého horního rohu,
# vpisujeme popořadě po řádcích jednotlivé znaky abecedy. Vzniklý
# čtverec pak v obou směrech indexujeme od jedničky, přičemž
# začínáme z levého horního rohu.

# V této úloze budeme jako abecedu zpráv používat písmena velké
# anglické abecedy. Těchto písmen je 26, podle výše popsaného
# postupu bychom tedy vytvářeli čtverec o straně velikosti 6 a
# zůstalo by nám 10 volných pozic. Toto se u této abecedy obvykle
# řeší tak, že písmena ‹I› a ‹J› sdílí společnou pozici a dostáváme
# tak čtverec se stranou o velikosti 5 (volné pozice v něm
# nezůstanou žádné). Tento obvyklý postup budeme implementovat i my.
# Písmena ‹I› a ‹J› se tedy budou kódovat stejně. U dekódování je
# pak už snadné z kontextu poznat, které z těchto písmen bylo
# v původní zprávě (program bude příslušnou pozici vždy dekódovat na
# ‹I›). Při šifrování budeme krom velkých písmen anglické abecedy
# akceptovat i malá a zakódujeme je, jako by se jednalo o velká, při
# dekódování ale budeme používat pouze velká písmena.

# Například ‹E› se bude kódovat jako ‹15›, poněvadž se nachází
# v prvním řádku a pátém sloupci, ‹I› a ‹J› se budou kódovat na ‹24›
# a třeba ‹T› na ‹44›. Kód slova ‹EJT› pak vypadá takto: ‹15 24 44›.

# Napište (čistou) funkci, která na vstupu dostane slovo (řetězec)
# skládající se z velkých a malých písmen anglické abecedy a vrátí
# tento text zašifrován pomocí Polybiova čtverce jako řetězec, ve
# kterém budou kódy jednotlivých písmen odděleny mezerou.

def polybius_encode(word):
    pass


# Dále napište čistou funkci, která na vstupu dostane řetězec
# reprezentující šifru vzniklou výše popsaným způsobem a vrátí
# původní slovo jako řetězec.

def polybius_decode(code):
    pass


def main():
    assert polybius_encode("Python") == "35 54 44 23 34 33"
    assert polybius_encode("EJT") == "15 24 44"
    assert polybius_encode("aEvZ") == "11 15 51 55"
    assert polybius_encode("AbcdefGHIJklmnOpqrstuvwXYz") == \
        "11 12 13 14 15 21 22 23 24 24 25 31 32 33 34 35 41 42 43 44 45 51 " \
        "52 53 54 55"

    assert polybius_decode("15 24 44") == "EIT"
    assert polybius_decode("35 54 44 23 34 33") == "PYTHON"
    assert polybius_decode("11 15 51 55")
    assert polybius_decode("11 12 13 14 15 21 22 23 24 24 25 31 32 33 34 35 "
                           "41 42 43 44 45 51 52 53 54 55") == \
        "ABCDEFGHIIKLMNOPQRSTUVWXYZ"


if __name__ == '__main__':
    main()
