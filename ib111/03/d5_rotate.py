# V poslední ukázce pro tento týden se budeme zabývat vnitřním
# přiřazením, tzn. změnou samotné hodnoty typu seznam (změnou
# vnitřních vazeb indexů na hodnoty). Po delší době tedy budeme
# implementovat «proceduru» (podprogram, kterého hlavním smyslem je
# provést nějakou akci – v tomto případě pozměnit existující
# hodnotu). Tato procedura provede «rotaci» seznamu (na místě)
# o zadaný počet prvků. Např. rotací seznamu ‹[1, 2, 3, 4]›:
#
#  • o jedna doprava dostaneme seznam ‹[4, 1, 2, 3]›,
#  • o dva doprava seznam ‹[3, 4, 1, 2]›,
#  • o dva doleva tentýž seznam ‹[3, 4, 1, 2]› a konečně,
#  • o jedna doleva seznam ‹[2, 3, 4, 1]›.
#
# Směr rotace určíme dle znaménka: kladná čísla budou rotovat
# doprava, záporná doleva.

# Možností, jak „in situ“ rotaci seznamu implementovat je několik,
# my si ukážeme dvě. První je konceptuálně nejjednodušší, ale
# nepříliš efektivní: jako základní operaci používá posuv o jedna
# doleva nebo doprava. Každá rotace o jedničku musí projít celý
# seznam, posuvy o větší počet prvků budou tedy procházet celý
# seznam mnohokrát – proto je tato implementace neefektivní.

def rotate_naive(lst, amount):
    while amount != 0:
        if amount < 0:

            # Posuv doleva implementujeme tak, že ze seznamu
            # odstraníme první prvek (volání metody ‹pop(0)›), který
            # vzápětí přidáme na konec (volání ‹append›).

            lst.append(lst.pop(0))
            amount += 1
        else:

            # Posuv doprava je analogický, ale odstraníme prvek
            # z konce (volání ‹pop›) a metodou ‹insert› jej vložíme
            # na začátek.

            lst.insert(0, lst.pop())
            amount -= 1


# Jiná možnost je prvky rovnou posouvat na správné místo v seznamu
# (použitím vnitřního přiřazení), musíme si ale pamatovat prvky,
# které takto přepisujeme, a to až do doby, než je můžeme samotné
# přesunout na jejich cílovou pozici. Takových prvků může být
# najednou až tolik, jaká je velikost posuvu. Každý prvek ale
# přesouváme nejvýše jednou (bez ohledu na velikost posuvu), celkový
# počet operací je tedy výrazně menší než v předchozí implementaci.

def rotate_smart(lst, amount):

    # Pro jednoduchost implementujeme pouze posuvy doprava – posuvy
    # doleva by byly analogické. Díky tomu je tato implementace při
    # rotacích doleva méně efektivní (malé otočení doleva je totéž
    # jako velké otočení doprava). V proměnné ‹backup› si budeme
    # pamatovat ty prvky, které budeme v nejbližší době ukládat na
    # své cílové pozice (po prvních ‹amount› přesunech zde budou
    # uloženy právě ty prvky, které aktuálně v ‹lst› dočasně chybí).

    amount = amount % len(lst)
    backup = lst[0:amount]

    for i in range(len(lst)):

        # Do ‹target› spočteme cílové políčko pro další přesun, a
        # prvek zde umístěný prohodíme s příslušným prvkem v seznamu
        # ‹backup›. Na pozici ‹i % amount› seznamu ‹backup› se
        # nachází prvek, který byl v původním seznamu na pozici ‹i›,
        # a tedy je to ten prvek, který potřebujeme umístit do
        # ‹lst[target]›. Jejich prohozením se do ‹backup[i %
        # amount]› dostane prvek, který byl v původním seznamu na
        # pozici ‹target› (tj. ‹i + amount›) a tedy se k němu
        # vrátíme po dalších ‹amount› iteracích (‹(i + amount) %
        # amount == i % amount›).

        target = (i + amount) % len(lst)
        displaced = backup[i % amount]
        backup[i % amount] = lst[target]
        lst[target] = displaced


# Protože máme dvě implementace stejné funkce, testy si
# parametrizujeme konkrétní implementací, aby nám stačilo napsat je
# jednou. Za parametr ‹rotate› se postupně doplní ‹rotate_naive› a
# ‹rotate_smart›.

def check_rotate(rotate):
    lst = [1, 2, 3, 4]
    rotate(lst, 1)
    assert lst == [4, 1, 2, 3]
    rotate(lst, -1)
    assert lst == [1, 2, 3, 4]
    rotate(lst, -2)
    assert lst == [3, 4, 1, 2]
    rotate(lst, -2)
    assert lst == [1, 2, 3, 4]
    lst.append(5)
    rotate(lst, 3)
    assert lst == [3, 4, 5, 1, 2]


def main():  # demo
    check_rotate(rotate_naive)
    check_rotate(rotate_smart)


if __name__ == '__main__':
    main()
