from typing import Optional

# V této ukázce se zaměříme na datové struktury. Jednoduše zřetězený
# seznam jste již viděli v přednášce, zde si ukážeme velice
# jednoduchou obměnu téhož. Seznamy tohoto typu nejsou sice v praxi
# až tak oblíbené (s možnou výjimkou Linuxového jádra, kde se
# používají často) ale velmi dobře ilustrují klíčové znalosti práce
# s pamětí. Proto je velmi důležité, abyste jim rozuměli.

# Zřetězený seznam je složený z «uzlů». Každý uzel je samostatná
# hodnota uložená v paměti (to, kde přesně je uložená a jak se o tom
# rozhodne, nás prozatím nebude příliš zajímat, stejně jako jsme to
# dosud neřešili u jiných typů hodnot). Každý uzel si bude pamatovat
# jedno z čísel, které bylo do seznamu uloženo. Co je ale mnohem
# zajímavější je, že si zároveň bude pamatovat svého následovníka:
# další uzel v seznamu.

# Zde je na místě připomenout, jak v Pythonu fungují proměnné,
# konkrétně «atributy» složených typů. Ze třetí kapitoly si jistě
# pamatujete, že zabudovaný typ ‹list› přiřazuje (váže) hodnoty
# k jednotlivým indexům. Má navíc tzv. «vnitřní přiřazení»: vazbu
# indexu a hodnoty lze změnit. Vnitřní přiřazení zapisujeme třeba
# ‹items[3] = 9›, jeho efekt jsme si ukazovali na obrázku, který si
# zde připomeneme:

#  ┌───┬───┬───┬───┬───┐
#  │ 0 │ 1 │ 2 │░3 │ 4 │                indexy
#  └───┴───┴───┴───┴───┘
#    │   │   │   │   ╰─────────────╮
#    │   │   │   ╰───────────╮     │    odkazy
#    │   ╰─╮ ╰───╮           │     │
#    ▼     ▼     ▼           ▼     ▼
#  ┌───┐ ┌───┐ ┌───┐ ┌┄┄┄┐ ┌───┐ ┌───┐
#  │ 1 │ │ 1 │ │ 2 │ ┆ 3 ┆ │ 9 │ │ 5 │  hodnoty
#  └───┘ └───┘ └───┘ └┄┄┄┘ └───┘ └───┘


# Složené typy mají stejný koncept vnitřního přiřazení, místo
# (proměnného) počtu indexů mají ale (pevnou) množinu jmen.
# Zadefinujme si složený typ ‹Node›, kterým budeme reprezentovat
# jednotlivé uzly zřetězeného seznamu:

class Node:
    def __init__(self, item: int):
        self.next: Optional['Node'] = None
        self.item = item

# Vytvoříme-li novou hodnotu typu ‹Node›, například voláním
# ‹a = Node(3)›, bude výsledek vypadat takto:

#  ┌───┐   ┌──────┐       ┌──────┐
#  │‹a›│──▶│ next │──────▶│ None │
#  └───┘   ├┄┄┄┄┄┄┤ ┌───┐ └──────┘
#          │ item │▶│ 3 │
#          └──────┘ └───┘

# Vytvořme nyní novou hodnotu, ‹b = Node(5)› a použijme vnitřní
# přiřazení ‹a.next = b›. Výsledek bude:

#  ┌───┐
#  │‹b›│─────────────────────╮
#  └───┘                     ▼
#  ┌───┐   ┌──────┐       ┌──────┐       ┌──────┐
#  │‹a›│──▶│ next │──────▶│ next │──────▶│ None │
#  └───┘   ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ └──────┘
#          │ item │▶│ 3 │ │ item │▶│ 5 │
#          └──────┘ └───┘ └──────┘ └───┘

# Pro jistotu vytvoříme ještě jeden uzel, tentokrát dvojicí příkazů
# ‹b.next = Node(7)› a ‹b = b.next›. Výsledná situace bude vypadat
# takto:

#  ┌───┐
#  │‹b›│──────────────────────────────────╮
#  └───┘                                  ▼
#  ┌───┐ ┌──────┐       ┌──────┐       ┌──────┐       ┌──────┐
#  │‹a›│▶│ next │──────▶│ next │──────▶│ next │──────▶│ None │
#  └───┘ ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ └──────┘
#        │ item │▶│ 3 │ │ item │▶│ 5 │ │ item │▶│ 7 │
#        └──────┘ └───┘ └──────┘ └───┘ └──────┘ └───┘

