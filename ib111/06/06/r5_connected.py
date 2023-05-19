from typing import Dict, List


# † Uvažme městskou hromadnou dopravu, která má pojmenované zastávky,
# mezi kterými jezdí (pro nás anonymní) spoje. Spoje mají daný směr:
# není zaručeno, že jede-li spoj z ⟦A⟧ do ⟦B⟧, jede i spoj z ⟦B⟧ do
# ⟦A⟧. Dopravní síť budeme reprezentovat slovníkem, kde klíčem je
# nějaká zastávka ⟦A⟧, a jemu příslušnou hodnotou je seznam
# zastávek, do kterých se lze z ⟦A⟧ dopravit bez dalšího zastavení.

# Napište predikát, který rozhodne, je-li možné dostat se
# z libovolné zastávky na libovolnou jinou zastávku pouze použitím
# spojů ze zadaného slovníku.

def all_connected(stops: Dict[str, List[str]]) -> bool:
    pass


def main() -> None:
    assert all_connected({"A": []})
    assert all_connected({"A": ["B", "C"], "B": ["A", "C"], "C": ["A", "B"]})
    assert all_connected({"A": ["B"], "B": ["C"], "C": ["D"], "D": ["A"]})
    assert all_connected({"A": ["B", "C", "D"], "B": ["C"], "C": ["A", "B"],
                          "D": ["C"]})

    assert not all_connected({"A": ["B"], "B": []})
    assert not all_connected({"A": ["B", "C"], "B": ["C"], "C": ["B"]})
    assert not all_connected({"A": ["B", "C"], "B": ["C"], "C": ["B"]})
    assert not all_connected({"A": ["B", "C", "D"], "B": ["C"], "C": ["B"],
                              "D": ["A"]})


if __name__ == '__main__':
    main()
