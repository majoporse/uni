# Abychom demonstrovali zápis a použití (čistých) funkcí a tedy i
# návratových hodnot, zadefinujeme si jednoduchou funkci se třemi
# parametry: délkami stran, které můžou (ale nemusí) zadávat
# trojúhelník. Výsledkem je pravdivostní hodnota (‹True› nebo
# ‹False›), která říká, zda zadaná trojice délek stran skutečně
# popisuje přípustný trojúhelník. Funkcím, které nemají vedlejší
# efekty (tj. čistým), a kterých výsledkem je pravdivostní hodnota,
# říkáme «predikáty».

# Funkce, stejně jako procedury, definujeme klíčovým slovem ‹def›,
# za kterým následuje název funkce. Názvy (a později v semestru i
# typové anotace) parametrů píšeme do závorek za název funkce a
# oddělujeme je čárkami. V tomto kontextu mluvíme o «formálních
# parametrech» – v těle funkce se chovají jako proměnné, do kterých
# jsou přiřazeny hodnoty tzv. «skutečných parametrů» – těch, které
# jsou funkci předány při jejím použití (viz také níže). Řádek
# ukončíme dvojtečkou a pokračujeme «tělem» funkce: seznamem
# příkazů, které se při jejím použití (zavolání) vykonají.

def is_triangle(a, b, c):

    # Vykonávání funkce je (korektně) ukončeno buď dojdou-li příkazy
    # k vykonání (dojdeme „na konec“), nebo vykonáním příkazu ‹return›.
    # Chceme-li, aby funkce poskytla svému volajícímu nějaký «výsledek»,
    # musíme použít příkaz ‹return›, kterému tuto výslednou hodnotu
    # předáme. Výsledek můžeme zapsat jako libovolný «výraz» (zejména
    # tedy nemusí být uložen v proměnné).

    # Všimněte si, že v tomto případě je výsledkem funkce logická
    # konjunkce (použití operátoru ‹and›) tří podvýrazů, kde každý
    # popisuje jednu variantu tzv.  trojúhelníkové nerovnosti. Za zmínku
    # zde stojí i konkrétní zápis těchto variant – první konjunkt je
    # zapsán v abecedním pořadí a každý další vznikl tzv. «cyklickou
    # záměnou» předchozího, tzn. náhradami ‹a› → ‹b›, ‹b› → ‹c› a ‹c› →
    # ‹a›.

    return (a + b > c) and (b + c > a) and (c + a > b)


# Procedura ‹main› je součástí každého příkladu, a obsahuje
# jednoduché (základní) testy, které ověří, že jste naprogramovali
# zhruba to, co se očekávalo.  Procházející testy «nezaručují», že
# je Vaše řešení správné! U příkladů jsou testy pouze v kostrách
# (nachystaných zdrojových souborech ‹.py›): v HTML a PDF verzi
# sbírky je budeme zobrazovat jen v ukázkách jako je tato.

def main():  # demo

    # V tomto příkladu stojí za povšimnutí i samotný zápis testů (je
    # důležité, abyste je uměli přečíst): příkaz ‹assert› ověří, že
    # výraz, který mu předáváme, se vyhodnotí na hodnotu ‹True›,
    # a pokud tomu tak není, program okamžitě ukončí s chybou.

    # Krom použití příkazu ‹assert› si všimněte i zápisu tzv.
    # «volání funkce» (neboli jejího použití): volání funkce je
    # «výraz», který začíná «jménem» příslušné funkce, které je
    # následováno závorkami, do kterých uvádíme (skutečné) hodnoty
    # parametrů funkce. Závorky mohou být prázdné, ale nelze je
    # vynechat.

    assert is_triangle(3, 4, 5)
    assert is_triangle(1, 1, 1)
    assert not is_triangle(1, 1, 3)
    assert not is_triangle(2, 3, 1)


if __name__ == "__main__":
    main()
