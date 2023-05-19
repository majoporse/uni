from typing import Tuple, List, Optional

# V tomto příkladu se vrátíme k „minmax“ stromům z ‹09/minmax.py› a
# zejména k jejich praktické aplikaci. Strom už nicméně nebudeme
# reprezentovat explicitně jako datovou strukturu, budeme jej vždy
# konstruovat „podle potřeby“ lokálně, v rámci rekurzivního řešení
# nějakého problému.

# Problém, který budeme řešit je jak vyhrát (nebo aspoň neprohrát)
# piškvorky na ploše ⟦3×3⟧ (v angličtině známé jako „tic-tac-toe“).
# Tato hra je dost jednoduchá na to, abychom dokázali řešení najít i
# celkem naivně.

# Jak si jistě pamatujete z minula, v „minmax“ stromu se střídají
# „min“ uzly a „max“ uzly: my teď do každého uzlu umístíme hrací
# plán: do uzlů typu „max“ takový, kde jsme na tahu my (hráč
# s křížky) a do uzlů typu „min“ pak ty, kde je na tahu hráč
# s kolečky (náš protivník). Zbývá nám ještě ohodnotit listy, které
# budou reprezentovat ukončené hry (některý hráč vyhrál, nebo je
# plocha již zaplněná a došlo tedy k remíze). To provedeme tak, že
# remízu ohodnotíme nulou (neutrální výsledek), výhru křížků
# ohodnotíme ⟦+1⟧ (pozitivní) a výhru koleček ⟦-1⟧ (negativní)
# výsledek. Takový strom můžeme zřejmě nakreslit z libovolné herní
# pozice. Například (poslední tah je vždy vybarven, u vnitřních uzlů
# uvádíme jejich vypočtené hodnoty):

#                               ┌───┬───┬───┐ ┌───┬───┬───┐
#                               │ × │ × │ ○ │ │ × │ × │ ○ │
#                               ├───┼───┼───┤ ├───┼───┼───┤
#                      ┌───────▶│❮○❯│ ○ │ × │▶│ ○ │ ○ │ × │ 0
#                ┌───┬───┬───┐  ├───┼───┼───┤ ├───┼───┼───┤
#                │❮×❯│ × │ ○ │  │ × │   │ ○ │ │ × │❮×❯│ ○ │
#                ├───┼───┼───┤  └───┴───┴───┘ └───┴───┴───┘
#        ┌──────▶│   │ ○ │ × │ 0
#        │       ├───┼───┼───┤  ┌───┬───┬───┐ ┌───┬───┬───┐
#        │       │ × │   │ ○ │  │ × │ × │ ○ │ │ × │ × │ ○ │
#        │       └───┴───┴───┘  ├───┼───┼───┤ ├───┼───┼───┤
#        │             └───────▶│   │ ○ │ × │▶│❮×❯│ ○ │ × │ 1
#        │                      ├───┼───┼───┤ ├───┼───┼───┤
#        │                      │ × │❮○❯│ ○ │ │ × │ ○ │ ○ │
#        │                      └───┴───┴───┘ └───┴───┴───┘
#        │                      ┌───┬───┬───┐
#        │                      │❮○❯│ × │ ○ │
#        │                      ├───┼───┼───┤
#        │             ┌───────▶│ × │ ○ │ × │ -1
#  ┌───┬───┬───┐ ┌───┬───┬───┐  ├───┼───┼───┤
#  │   │ × │ ○ │ │   │ × │ ○ │  │ × │   │ ○ │
#  ├───┼───┼───┤ ├───┼───┼───┤  └───┴───┴───┘
#  │   │ ○ │ × │▶│❮×❯│ ○ │ × │ -1
#  ├───┼───┼───┤ ├───┼───┼───┤  ┌───┬───┬───┐ ┌───┬───┬───┐
#  │ × │   │ ○ │ │ × │   │ ○ │  │   │ × │ ○ │ │❮×❯│ × │ ○ │
#  └───┴───┴───┘ └───┴───┴───┘  ├───┼───┼───┤ ├───┼───┼───┤
#        │  0          └───────▶│ × │ ○ │ × │▶│ × │ ○ │ × │ 1
#        │                      ├───┼───┼───┤ ├───┼───┼───┤
#        │                      │ × │❮○❯│ ○ │ │ × │ ○ │ ○ │
#        │                      └───┴───┴───┘ └───┴───┴───┘
#        │                      ┌───┬───┬───┐
#        │                      │❮○❯│ × │ ○ │
#        │                      ├───┼───┼───┤
#        │             ┌───────▶│   │ ○ │ × │ -1
#        │       ┌───┬───┬───┐  ├───┼───┼───┤
#        │       │   │ × │ ○ │  │ × │ × │ ○ │
#        │       ├───┼───┼───┤  └───┴───┴───┘
#        └──────▶│   │ ○ │ × │ -1
#                ├───┼───┼───┤  ┌───┬───┬───┐ ┌───┬───┬───┐
#                │ × │❮×❯│ ○ │  │   │ × │ ○ │ │❮x❯│ × │ ○ │
#                └───┴───┴───┘  ├───┼───┼───┤ ├───┼───┼───┤
#                      └───────▶│❮○❯│ ○ │ × │▶│ ○ │ ○ │ × │ 0
#                               ├───┼───┼───┤ ├───┼───┼───┤
#                               │ × │ × │ ○ │ │ × │ × │ ○ │
#                               └───┴───┴───┘ └───┴───┴───┘
#       max           min            max           min

