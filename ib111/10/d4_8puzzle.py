from typing import List, Tuple, Optional, Dict

# † V této ukázce přidáme oproti předchozím několik novinek. Nejprve
# si ale představme problém, který budeme řešit. Možná znáte hru „15
# puzzle“ – hraje se s 15 posuvnými kameny v rámu o rozměru ⟦4×4⟧ –
# jedno místo tedy zůstává volné a umožňuje kameny posouvat. My
# budeme řešit o něco menší variantu této hry: 8 kamenů v rámečku
# ⟦3×3⟧. Na kamenech může být třeba obrázek, ale tradiční varianta,
# kterou budeme používat i my, má kameny očíslované od 1 do 8.
# Vyřešený rébus má tedy tuto podobu:
#
#  ┌───┬───┬───┐
#  │   │ 1 │ 2 │
#  ├───┼───┼───┤
#  │ 3 │ 4 │ 5 │
#  ├───┼───┼───┤
#  │ 6 │ 7 │ 8 │
#  └───┴───┴───┘

# Hra se hraje tak, že dostaneme pole nějak pomíchané a snažíme se
# sestavit jej do podoby nakreslené výše. K dispozici máme vždy
# několik tahů – můžeme si vybrat, který sousední kámen do prázdného
# políčka přemístit. Protože hra je ve své klasické podobě
# realizovaná fyzicky, přesouvat můžeme kameny pouze ve 4 směrech:
# nahoru, dolů, doleva a doprava. Příklad krátké hry:

#  ┌───┬───┬───┐ ┌───┬───┬───┐ ┌───┬───┬───┐ ┌───┬───┬───┐
#  │ 1 │ 4 │ 2 │ │ 1 │ 4 │ 2 │ │ 1 │   │ 2 │ │   │«1»│ 2 │
#  ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
#  │ 3 │ 5 │   │ │ 3 │   │«5»│ │ 3 │«4»│ 5 │ │ 3 │ 4 │ 5 │
#  ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
#  │ 6 │ 7 │ 8 │ │ 6 │ 7 │ 8 │ │ 6 │ 7 │ 8 │ │ 6 │ 7 │ 8 │
#  └───┴───┴───┘ └───┴───┴───┘ └───┴───┴───┘ └───┴───┴───┘

# Každý přípustný počáteční stav hry (konfigurace) má mnoho řešení:
# my budeme odpovídat na otázku, jak dlouhé je to nejkratší¹
# (s nejmenším počtem kroků). Nejprve si zadefinujeme několik
# užitečných typů a pomocných funkcí. Uspořádání rámečku (krabičky)
# budeme reprezentovat lineárním seznamem, a to tak, že vyřešená hra
# bude mít tvar ‹[0, 1, 2, 3, 4, 5, 6, 7, 8]›: hrací pole budeme
# odečítat ze seznamu po řádcích, vždy zleva doprava, prázdné
# políčko reprezentujeme nulou. Souřadnice políčka budou dvojice
# čísel z rozsahu ⟦⟨0, 2⟩⟧, přičemž ⟦(0, 0)⟧ je levý horní roh.

Box = List[int]
Position = Tuple[int, int]

# Tahy budeme reprezentovat jako «pohyb volného políčka» (rozmyslete
# si, že se jedná o ekvivalentní, ale úspornější popis, než si
# pamatovat který kámen tahal kterým směrem). Tento pohyb budeme
# zapisovat jako ‹(dx, dy)› – posuv ve směru ⟦x⟧ a ve směru ⟦y⟧
# samostatně. Po směru hodinových ručiček jsou to postupně dvojice
# ⟦(1, 0), (0, 1), (-1, 0), (0, -1)⟧.

Move = Tuple[int, int]


# Dále budeme potřebovat převádět mezi indexem v seznamu ‹Box› a
# souřadnicemi daného políčka. K tomu slouží následující dvě (čisté)
# funkce.

def to_index(position: Position) -> int:
    x, y = position
    return y * 3 + x


