# Atbash je jednoduchá substituční šifra, kterou vynalezli Hebrejci
# (její název je odvozen od písmen hebrejské abecedy). Zašifrování
# písmene touto šifrou probíhá tak, že se spočítá vzdálenost daného
# písmena od prvního písmena používané abecedy a toto písmeno je
# nahrazené písmenem, které se nachází ve stejné vzdálenosti od
# konce abecedy.

# V této úloze budeme jako abecedu používat velká písmena anglické
# abecedy: zašifrujeme-li písmeno ‹C› výsledkem bude ‹X›, protože
# ‹C› je třetím písmenem abecedy a ‹X› je třetí od konce.

# Abychom dosáhli větší uživatelské přívětivosti, povolíme na vstupu
# i malá písmena a mezery – malá písmena budeme šifrovat obdobně
# jako velká, a šifrování bude velikost písmen zachovávat (malá
# písmena se šifrují na malá a velká na velká). Mezery šifrování i
# dešifrování zachová nezměněné.

# Napište čistou funkci, která na vstupu dostane text (řetězec),
# zašifruje ho šifrou atbash výše popsaným způsobem, a výsledek
# vrátí opět jako řetězec.

def atbash_encrypt(text):
    pass


# Dále napište čistou funkci, která na vstupu dostane řetězec
# představující text zašifrovaný šifrou atbash, tento text
# dešifruje, a výsledek vrátí jako řetězec.

def atbash_decrypt(text):
    pass


def main():
    assert atbash_encrypt("C") == "X"
    assert atbash_encrypt(" ") == " "
    assert atbash_decrypt("") == ""
    assert atbash_encrypt("python") == "kbgslm"
    assert atbash_encrypt("We love PROGRAMMING") == "Dv olev KILTIZNNRMT"
    assert atbash_encrypt("we will all pass this course because learning is"
                          " GREAT") == "dv droo zoo kzhh gsrh xlfihv yvxzfhv" \
                                       " ovzimrmt rh TIVZG"

    assert atbash_decrypt("X") == "C"
    assert atbash_decrypt(" ") == " "
    assert atbash_decrypt("") == ""
    assert atbash_decrypt("KBGSLM") == "PYTHON"
    assert atbash_decrypt("Dv olev KILTIZNNRMT") == "We love PROGRAMMING"
    assert atbash_decrypt("dv droo zoo kzhh gsrh xlfihv yvxzfhv ovzimrmt rh"
                          " TIVZG") == "we will all pass this course because" \
                                       " learning is GREAT"


if __name__ == '__main__':
    main()
