# V této ukázce naprogramujeme funkci, která na vstupu dostane řetězec, který
# obsahuje dvě fráze oddělené čárkou. Výstupem bude nová fráze, které bude
# obsahovat „součet“ těchto dvou vstupních frází.
#
# Sčítání definujeme po písmenech takto (minuska je malé písmeno, verzálka
# velké):
#
#  • mezera + mezera = mezera
#  • mezera + ⟦x⟧-té písmeno = ⟦x⟧-té písmeno (velikost se zachová)
#  • ⟦x⟧-tá minuska + ⟦y⟧-tá minuska = ⟦(x+y)⟧-tá minuska
#  • ⟦x⟧-tá verzálka + ⟦y⟧-tá verzálka = ⟦(x+y)⟧-tá verzálka
#  • ⟦x⟧-tá minuska + ⟦y⟧-tá verzálka nebo naopak = ⟦(x+y)⟧-tá verzálka


# Nejprve si definujeme několik pomocných funkcí na sčítání a odečítání
# písmenek.  Musíme si zde dát pozor, protože jednotlivá písmena jsou v Pythonu
# reprezentována jako jednopísmenné řetězce, a mají tedy definovánu operaci
# sčítání (operátor ‹+›), která ale funguje jako zřetězení.  Abychom mohli
# sčítat numerické hodnoty znaků, potřebujeme zabudovanou (čistou) funkci
# ‹ord›, která ze znaku vyrobí hodnotu typu ‹int›.  Jaká čísla jsou kterým
# znakům přidělena nás nemusí příliš zajímat, důležité je, že velká i malá
# písmena jsou uspořádána abecedně (každé zvlášť, tzn. od jiného indexu).

# Na to, abychom zjistili zda se jedná o minusku nebo verzálku můžeme využít
# predikátovou metodu ‹isupper› resp. ‹islower›.

def add(a, b):
    return chr(ord(a) + b)


def sub(a, b):
    return ord(a) - ord(b)


def index(a):
    if a.isupper():
        return sub(a, 'A')
    if a.islower():
        return sub(a, 'a')


def string_sum(words):

    # Nejprve musíme vstupní řetězec rozdělit podle znaku čárka na dvě fráze.
    # K tomu můžeme využít metodu ‹split›, která daný řetězec rozdělí na seznam
    # podřetězců, které byly v původním odděleny dodaným oddělovačem (opět
    # řetězec). Vstupní podmínkou funkce je, že vstupní řetězec obsahuje právě
    # jednu čárku, a tedy výsledek volání ‹split› vytvoří vždy dvouprvkový
    # seznam. Proto můžeme využít syntaxe „rozbalení“ seznamu (které funguje
    # stejně jako to, které známe u n-tic). Tento přístup má výhodu mimo jiné
    # v tom, že bude-li vstupní podmínka porušena, program na tomto místě
    # okamžitě skončí s chybou. Proměnná ‹result› slouží jako zobecněný střadač
    # – budeme v ní budovat výsledný řetězec.

    top, bottom = words.split(",")
    result = ""

    # Nyní řetězce zarovnáme na společnou délku. Není to nejefektivnější
    # možnost, ale je zřejmé co se děje a v dalším již můžeme předpokládat, že
    # jsou řetězce stejné délky, čim se kód znatelně zjednoduší.

    while len(top) < len(bottom):
        top += " "
    while len(top) > len(bottom):
        bottom += " "

    # Nyní zbývá samotné sčítání, pro které jsme si definovali pomocné funkce
    # výše, a stačí tedy vyřešit jednotlivé případy popsané v zadání.

    for i in range(len(top)):
        if top[i] == ' ':
            result += bottom[i]
        elif bottom[i] == ' ':
            result += top[i]
        elif top[i].isupper() or bottom[i].isupper():
            result += add('A', index(top[i]) + index(bottom[i]))
        else:
            result += add('a', index(top[i]) + index(bottom[i]))

    return result


# Nakonec na několika vstupech ověříme, že jsme v implementaci
# neudělali chybu.

def main():  # demo
    assert string_sum("xy,") == "xy"
    assert string_sum("xy,a") == "xy"
    assert string_sum("xy,b") == "yy"
    assert string_sum("xy,bb") == "yz"
    assert string_sum("Xy,bb") == "Yz"
    assert string_sum("xy,Bb") == "Yz"
    assert string_sum("xY,BB") == "YZ"


if __name__ == '__main__':
    main()
