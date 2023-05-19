# Napište funkci, která spočítá sumu prvních ‹n› ‹k›-tých mocnin
# kladných po sobě jdoucích čísel, tzn. sumu ⟦sₙ = ∑ᵢ₌₁ⁿ aᵢ⟧, kde
# ⟦i⟧-tý člen ⟦aᵢ = iᵏ⟧.

def powers(n, k):
    sucet=0
    for i in range(n):
        sucet+=(i+1)**k
    return(sucet)
        


def main():
    assert powers(3, 2) == 14
    assert powers(5, 2) == 55
    assert powers(5, 3) == 225
    assert powers(3, 10) == 60074
    assert powers(8, 1) == 36
    assert powers(170, 0) == 170
    assert powers(10, 7) == 18080425
    assert powers(125, 4) == 6226236975


if __name__ == "__main__":
    main()
