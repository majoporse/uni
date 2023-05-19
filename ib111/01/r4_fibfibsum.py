# † Nechť ⟦A⟧ je Fibonacciho posloupnost s členy ⟦aₙ⟧ a ⟦B⟧ je
# posloupnost taková, že má na ⟦i⟧-té pozici ⟦aᵢ⟧-tý prvek
# posloupnosti ⟦A⟧, tj. prvek s indexem ⟦aᵢ⟧ (nikoliv prvek
# s indexem ⟦i⟧). Napište funkci, která sečte prvních ‹count› prvků
# posloupnosti ⟦B⟧ (t.j. ty prvky posloupnosti ⟦A⟧, kterých «indexy»
# jsou po sobě jdoucí Fibonacciho čísla).

# Například ‹fibfibsum(6)› se vypočte takto:
# ⟦ a₁ + a₁ + a₂ + a₃ + a₅ + a₈ = 1 + 1 + 1 + 2 + 5 + 21 = 31 ⟧

def fibfibsum(count):
    pass


def main():
    assert fibfibsum(3) == 3
    assert fibfibsum(5) == 10
    assert fibfibsum(6) == 31
    assert fibfibsum(7) == 264
    assert fibfibsum(10) == 139589576542


if __name__ == "__main__":
    main()
