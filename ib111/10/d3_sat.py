from typing import List, Tuple, Set, Dict, Optional

# Výrokovou logiku jistě znáte, například z předmětu MZI. To co
# možná nevíte je, že každou formuli výrokové logiky lze přepsat do
# obzvláště jednoduchého tvaru: takzvané «konjunktivní normální
# formy». V této formě se formule skládá ze závorek (klauzulí),
# které jsou spojeny konjunkcí. V každé závorce je pak disjunkce
# «literálů»: proměnných, nebo jejich negací. Například:
#
# ⟦ (a ∨ b) ∧ (¬a ∨ c) ∧ (¬a ∨ ¬b ∨ c) ⟧

# To, jak se formule do této podoby převede nás teď nemusí zajímat
# (někdy později v průběhu studia to nejspíš ještě zjistíte), co je
# důležité je, že nám stačí pracovat s formulemi tohoto tvaru.

# Jak takové formule reprezentovat v programu? Vybudujeme si vhodné
# typy odspodu, tzn. od samotných proměnných, které budeme
# reprezentovat písmeny:

Variable = str

# Literál budeme reprezentovat dvojicí: krom proměnné si potřebujeme
# pamatovat, je-li literál «pozitivní» (pozitivní je, když proměnné
# nepředchází negace): na toto nám stačí hodnota typu ‹bool›.

Literal = Tuple[Variable, bool]

# Dalším útvarem je klauzule, tedy disjunkce nějakého počtu
# literálů:

Clause = List[Literal]

# A konečně samotná formule, která je konjunkcí klauzulí:

Formula = List[Clause]

# Zbývá poslední typ, který budeme potřebovat, a tím je «valuace»:
# přiřazení pravdivostních hodnot jednotlivým proměnným.

Valuation = Dict[str, bool]


# Problém, který budeme řešit se jmenuje «splnitelnost»: bude nás
# zajímat, existuje-li valuace taková, že se zadaná formule
# vyhodnotí na ‹True›. Nejprve si ale naprogramujeme jednodušší
# funkci: «vyhodnocení» formule, kterého vstupem je nějaká formule a
# valuace proměnných, a výsledkem je pravdivostní hodnota. Budeme
# navíc ale uvažovat i případ, kdy valuace není úplná, tzn. některé
# proměnné nemají pravdivostní hodnotu určenu. V takovém případě
# můžou nastat tři případy:
#
#  1. formule je pravdivá bez ohledu na nepřiřazené proměnné
#     (v každé klauzuli je alespoň jeden splněný literál),
#  2. formule je nepravdivá: existuje klauzule, která obsahuje pouze
#     přiřazené proměnné a zároveň není splněna,
#  3. o pravdivosti nelze rozhodnout: některou klauzuli se nepovedlo
#     splnit, ale tato klauzule obsahuje nerozhodnutou proměnnou.
#
# Funkce ‹evaluate› bude v těchto situacích vracet postupně ‹True›
# (určitě splněno), ‹False› (určitě nesplněno) a ‹None› (nevíme).

def evaluate(phi: Formula, valuation: Valuation) -> Optional[bool]:

    undecided_clause = False

    # Formuli budeme vyhodnocovat po jednotlivých klauzulích.
    # Výsledek pro každou z nich může být, podobně jako pro celou
    # formuli, „splněna“, „nesplněna“ nebo „nelze říct“.

    for clause in phi:
        satisfied = False
        undecided_literal = False

        for variable, positive in clause:
            if variable not in valuation:
                undecided_literal = True
            elif valuation[variable] == positive:
                satisfied = True
                break

        # V případě, že se klauzuli nepovedlo splnit, musíme
        # rozlišit dva případy: jestli tato obsahovala nerozhodnutý
        # literál (příslušná proměnná nemá přiřazenu pravdivostní
        # hodnotu), výsledek pro klauzuli je „nelze říct“ a
        # pokračujeme ve vyhodnocování (může se totiž ještě objevit
        # klauzule, která formuli rozhodne v záporu). Jsou-li ale
        # všechny proměnné v klauzuli přiřazené, víme, že formule
        # jako celek se vyhodnotí na ‹False› a tento výsledek můžeme
        # rovnou vrátit.

        if not satisfied:
            if undecided_literal:
                undecided_clause = True
            else:
                return False

    # Žádná klauzule se nevyhodnotila na ‹False›, pro formuli jako
    # celek zbývají tedy pouze možnosti „splněna“ nebo „nelze říct“.
    # Druhá možnost nastane v případě, kdy se nám některou klauzuli
    # nepodařilo rozhodnout.

    return None if undecided_clause else True


# Dále budeme potřebovat (čistou) funkci, která nám z formule získá
# množinu všech proměnných, které se ve formuli objevují.

def variables(phi: Formula) -> Set[str]:
    var_set: Set[str] = set()
    for clause in phi:
        for var, _ in clause:
            var_set.add(var)
    return var_set


# Poslední pomocnou funkcí (opět čistou) bude ‹extend›, která
# do valuace přidá novou proměnnou. Vstupní podmínkou je, že tato
# proměnná ještě ve valuaci hodnotu přiřazenou nemá.

def extend(val: Valuation, var: str, value: bool) -> Valuation:
    assert var not in val
    new = val.copy()
    new[var] = value
    return new


