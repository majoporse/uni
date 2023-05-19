# Naprogramujte dvojici čistých funkcí, které realizují permutační
# šifru „skytalé“, která funguje takto:
#
#  • na hranol s ⟦n⟧-úhelníkovým průřezem se po spirále namotá úzký
#    pruh papíru (stejně jako když se omotává válec páskou),
#  • na strany takto omotaného hranolu se napíše tajná zpráva, každé
#    písmeno vždy na další obrátku papíru,
#  • papír se rozvine a zapíše se vzniklý dlouhý sloupec písmen.
#
# Když zapíšeme jednotlivé strany šifrovacího hranolu po řádcích do
# tabulky, původní zprávu přečteme po řádcích, zatímco tu
# zašifrovanou po sloupcích. Tříboký hranol se zprávou „útok za
# úsvitu“ by tedy vypadal takto:
#
#  ┌───┬───┬───┬───┐
#  │ U │ T │ O │ K │
#  ├───┼───┼───┼───┤
#  │ Z │ A │ U │ S │
#  ├───┼───┼───┼───┤
#  │ V │ I │ T │ U │
#  └───┴───┴───┴───┘
#
# Zašifrovaná zpráva pak bude „UZVTAIOUTKSU“. Při šifrování mezery
# na vstupu ignorujte. Při dešifrování jsou ale důležité v případě,
# kdy zpráva nevyplnila celou skytalé! Druhým parametrem funkcí je
# vždy ⟦n⟧, tzn. počet stran šifrovacího hranolu. Délku papíru
# zvolte nejkratší možnou (tak, aby se na ni zpráva celá vešla) a
# výsledek vraťte bez koncových mezer.

def scytale_encrypt(text, circumference):
    new_text = text
    for i in range(len(text)):
        new_text = new_text.replace(new_text[(i*circumference)%len(text)],text[i],1)
    return new_text

def scytale_decrypt(text, circumference):
    pass


def main():
    assert scytale_encrypt("UTOK ZA USVITU", 3) == "UZVTAIOUTKSU"
    assert scytale_encrypt("Python", 2) == "Phyotn"
    assert scytale_encrypt("Python IB111 Python", 5) \
        == "Po1ynyn1t tI1h hBPo"
    assert scytale_encrypt("Python", 1) \
        == "Python"
    assert scytale_encrypt("Python!!!", 5) \
        == "Pto!!yhn!"
    assert scytale_encrypt("Python IB111 Python", 1) \
        == "PythonIB111Python"

    assert scytale_decrypt("Phyotn", 2) == "Python"
    assert scytale_decrypt("Pn1o yIPn tBy  h1t  o1h  ", 5) \
        == "PythonIB111Python"
    assert scytale_decrypt("Python    ", 1) \
        == "Python"
    assert scytale_decrypt("Pto!!yhn! ", 5) \
        == "Python!!!"
    assert scytale_decrypt("PythonIB111Python", 1) \
        == "PythonIB111Python"


if __name__ == "__main__":
    main()
