# † Napište čistou funkci, která dostane na vstupu dva řetězce,
# ‹text› a ‹pattern› (vzor) a vrátí pozici prvního výskytu vzoru v
# textu, pokud se v něm nachází, -1 jinak. Text se skládá pouze z
# velkých a malých písmen anglické abecedy a mezer a vzor může navíc
# obsahovat znaky ‹?›, ‹[›, ‹]›, ‹-›, kterých význam je následovný:
#
#  • ‹?› představuje libovolný znak textu, zatímco
#  • ‹[a-c]› představuje libovolné z písmen mezi ‹a› a ‹c› včetně,
#    tj. libovolné z písmen ‹a›, ‹b› nebo ‹c›.
#
# Speciální znaky se ve vzoru nemůžou vykytovat v žádném jiném kontextu, než
# ve výše popsaném.

# Například vzor ‹y[l-u]h[m-q]?› se v textu ‹Python› nachází jednou
# a to na pozici 1 a vzor "python" se v daném textu nenachází vůbec
# (naše funkce by vrátila -1).

def find_pattern(text, pattern):
    pass


def main():
    assert find_pattern("abc", "abc") == 0
    assert find_pattern("abc", "v") == -1
    assert find_pattern("Python", "python") == -1
    assert find_pattern("abcd", "b?d") == 1
    assert find_pattern(" is ", " i[l-t] ") == 0
    assert find_pattern("abc", "c") == 2
    assert find_pattern("Python", "Py[c-x]") == 0
    assert find_pattern("k", "[i-k]") == 0
    assert find_pattern("k", "[k-l]") == 0
    assert find_pattern("abcd", "k?") == -1
    assert find_pattern("ghij", "[a-c]") == -1
    assert find_pattern("Python", "y[l-u]h[m-q]?") == 1
    assert find_pattern("Python", "python") == -1
    assert find_pattern("Python is great", " i[l-t] g[k-v]e") == 6
    assert find_pattern("Python is great", " i[l-t] g[s-v]e") == -1
    assert find_pattern("PPython", "Python") == 1
    assert find_pattern("PyPython", "Python") == 2
    assert find_pattern("hrad veveří nehoří", "veverka") == -1


if __name__ == '__main__':
    main()