# Jak nám takový strom pomůže vyhrát? Střídající se minima a maxima
# v jednotlivých patrech stromu odpovídají nejlepším možným tahům
# příslušného hráče: dojdeme-li do listu s hodnotou -1, znamená to,
# že kolečka vyhrála (tomuto hráči budeme odteď říkat „min“). Cílem
# hráče „min“ je tedy dostat se do listu ohodnoceného -1. Naopak,
# hráč s křížky (bude se jmenovat „max“) se pokouší dostat do listu
# ohodnoceného +1. Toto odpovídá elementárním případům rekurze.

# Stojí-li hráč před posledním rozhodnutím (uvažme třeba
# nejspodnější případ z druhého sloupce obrázku, kde se hráč „min“
# rozhoduje mezi dvěma políčky), vybere si tu z nich, která povede k
# výhře (je-li to možné), případně k remíze. Je vidět, že to
# odpovídá právě následníkovi s nejmenší hodnotou (pro hráče „min“,
# u hráče „max“ je tomu přesně naopak). Totéž samozřejmě platí i o
# patro výš, a tak dále, až ke kořeni.


# Abychom mohli takový pomyslný „minmax“ strom prohledat, musíme
# umět reprezentovat jeho jednotlivé vrcholy: ty neobsahují nic
# jiného, než herní pozice. Ty budeme reprezentovat dvourozměrným
# seznamem čísel. Prázdná políčka budou mít hodnotu 0, hráči pak
# budou používat „svoji“ hodnotu: hráč „min“ dostane -1 a hráč „max“
# +1. Jednotlivý tah pak budeme reprezentovat jako dvojici ⟦(x, y)⟧
# souřadnic, každou z rozsahu ⟦⟨0, 2⟩⟧.

Plan = List[List[int]]
Move = Tuple[int, int]


# První pomocnou funkci, kterou si zadefinujeme, bude čistá funkce
# ‹put›, která dostane plán, souřadnice tahu, a hráče, a vytvoří nový
# plán takový, kde zadaný hráč obsadil zadané políčko. Vstupní
# podmínkou je, že políčko bylo prázdné.

def put(plan: Plan, where: Move, player: int) -> Plan:
    x, y = where
    assert plan[y][x] == 0
    plan = [row[:] for row in plan]
    plan[y][x] = player
    return plan


# Čistá funkce ‹list_empty› vytvoří seznam všech přípustných tahů
# (tzn. souřadnice všech prázdných políček v předané hrací ploše).

def list_empty(plan: Plan) -> List[Move]:
    return [(x, y)
            for x in range(3)
            for y in range(3)
            if not plan[y][x]]


# Další (opět čistá) funkce bude ‹line›, která na vstupu dostane
# počáteční souřadnice (parametry ‹x› a ‹y›) a „směr“ (parametry
# ‹dx› a ‹dy›, které udávají požadovaný přírůstek na dané
# souřadnici). Z těchto spočítá, je-li celá takto popsaná „čára“
# obsazena týmž hráčem.  Pokud ano, vrátí identifikátor hráče, jinak
# nulu. Tato situace zřejmě odpovídá (nějaké) vítězné pozici.

def line(plan: Plan, x: int, y: int, dx: int, dy: int) -> int:
    player = plan[y][x]
    for n in range(1, 3):
        if plan[y + dy * n][x + dx * n] != player:
            return 0
    return player


# Následuje pomocná funkce, která vrátí svůj první nenulový
# parametr,¹ existuje-li takový (jinak vrátí nulu).

def either(a: int, b: int) -> int:
    return a if a else b


# Poslední pomocnou funkcí je ‹winner›, která rozhodne, zda některý
# hráč již vyhrál, a pokud ano, který. Určitě to není nejkrásnější
# funkce v historii funkcí, ale účel plní a je relativně kompaktní
# (a to je občas také žádoucí).

def winner(plan: Plan) -> int:
    player = 0
    for v in range(3):
        player = either(player, line(plan, v, 0, 0, 1))
        player = either(player, line(plan, 0, v, 1, 0))
    player = either(player, line(plan, 0, 0, 1, 1))
    player = either(player, line(plan, 2, 0, -1, 1))
    return player