# Nyní již můžeme přistoupit k samotnému řešení problému: možná si
# pamatujete «pravdivostní tabulky» – jejich konstrukcí lze
# jednoduše zjistit, je-li formule splnitelná. K tomu nám totiž
# stačí nalézt splňující přiřazení (tedy takové, při kterém se
# formule vyhodnotí na ‹True›). Pro ⟦φ = (a ∨ b) ∧ (¬a ∨ c) ∧ (¬a ∨
# ¬b ∨ c) ⟧ vypadá pravdivostní tabulka takto:

# │ ⟦a⟧ │ ⟦b⟧ │ ⟦c⟧ │ ⟦φ⟧ │
# ├─────┼─────┼─────│─────┤
# │   0 │   0 │   0 │   0 │
# │   0 │   0 │   1 │   0 │
# │   0 │   1 │   0 │   1 │
# │   0 │   1 │   1 │   1 │
# │   1 │   0 │   0 │   0 │
# │   1 │   0 │   1 │   1 │
# │   1 │   1 │   0 │   0 │
# │   1 │   1 │   1 │   1 │

# Potřebujeme tedy algoritmus, který takovou tabulku sestrojí a
# najde první řádek, kde formuli jako celku náleží hodnota 1 (neboli
# ‹True›). Jak již jistě tušíte, použijeme rekurzi. Budeme si přitom
# předávat dvě pomocné hodnoty: seznam proměnných, jejichž
# pravdivost ještě potřebujeme rozhodnout, a částečnou valuaci,
# kterou budeme postupně budovat. Význam predikátu ‹satisfiable_rec›
# je „lze přiřazení ‹valuation› doplnit tak, aby formuli splnilo?“

def satisfiable_rec(phi: Formula, to_decide: List[str],
                    valuation: Valuation) -> bool:

    # Jako obvykle, nejprve vyřešíme jednoduchý případ, totiž ten,
    # kdy již formuli dokážeme rozhodnout. Tento případ zejména
    # nastane, je-li již přiřazení ‹valuation› kompletní a tedy
    # seznam ‹to_decide› prázdný.

    # Může se ale stát, že formuli dokážeme rozhodnout i přesto, že
    # jsme dosud nepřiřadili pravdivostní hodnoty všem proměnným.
    # Toto odpovídá třeba hned první dvojici řádků tabulky výše: na
    # hodnotě ⟦c⟧ vůbec nezáleží, a při vyhodnocování druhého sloupce
    # prvního řádku zjistíme, že „tudy cesta nevede“: můžeme rovnou
    # skočit na řádek třetí.

    result = evaluate(phi, valuation)
    if result is not None:
        return result

    # V případě, že zatím rozhodnout nelze, z ‹to_decide› vybereme
    # proměnnou, které následně přisoudíme pravdivostní hodnotu.

    var = to_decide[0]
    remaining = to_decide[1:]

    # Vybrané proměnné můžeme přisoudit hodnotu ‹True› nebo ‹False›,
    # čím dostaneme dvě (striktně úplnější) valuace: nazveme je
    # ‹val_true› a ‹val_false›.

    val_true = extend(valuation, var, True)
    val_false = extend(valuation, var, False)

    # Konečně přiřazení ‹valuation› lze na splňující přiřazení
    # doplnit právě tehdy, když lze takto doplnit alespoň jedno
    # z rozšířených přiřazení ‹val_true› nebo ‹val_false›. Zároveň
    # je zřejmé, že instance, které řešíme rekurzí jsou jednodušší:
    # zbývá o jednu nerozhodnutou proměnnou méně.

    return (satisfiable_rec(phi, remaining, val_true) or
            satisfiable_rec(phi, remaining, val_false))


# Není již těžké si uvědomit, že formule je splnitelná právě když
# lze prázdnou valuaci rozšířit na valuaci splňující:

def satisfiable(phi: Formula) -> bool:
    return satisfiable_rec(phi, list(variables(phi)), {})


# Tím jsme hotovi, implementaci si ještě na několika formulích
# otestujeme. Aby se nám formule trochu lépe četly, zadefinujeme si
# pro jejich vytváření dvě jednoduché pomocné funkce (‹positive› a
# ‹negative›).

def positive(var: str) -> Literal:
    return (var, True)


def negative(var: str) -> Literal:
    return (var, False)


def main() -> None:  # demo
    phi_1 = [[positive('a'), positive('b')],
             [negative('a'), positive('c')],
             [negative('a'), negative('b'), positive('c')]]
    assert satisfiable(phi_1)

    phi_2 = [[positive('a')], [negative('a')]]
    assert not satisfiable(phi_2)

    phi_3 = [[positive('a'), positive('b')],
             [negative('a'), positive('b')],
             [positive('a'), negative('b')],
             [negative('a'), negative('b')]]
    assert not satisfiable(phi_3)

    phi_4 = [[positive('a'), positive('b'), positive('c')],
             [negative('a'), positive('b'), negative('c')],
             [positive('a'), negative('b'), negative('c')],
             [positive('a'), negative('b'), positive('c')],
             [negative('a'), negative('b'), negative('c')],
             [negative('a'), positive('c')],
             [positive('a'), negative('c')]]
    assert not satisfiable(phi_4)

    phi_5 = [[positive('a'), positive('b'), positive('c')],
             [negative('a'), positive('b'), negative('c')],
             [positive('a'), negative('b'), positive('c')],
             [negative('a'), negative('b'), negative('c')]]
    assert satisfiable(phi_5)


if __name__ == '__main__':
    main()
