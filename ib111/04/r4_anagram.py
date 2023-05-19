# Napište predikát ‹is_anagram›, který dostane na vstup 2 řetězce,
# ‹text› a ‹anagram›, složené z velkých písmen anglické abecedy a
# mezer. Predikát nechť rozhodne, zda je řetězec ‹anagram› permutací
# řetězce ‹text› (mezery přitom ignorujte).

def is_anagram(text, anagram):
    pass


def main():
    assert is_anagram("ABC", "ACB")
    assert is_anagram(" ABC", "ACB ")
    assert is_anagram(" A  BC", "ACB ")
    assert is_anagram("B BB C", "CBBB")
    assert is_anagram("     ", "")

    assert not is_anagram("ABC", "EFG")
    assert not is_anagram("ABCC", "ACB")
    assert not is_anagram(" A    ", " ")
    assert not is_anagram("B BB ", "B")
    assert not is_anagram("B BB ", "BC")


if __name__ == "__main__":
    main()