# Tím jsme vybaveni k implementaci samotného rekurzivního
# prohledávání „minmax“ stromu hry tic-tac-toe.

def decide(plan: Plan, player: int) -> Tuple[int, Optional[Move]]:

    # Jak jsme již zvyklí, vyřešíme nejprve jednoduché případy,
    # totiž ty, kdy se nacházíme v listu. Listy jsou dvojího typu:
    # některý hráč vyhrál, nebo je pole již plné a nastala remíza.

    won = winner(plan)
    empty = list_empty(plan)
    moves = []
    if won or len(empty) == 0:
        return (won, None)

    # Nejsme-li v listu, musíme prohledat následníky. Následník se
    # od aktuálního vrcholu odlišuje tím, že hráč, který je na tahu
    # do některého volného pole umístí svůj symbol. Následníků je
    # právě tolik, kolik je volných políček. Nesmíme zapomenout, že
    # na tahu bude v rekurzivním volání opačný hráč, než je ten
    # současný. Krom skóre, které danému uzlu přisoudí rekurzivní
    # volání si zapamatujeme i tah, který do tohoto uzlu vedl.

    for move in empty:
        score, _ = decide(put(plan, move, player), -player)
        moves.append((score, move))

    # Nyní již máme výsledky pro všechny následníky: vybereme ten
    # nejlepší možný – hráč „max“ ten maximální, zatímco hráč „min“
    # ten minimální. Všimněte si, že vybíráme ze seznamu, který
    # obsahuje dvojice (skóre, tah). Je-li několik ekvivalentních
    # možností (mají stejné skóre), hráč „min“ vybere ten s
    # nejmenšími a hráč „max“ ten s největšími souřadnicemi. Protože
    # na konkrétní volbě nezáleží, můžeme si tuto zápisovou zkratku
    # na tomto místě dovolit.

    return max(moves) if player > 0 else min(moves)


# Tím je hra tic-tac-toe vyřešena: máme algoritmus, který hraje
# „nejlépe, jak je to možné“ – může-li v nějaké pozici vynutit
# výhru, nebo alespoň remízu, ‹decide› vybere právě takové tahy, aby
# ji skutečně vynutil.


# Výjimečně si krom jednoduchých automatických testů přidáme i
# možnost hry vypisovat na obrazovku. Pomocná funkce ‹draw› přidá do
# rozpracovaného obrázku hry další tah.

def draw(plan: Plan, game: str) -> str:
    out = ''
    for row, game_row in zip(plan, game.split('\n')):
        game_row += ' │ ' if game_row else ' '
        for cell in row:
            game_row += '×' if cell > 0 else \
                        '○' if cell < 0 else '_'
        out += game_row + '\n'
    return out


# A konečně funkce ‹play› nechá hrát strategii ‹decide› samu proti
# sobě a výsledek nakreslí. Parametry jsou počáteční pozice a hráč,
# který je na tahu. V parametru ‹game› si funkce udržuje „obrázek“
# hry, který na konci vrátí. Všimněte si, že tato funkce s výhodou
# využívá koncové rekurze.

def play(plan: Plan, player: int, game: str = '\n\n') -> str:
    game = draw(plan, game)
    _, move = decide(plan, player)

    if move is None:
        return game

    plan = put(plan, move, player)
    return play(plan, -player, game)


def main() -> None:  # demo

    # Nejprve si vykreslíme několik jednoduchých her. Zkuste si hry
    # upravit a rozmyslete si, proč ‹decide› hraje zrovna takto.

    print(play([[-1, +0, +0],
                [+0, +1, +0],
                [+0, +1, -1]], 1))
    print(play([[-1, +0, +1],
                [+0, +0, +0],
                [+0, +1, -1]], 1))
    print(play([[-1, +0, +1],
                [+0, +0, +0],
                [-1, +1, +0]], 1))

    # První dva testy odpovídají obrázku ze začátku příkladu.
    # Ty zbývající nejsou příliš intuitivní (proto jsme si
    # nechali hry vykreslovat), nicméně odpovídají konkrétním
    # volbám, které algoritmus provede.

    assert decide([[+0, +1, -1],
                   [+0, -1, +1],
                   [+1, +1, -1]], -1) == (-1, (0, 0))

    assert decide([[+0, +1, -1],
                   [+0, -1, +1],
                   [+1, +0, -1]], +1) == (0, (0, 0))

    assert decide([[-1, +0, +1],
                   [+0, +0, +0],
                   [+0, +1, -1]], 1) == (1, (1, 1))

    assert decide([[-1, +0, +1],
                   [+0, +0, +0],
                   [-1, +1, +0]], 1) == (0, (0, 1))


# ¹ V Pythonu by bylo lze stejného efektu docílit použitím operátoru
# ‹or›, nicméně se jedná o docela atypickou vlastnost jazyka, proto
# se zde takovému použití raději vyhneme.

if __name__ == '__main__':
    main()
