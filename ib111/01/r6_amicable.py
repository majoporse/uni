# † Napište predikát, který určí, jsou-li 2 čísla spřátelená
# (amicable). Spřátelená čísla jsou dvě přirozená čísla taková, že
# součet všech kladných dělitelů jednoho čísla (kromě čísla
# samotného) se rovná druhému číslu, a naopak – součet všech
# dělitelů druhého čísla (kromě něho samotného) se rovná prvnímu.

def amicable(a, b):
    pass


def main():
    assert not amicable(136, 241)
    assert not amicable(1, 1)
    assert amicable(220, 284)
    assert amicable(1184, 1210)
    assert amicable(2620, 2924)
    assert not amicable(1190, 1212)
    assert not amicable(349, 234)


if __name__ == "__main__":
    main()
