from typing import Optional, Set


# Binární rozhodovací diagram (anglicky „binary decision diagram“,
# zkráceně „BDD“) je datová struktura, která umožňuje efektivně
# kódovat formule výrokové logiky, například:
#
#   ⟦ φ = a ∨ (b ∧ c) ⇒ (a ∧ c) ⟧
#
# Protože budeme takto zapsané funkce pouze vyhodnocovat, můžeme se
# na BDD dívat jako na binární strom,¹ který má ve vnitřních uzlech
# názvy proměnných a v listech pravdivostní hodnoty (budeme je
# reprezentovat hodnotami ‹0› a ‹1›). BDD pro výše uvedenou formuli
# může vypadat například takto:
#
#                             ╭───╮
#               ╭─────────────│ a │─────────────╮
#               ▼           0 ╰───╯ 1           ▼
#             ╭───╮                           ╭───╮
#       ╭─────│ b │─────╮               ╭─────│ c │─────╮
#       ▼   0 ╰───╯ 1   ▼               ▼   0 ╰───╯ 1   ▼
#     ┌───┐           ╭───╮           ┌───┐           ┌───┐
#     │ 1 │     ╭─────│ c │─────╮     │ 0 │           │ 1 │
#     └───┘     ▼   0 ╰───╯ 1   ▼     └───┘           └───┘
#             ┌───┐           ┌───┐
#             │ 1 │           │ 0 │
#             └───┘           └───┘
#
# BDD vyhodnotíme tak, že začneme v kořenu, a v každém uzlu se
# rozhodneme podle pravdivosti proměnné, kterou je tento uzel
# označený: je-li pravdivá, pokračujeme doprava, jinak doleva.
# Výsledkem je hodnota, kterou najdeme v takto nalezeném listu.
# Srovnejte tabulku pravdivostních hodnot:
#
# │ a │ b │ c │ b ∧ c │ a ∨ (b ∧ c) │ a ∧ c │ φ │
# ├───┼───┼───│───────│─────────────│───────│───│
# │ 0 │ 0 │ 0 │   0   │      0      │   0   │ 1 │
# │ 0 │ 0 │ 1 │   0   │      0      │   0   │ 1 │
# │ 0 │ 1 │ 0 │   0   │      0      │   0   │ 1 │
# │ 0 │ 1 │ 1 │   1   │      1      │   0   │ 0 │
# │┄┄┄│┄┄┄│┄┄┄│┄┄┄┄┄┄┄│┄┄┄┄┄┄┄┄┄┄┄┄┄│┄┄┄┄┄┄┄│┄┄┄│
# │ 1 │ 0 │ 0 │   0   │      1      │   0   │ 0 │
# │ 1 │ 0 │ 1 │   0   │      1      │   1   │ 1 │
# │ 1 │ 1 │ 0 │   0   │      1      │   0   │ 0 │
# │ 1 │ 1 │ 1 │   1   │      1      │   1   │ 1 │
#
# ¹ V praxi se obvykle používají tzv. redukované BDD, kde jsou
#   některé podstromy vhodně sloučeny, a to tak, aby se nezměnil
#   výsledek vyhodnocení. Na samotný proces vyhodnocování tato
#   úprava nemá žádný vliv.


class BDD:
    def __init__(self, val: str, left: Optional['BDD'] = None,
                 right: Optional['BDD'] = None) -> None:
        self.val = val
        self.left = left
        self.right = right


# Naprogramujte čistou funkci, která vyhodnotí zadané BDD pro dané
# ohodnocení proměnných. Předpokládejte, že každý vnitřní uzel má
# oba potomky. Hodnoty proměnných jsou zadané množinou ‹true_vars›:
# je-li název proměnné v této množině, proměnná je pravdivá, jinak
# nikoliv. V listech jsou uloženy řetězce ‹"0"› (výsledek je
# ‹False›) nebo ‹"1"› (výsledek je ‹True›).

def evaluate_bdd(bdd, true_vars: Set[str]) -> bool:
    pass


def main() -> None:
    assert evaluate_bdd(BDD("1"), set())
    assert evaluate_bdd(BDD("1"), {"x", "y", "z"})
    assert not evaluate_bdd(BDD("0"), set())
    assert not evaluate_bdd(BDD("0"), {"x", "y", "z"})

    assert evaluate_bdd(BDD("x", BDD("0"), BDD("1")), {"x"})
    assert not evaluate_bdd(BDD("x", BDD("0"), BDD("1")), {"y"})

    true = BDD("1")
    false = BDD("0")
    or_xyz = BDD("x", BDD("y", BDD("z", false, true), true), true)
    assert evaluate_bdd(or_xyz, {"x", "y", "z"})
    assert evaluate_bdd(or_xyz, {"y"})
    assert not evaluate_bdd(or_xyz, set())
    assert not evaluate_bdd(or_xyz, {"a", "b", "c"})

    and_xyz = BDD("x", false, BDD("y", false, BDD("z", false, true)))
    assert evaluate_bdd(and_xyz, {"x", "y", "z"})
    assert not evaluate_bdd(and_xyz, {"y", "z"})
    assert not evaluate_bdd(and_xyz, {"x", "b", "z"})

    xor_ab = BDD("a", BDD("b", false, true), BDD("b", true, false))
    assert evaluate_bdd(xor_ab, {"a"})
    assert evaluate_bdd(xor_ab, {"b"})
    assert not evaluate_bdd(xor_ab, {"a", "b"})
    assert not evaluate_bdd(xor_ab, set())
    assert not evaluate_bdd(xor_ab, {"a", "x", "b"})
    assert evaluate_bdd(xor_ab, {"a", "x", "y"})


if __name__ == "__main__":
    main()
