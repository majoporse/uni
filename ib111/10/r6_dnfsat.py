from typing import List, Tuple, Dict

# Ve třetí ukázce této kapitoly jsme řešili problém splnitelnosti
# výrokové formule. Tato formule byla ve speciálním tvaru, takzvané
# konjunktivní normální formě.

# Nyní se podíváme na stejný problém pro formule v jiném speciálním
# tvaru – v tzv. «disjunktivní» normální formě. V tomto tvaru se
# formule skládá opět z klauzulí, tentokrát je ale jejich disjunkcí.
# Uvnitř závorek se pak objevuje konjunkce literálů. Například:
#
#  ⟦ (a ∧ b) ∨ (¬a ∧ b ∧ a) ∨ (¬a ∧ c ∧ b ∧ ¬c) ⟧
#
# Napište čistou funkci ‹satisfiable›, která rozhodne, je-li takto
# zadaná formule splnitelná. Než se pustíte do řešení, dobře si
# rozmyslete, co splnitelnost znamená a v jakých přesně případech je
# formule v tomto tvaru (ne)splnitelná. Typy, kterými formuli
# reprezentujeme jsou stejné, jako ty v ukázce.


Variable = str
Literal = Tuple[Variable, bool]
Clause = List[Literal]
Formula = List[Clause]


def satisfiable(phi: Formula) -> bool:
    pass


def main() -> None:
    assert satisfiable([[positive("a")]])
    assert satisfiable([[negative("a")]])
    assert not satisfiable([[positive("a"), negative("a")]])
    assert satisfiable([[positive("a"), negative("b")],
                        [positive("b")]])
    assert satisfiable([[positive("a"), negative("b")],
                        [positive("b"), positive("a")]])

    assert satisfiable([[positive("a"), negative("b"), positive("c")],
                        [negative("a"), negative("b"), negative("c")],
                        [negative("a"), positive("b"), negative("c")]
                        ])
    assert satisfiable([[positive("a"), negative("b"), positive("c")],
                        [negative("a"), negative("b"), negative("c")],
                        [positive("a"), negative("b"), negative("c")],
                        [negative("a"), positive("b"), negative("c")]
                        ])
    assert satisfiable([[positive("a"), negative("a"), positive("c")],
                        [negative("a"), negative("b"), negative("c")],
                        [positive("a"), negative("a"), negative("c")],
                        [negative("a"), positive("c"), negative("c")]
                        ])
    assert satisfiable([[positive("a"), negative("a"), positive("c")],
                        [negative("a"), negative("b"), negative("c")],
                        [negative("a"), positive("b"), negative("c")]
                        ])
    assert satisfiable([[positive("a"), negative("b"), positive("c")],
                        [negative("a"), negative("b"), negative("c")],
                        [negative("a"), positive("b"), negative("b")]
                        ])
    assert not satisfiable([[positive("a"),
                             negative("b"), positive("b")],
                            [negative("a"), positive("a"),
                             negative("c")],
                            [negative("a"), positive("c"),
                             negative("c")]])


def positive(var: str) -> Literal:
    return (var, True)


def negative(var: str) -> Literal:
    return (var, False)


if __name__ == "__main__":
    main()