# Na tomto posledním obrázku je také vidět, že k uzlu s hodnotou ‹5›
# již sice nemáme přímý přístup (není přímo uložen v žádné
# proměnné), dostaneme se k němu ale skrz atribut ‹next› uzlu ‹a›.


# Nyní již můžeme přistoupit k implementaci samotného zásobníku.
# Tento bude mít pouze 2 metody, ‹push› a ‹pop›. Metoda ‹push› vloží
# novou hodnotu na vrchol zásobníku. Pro tuto hodnotu vytvoří nový
# uzel a přidá ho na začátek seznamu. Metoda ‹pop› naopak uzel
# odstraní a hodnotu v něm uloženou vrátí. Je-li seznam prázdný,
# vrátí ‹None›.

class Stack:

    # Metoda ‹__init__› inicializuje prázdný zásobník. Vrchol
    # zásobníku bude uzel (hodnota typu ‹Node›), je-li zásobník
    # neprázdný, jinak bude ‹None›.

    def __init__(self) -> None:
        self.top: Optional[Node] = None

    # Následuje metoda ‹push›. Ta vytvoří nový uzel a nastaví jeho
    # následníka na stávající vrchol (ať už je to uzel nebo ‹None›).
    # Parametrem metody ‹push› je hodnota, kterou chceme do
    # zásobníku vložit. Uvažme následující situaci před voláním
    # ‹stack.push(7)›:

    #  ┌─────┐                    ┌──────┐       ╭┄┄┄╮   ┌──────┐
    #  │‹top›│───────────────────▶│ next │──────▶┆ … ┆──▶│ None │
    #  └─────┘                    ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯   └──────┘
    #                             │ item │▶│ 3 │
    #                             └──────┘ └───┘

    def push(self, item: int) -> None:

        # Metoda ‹push› má pouze tři příkazy. Proto si na ní
        # detailně ilustrujeme, jak se bude postupně vnitřní
        # struktura (tvořená zejména atributy ‹next› jednotlivých
        # uzlů) postupně měnit.

        # Atribut ‹top› prozatím obsahuje uzel, který byl doteď
        # (tzn. těsně před voláním metody ‹push›) vrcholem
        # zásobníku. První příkaz vytvoří nový uzel (voláním
        # ‹Node(item)›) a přiřadí jej do lokální proměnné ‹new›.

        new = Node(item)

        # Tento uzel zatím není nijak svázaný se zbytkem seznamu:

        #     ╭──────────────────╮
        #  ┌─────┐    ┌──────┐   │   ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│ ╭─▶│ next │   ╰──▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘ │  ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #  ┌─────┐ │  │ item │▶│ 7 │ │ item │▶│ 3 │
        #  │‹new›│─╯  └──────┘ └───┘ └──────┘ └───┘
        #  └─────┘

        # V dalším kroku provážeme uzel ‹new› se zbytkem seznamu.
        # Atribut ‹top› ovšem stále odkazuje předchozí vrchol
        # zásobníku.

        new.next = self.top

        # Nová situace:
        #
        #     ╭─────────────────────────╮
        #     │                         ▼
        #  ┌─────┐    ┌──────┐       ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│ ╭─▶│ next │──────▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘ │  ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #  ┌─────┐ │  │ item │▶│ 7 │ │ item │▶│ 3 │
        #  │‹new›│─╯  └──────┘ └───┘ └──────┘ └───┘
        #  └─────┘

        # V posledním krok změníme odkaz (atribut) ‹top› tak, aby
        # ukazoval na nový vrchol.

        self.top = new

        # Atribut ‹top› a lokální proměnná ‹new› tak sdílí tutéž
        # hodnotu:

        #  ┌─────┐───▶┌──────┐       ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│ ╭─▶│ next │──────▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘ │  ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #  ┌─────┐ │  │ item │▶│ 7 │ │ item │▶│ 3 │
        #  │‹new›│─╯  └──────┘ └───┘ └──────┘ └───┘
        #  └─────┘

        # Návratem z metody ‹push› lokální proměnná ‹new› zanikne, a
        # atribut ‹top› zůstane jediným odkazem na (teď již nový)
        # vrchol zásobníku. K předchozímu vrcholu se dostaneme skrz
        # atribut ‹next› nového vrcholu:
        #
        #  ┌─────┐    ┌──────┐       ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│───▶│ next │──────▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘    ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #             │ item │▶│ 7 │ │ item │▶│ 3 │
        #             └──────┘ └───┘ └──────┘ └───┘

    # Druhou metodou je ‹pop›, která odstraní prvek (a
    # odpovídající uzel) ze zásobníku. V obecném případě můžeme
    # samozřejmě metodu ‹pop› volat v libovolném stavu zásobníku.
    # Pro ilustraci ale předpokládejme, že byla zavolána těsně po
    # ukončení výše vyobrazeného ‹push(7)›.

    def pop(self) -> Optional[int]:

        # Nejprve vyřešíme případ, kdy byl zásobník prázdný. To
        # poznáme tak, že atribut ‹top› je nastavený na ‹None›.
        # V takovém případě stav nijak neměníme, a pouze vrátíme
        # ‹None›, čím indikujeme volajícímu, že nebylo ze zásobníku
        # co odstranit.

        if self.top is None:
            return None

        # Na tomto místě již víme, že zásobník je neprázdný, a tedy
        # atribut ‹top› obsahuje nějaký vrchol. Nejprve si poznačíme
        # hodnotu, která je v tomto uzlu uložena:

        result = self.top.item

        # Po vykonání tohoto příkazu bude lokální proměnná ‹result›
        # sdílet hodnotu s atributem ‹top.item›:

        #  ┌─────┐    ┌──────┐       ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│───▶│ next │──────▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘    ├┄┄┄┄┄┄┤ ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #             │ item │▶│ 7 │ │ item │▶│ 3 │
        #             └──────┘ └───┘ └──────┘ └───┘
        #  ┌────────┐            ▲
        #  │‹result›│────────────╯
        #  └────────┘

        # Dále přesměrujeme atribut ‹top› na nový vrchol. Uvědomte
        # si, že je-li stav zásobníku X, po provedení dvojice
        # operací ‹push› a ‹pop› se tento vrátí do stejného stavu X.
        # Zejména bude mít tentýž vrchol jako před provedením obou
        # operací.

        self.top = self.top.next

        # Srovnejte následující situaci se situací vyobrazenou před
        # voláním ‹push› výše.

        #     ╭─────────────────────────╮
        #     │                         ▼
        #  ┌─────┐   ┌┄┄┄┄┄┄┐        ┌──────┐       ╭┄┄┄╮  ┌──────┐
        #  │‹top›│   ┆ next ┆┄┄┄┄┄┄┄▶│ next │──────▶┆ … ┆─▶│ None │
        #  └─────┘   ├┄┄┄┄┄┄┤  ┌───┐ ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯  └──────┘
        #            ┆ item ┆┄▶│ 7 │ │ item │▶│ 3 │
        #            └┄┄┄┄┄┄┘  └───┘ └──────┘ └───┘
        #  ┌────────┐            ▲
        #  │‹result›│────────────╯
        #  └────────┘

        # Všimněte si také, že na původní vrchol zásobníku již
        # neexistuje žádný odkaz (není uložen v žádné proměnné ani
        # atributu). V jazyce Python taková hodnota automaticky
        # zanikne. Zbývá už jen vrátit požadovanou hodnotu:

        return result

    # Po provedení dvojice volání ‹push› a ‹pop› se tedy dostaneme
    # do původního stavu. Ještě jednou zdůrazňujeme, že volání
    # ‹push› a ‹pop› nemusí být takto provázána vždy. Lze třeba
    # volat vícekrát za sebou ‹push›, nebo ‹pop›. Na vyobrazených
    # situacích to ve skutečnosti nic nemění, s výjimkou konkrétních
    # čísel uložených v zásobníku.

    #  ┌─────┐                    ┌──────┐       ╭┄┄┄╮   ┌──────┐
    #  │‹top›│───────────────────▶│ next │──────▶┆ … ┆──▶│ None │
    #  └─────┘                    ├┄┄┄┄┄┄┤ ┌───┐ ╰┄┄┄╯   └──────┘
    #                             │ item │▶│ 3 │
    #                             └──────┘ └───┘


def main() -> None:
    stack = Stack()
    assert stack.pop() is None
    stack.push(3)
    stack.push(7)
    v = stack.pop()
    assert v is not None
    assert v == 7


if __name__ == '__main__':
    main()