def to_position(index: int) -> Position:
    return (index % 3, index // 3)


# Dále si zadefinujeme (opět čistou) funkci, která nám pro daný tah
# vrátí ten opačný (když provedeme tah ‹m› a poté ‹opposite(m)›,
# nestane se nic – ujistěte se, že rozumíte, proč tomu tak je).

def opposite(move: Move) -> Move:
    shift_x, shift_y = move
    return (-shift_x, -shift_y)


# Základ herní mechaniky realizuje procedura ‹move_blank›, která
# v daném rozložení kamenů posune prázdné místo ve směru daném
# parametrem ‹move›. Pohyb realizuje výměnou hodnot na
# odpovídajících pozicích v seznamu, který hru reprezentuje.

def move_blank(box: Box, move: Move) -> None:
    shift_x, shift_y = move
    blank_idx = box.index(0)
    blank_pos = to_position(blank_idx)
    other_pos = (blank_pos[0] + shift_x, blank_pos[1] + shift_y)
    other_idx = to_index(other_pos)
    box[blank_idx], box[other_idx] = box[other_idx], box[blank_idx]


# Dále nás bude zajímat, je-li nějaký tah při daném rozložení kamenů
# přípustný, tzn. nepokusíme se přesunout neexistující kámen
# (umístěný mimo hrací plochu) do prázdného místa, které je zrovna
# na některém kraji. Tuto kontrolu realizuje predikát ‹admissible›.

def admissible(box: Box, move: Move) -> bool:
    move_x, move_y = move
    blank_x, blank_y = to_position(box.index(0))
    return (0 <= move_x + blank_x < 3 and
            0 <= move_y + blank_y < 3)


# Předposlední pomocná čistá funkce je ‹distance›, která nám řekne,
# kolikrát se daný kámen musí určitě posunout, aby se dostal na své
# správné místo. Protože kameny lze posouvat pouze v pravých úhlech,
# záleží pouze na počtu horizontálních a počtu vertikálních posunů
# samostatně. Uvažme například posuv ze souřadnic ⟦(2, 2)⟧ na
# souřadnice ⟦(1, 0)⟧ (šipky reprezentují směr pohybu). Je vidět, že
# určitě potřebujeme aspoň tři posuvy, co odpovídá naznačenému
# vzorci ⟦|x₁ - x₂| + |y₁ - y₂|⟧ – v našem příkladě tedy ⟦|2 - 1| +
# |2 - 0| = 1 + 2 = 3⟧. Přesun lze jistě realizovat i více kroky,
# nás ale bude zajímat minimum.

#  ┌───┬───┬───┐ ┌───┬───┬───┐ ┌───┬───┬───┐
#  │   │ × │ ← │ │   │ × │   │ │   │ × │   │
#  ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
#  │   │   │ ↑ │ │   │ ↑ │ ← │ │   │ ↑ │   │
#  ├───┼───┼───┤ ├───┼───┼───┤ ├───┼───┼───┤
#  │   │   │ ↑ │ │   │   │ ↑ │ │   │ ↑ │ ← │
#  └───┴───┴───┘ └───┴───┴───┘ └───┴───┴───┘

# Toto číslo odpovídá tzv. Manhattanské metrice² (vzdálenosti) mezi
# současnou a koncovou pozicí daného kamene.

def distance(box: Box, tile: int) -> int:
    want_x, want_y = to_position(tile)
    now_x, now_y = to_position(box.index(tile))
    return abs(want_x - now_x) + abs(want_y - now_y)


# Vyzbrojeni minimálním počtem kroků, které potřebujeme k přesunu
# daného kamene na své místo, se pokusíme odhadnout, kolik nejméně
# kroků potřebujeme k vyřešení celého rébusu. Tento odhad je
# naštěstí velmi jednoduchý: stačí si uvědomit, že přesunem jednoho
# kamene se ke své koncové pozici přiblíží «pouze tento kámen» a
# žádný jiný. Jistě se nám často stane, že kroků bude potřeba víc:
# to nám ale nebude vadit, důležité je pouze to, abychom měli dobrý
# spodní odhad.

def need_steps(box: Box) -> int:
    total = 0
    for tile in range(1, 9):
        total += distance(box, tile)
    return total


# Tím jsou pomocné funkce vyřešeny a můžeme se pustit do samotného
# hledání nejkratšího řešení. Stejně jako v předchozích ukázkách,
# budeme používat rekurzi a backtracking, ale objeví se zde i
# slibované novinky.

#  1. Dosud jsme všechny prohledávací algoritmy realizovali jako
#     čisté funkce.  Prohledávací algoritmus pro „8 puzzle“ má ale
#     «sdílený stav»: efektivní řešení tohoto rébusu vyžaduje,
#     abychom sdíleli informace mezi jednotlivými podvýpočty. To nám
#     umožní ty, o kterých z předchozího prohledávání víme, že
#     nevedou k cíli, rychle zamítnout.
#  2. Protože beztak je výpočet realizován procedurou, nebudeme pro
#     každý tah vytvářet novou (upravenou) kopii stavu hry: místo
#     toho si budeme pamatovat pouze «sekvenci tahů» jako
#     explicitní zásobník a hrací plochu budeme upravovat «in situ»
#     (na místě). Ušetříme tak značné množství práce.

# Sdílený stav zapouzdříme do «třídy», která bude mít následovné
# atributy:
#
#  • ‹best›: délka dosud nalezeného nejlepšího řešení (k vyřešení
#    hry s nejdelším optimálním řešením je potřeba 31 tahů³ – toto
#    číslo tedy použijeme jako počáteční horní odhad pro délku),
#  • ‹found›: nastavíme na ‹True› jakmile nalezneme libovolné
#    řešení,
#  • ‹moves›: zmiňovaný zásobník tahů, které jsme provedli
#    z počáteční konfigurace, a který nám umožní efektivně se ve
#    výpočtu vracet,
#  • ‹box›: aktuálně zkoumaná herní pozice,
#  • ‹visited›: slovník,⁴ ve kterém si budeme pamatovat již objevené
#    herní pozice (konfigurace hrací plochy) a v kolika krocích
#    jsme k nim z té počáteční došli (tento slovník nám umožní
#    přeskočit velkou část redundantních podstromů).

class Solver:
    def __init__(self, initial: Box):
        self.best = 31
        self.found = False
        self.moves: List[Move] = []
        self.box = initial[:]
        self.visited: Dict[Tuple[int, ...], int] = {}

    # Následující dvě metody realizují provedení jednoho tahu
    # (‹apply›) resp. jeho vrácení (‹backtrack›). Všimněte si, že
    # jsou to jediné dvě metody, které přímo modifikují jak aktuální
    # hrací pole, tak zásobník tahů.

    def apply(self, move: Move) -> None:
        self.moves.append(move)
        move_blank(self.box, move)

    def backtrack(self) -> None:
        move_blank(self.box, opposite(self.moves.pop()))

    # Samotné rekurzivní hledání realizuje metoda-procedura
    # ‹search›.

    def search(self) -> None:

        # Struktura rekurzivního řešení je stále zachována. Nejprve
        # jednoduché (přímo řešitelné nebo nezajímavé) případy. Ten
        # první jednoduchý případ je ale nového typu: nacházíme-li
        # se v konfiguraci, kterou jsme již někdy v minulosti
        # (v jiném podstromě) navštívili, zjistíme, kolik kroků jsme
        # na to v minulosti potřebovali (jak hluboko ve stromě se
        # nacházela).

        # Podstrom, který je na dané konfiguraci „zavěšen“ je totiž
        # vždy stejný: má smysl jej prohledávat pouze v případě, že
        # jsme tuto konfiguraci ještě nikdy nepotkali, nebo ji
        # potkali pouze ve větší hloubce. V tom druhém případě si
        # totiž celkovou délku cesty k řešení zkrátíme. Uvažme
        # například tuto situaci (⟦i⟧ je počáteční konfigurace, ⟦c⟧
        # je současná konfigurace, která se ve stromě opakuje, ⟦s⟧
        # je vyřešený rébus):

        #                                ╭───▶ …
        #                                │
        #        ╭────▶●────▶●────▶●────▶●────▶●───▶ …
        #        │                ⟦c₁⟧   │
        #        │                       ╰────▶●────▶●
        #        │           ╭───▶ …                ⟦s₁⟧
        #        │           │
        #  ●────▶●────▶●────▶●────▶●───▶ …
        # ⟦i⟧         ⟦c₂⟧   │
        #                    ╰────▶●────▶●
        #                               ⟦s₂⟧

        # Je vidět, že navštívíme-li uzel ⟦c₁⟧ jako první, má smysl
        # uzel ⟦c₂⟧ prohledat, protože cesta z ⟦i⟧ do ⟦s₂⟧ je
        # kratší, než cesta z ⟦i⟧ do ⟦s₁⟧ kterou jsme již našli.
        # Naopak, dostaneme-li se do uzlu ⟦c₁⟧ poté, co jsme již
        # ⟦c₂⟧ navštívili, nemůžeme touto cestou žádné lepší řešení
        # než je ⟦s₂⟧ nalézt a tento podstrom můžeme celý zamítnout.

        # Není-li konfigurace rovnou zamítnuta, nezapomeneme si pro
        # pozdější výpočet poznačit její hloubku do atributu
        # ‹self.visited›.

        key = tuple(self.box)

        if key in self.visited:
            if self.visited[key] <= len(self.moves):
                return

        self.visited[key] = len(self.moves)

        # Druhý jednoduchý případ je již dobře známého typu: nalezli
        # jsme řešení. Zároveň si poznačíme jeho hloubku v případě,
        # že se jedná o řešení zatím nejlepší (nejkratší).

        if self.box == list(range(0, 9)):
            self.best = min(self.best, len(self.moves))
            self.found = True
            return

        # Poslední jednoduchý případ je ten, kdy již víme, že
        # nejkratší možná cesta ze současného stavu k řešení je
        # delší, než ta zatím nejlepší nalezená. K tomu s výhodou
        # použijeme pomocnou funkci ‹need_steps›, kterou jsme si
        # dříve definovali. Připomeňme si, že tato nám dává «spodní
        # odhad» na délku cesty k řešení: je-li tento příliš dlouhý,
        # skutečná délka bude jistě také.

        if len(self.moves) + need_steps(self.box) > self.best:
            return

        # Zbývá vyřešit případy, o kterých nelze přímo říct nic.
        # Rekurzivně tedy prohledáme podstromy, do kterých vedou
        # jednotlivé přípustné tahy. Najdeme-li v některé větvi nové
        # nejlepší řešení, rekurzivní volání tuto skutečnost poznačí
        # do atributů ‹best› a ‹found›.

        for move in ((1, 0), (0, 1), (-1, 0), (0, -1)):
            if admissible(self.box, move):
                self.apply(move)
                self.search()
                self.backtrack()

    # Pomocná metoda-procedura, která spustí hledání a vrátí jeho
    # celkový výsledek: ‹None› v případě, kdy řešení neexistuje,
    # jinak délku toho nejlepšího možného.

    def solve(self) -> Optional[int]:
        self.search()
        return self.best if self.found else None


# Hotové řešení jako obvykle otestujeme na několika příkladech.

def main() -> None:  # demo
    assert Solver([0, 1, 2,
                   3, 4, 5,
                   6, 7, 8]).solve() == 0
    assert Solver([1, 0, 2, 3, 4, 5, 6, 7, 8]).solve() == 1
    assert Solver([1, 2, 0, 3, 4, 5, 6, 7, 8]).solve() == 2
    assert Solver([1, 2, 5, 3, 4, 0, 6, 7, 8]).solve() == 3
    assert Solver([1, 2, 5, 3, 0, 4, 6, 7, 8]).solve() == 4
    assert Solver([1, 0, 5, 3, 2, 4, 6, 7, 8]).solve() == 5
    assert Solver([0, 1, 5, 3, 2, 4, 6, 7, 8]).solve() == 6
    assert Solver([0, 8, 6, 5, 4, 7, 2, 3, 1]).solve() == 30
    assert Solver([8, 0, 6, 5, 4, 7, 2, 3, 1]).solve() == 31


# ¹ V mnoha případech existuje víc než jedno nejkratší řešení, to na
# náš úkol ale nemá zásadní vliv, protože nás zajímá pouze jejich
# délka, kterou mají samozřejmě všechny společnou.

# ² Můžete si ji prostudovat online, pro pochopení řešení hry si ale
# vystačíte s informacemi zde uvedenými.

# ³ Počet tahů není vůbec jednoduché odvodit teoreticky. Horní mez
# 31 tahů byla určena výpočetně, vyhledáním optimálního řešení
# z každého přípustného herního stavu. Pro hru „15 puzzle“ je tato
# mez 80 tahů (opět získána výpočetně). Znalost dobrého horního
# odhadu na délku řešení je pro efektivitu našeho algoritmu klíčová:
# pro zobecnění hry na ⟦n×n⟧ políček, kdy podobně dobrý odhad
# nemáme, je potřeba použít mírně sofistikovanější algoritmus. Jeho
# základní myšlenkou je nějakou mez zvolit, a nenajdeme-li v této
# mezi žádné řešení, postupně ji zvyšovat. To, jestli «nějaké»
# řešení existuje lze zjistit snadno z počáteční konfigurace, bez
# prohledávání.

# ⁴ Tento slovník má trochu zvláštní typ. Je to proto, že seznam
# nelze použít jako klíč: seznam (typ ‹Box›) tedy musíme převést na
# ⟦n⟧-tici, kterou již můžeme použít jako klíč. Zápis s třemi
# tečkami říká, že ⟦n⟧-tice obsahuje nějaký počet celých čísel,
# který není blíže určený.

if __name__ == '__main__':
    main()
