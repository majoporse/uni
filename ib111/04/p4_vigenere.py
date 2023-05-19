# Z přednášky již znáte Caesarovu šifru. Vigenèrova šifra funguje
# podobně, ale klíčem je řetězec (slovo), nikoliv pouze jediné číslo
# z rozsahu 0–26.

# Šifrujeme (i dešifrujeme) tak, že pod vstupní text si podepíšeme
# klíč, který zopakujeme tolikrát, aby byl stejně dlouhý jako text.
# Každou takovou dvojici pak použijeme jako vstup pro Caesarovou
# šifru (písmeno klíče udává posuv — A = 0, B = 1, …).

# Jako příklad zašifrujeme slovo „PYTHON“ klíčem „BCD“: klíč nejprve
# prodloužíme opakováním na „BCDBCD“, poté spočítáme:
#
#  • ‹caesar('P', 1) = 'Q'›
#  • ‹caesar('Y', 2) = 'A'›
#  • ‹caesar('T', 3) = 'W'›
#  • ‹caesar('H', 1) = 'I'›
#  • ‹caesar('O', 2) = 'Q'›
#  • ‹caesar('N', 3) = 'Q'›

# Napište (čistou) funkci, která na vstupu dostane text
# k zašifrování a klíč. Obojí budou řetězce libovolné délky, přičemž
# klíč je neprázdný a tvořený pouze písmeny anglické abecedy a text
# písmeny anglické abecedy a mezerami. Výstupem bude daný text
# zašifrovaný pomocí daného klíče. Pro zjednodušení budeme vracet
# zašifrovaný text ve velkých písmenech.

def vigenere_encrypt(text, key):
    encrypted = ''
    for i in range(len(text)):
        cipher = ord(key.upper()[i%len(key)]) - ord('A')
        if (ord(text.upper()[i]) + cipher)> 90:
            encrypted += chr(ord(text.upper()[i]) + cipher - 26)
        elif text[i] == ' ':
                encrypted += ' '
        else:
            encrypted += chr(ord(text.upper()[i]) + cipher)
    return encrypted

# Dále napište (opět čistou) funkci, která na vstupu dostane
# zašifrovaný text a odpovídající klíč (obojí ve stejném formátu,
# jako parametry předešlé funkce) a vrátí dešifrovaný text. Pro
# zjednodušení budeme dešifrovaný text opět vracet ve velkých
# písmenech.

def vigenere_decrypt(text, key):
    encrypted = ''
    for i in range(len(text)):
        cipher = ord(key.upper()[i%len(key)]) - ord('A')
        if text[i] == ' ':
                encrypted += ' '
        elif (ord(text.upper()[i]) - cipher) < 65:
            encrypted += chr(ord(text.upper()[i]) - cipher + 26)
        else:
            encrypted += chr(ord(text.upper()[i]) - cipher)
    return encrypted


def main():
    assert vigenere_encrypt("", "abcd") == ""
    assert vigenere_encrypt(" ", "a") == " "
    assert vigenere_encrypt("abcde", "a") == "ABCDE"
    assert vigenere_encrypt("programming", "c") == "RTQITCOOKPI"
    assert vigenere_encrypt("python", "bcd") == "QAWIQQ"
    assert vigenere_encrypt("PYTHON", "PROGRAMMING") == "EPHNFN"
    assert vigenere_encrypt("Python is fun", "NO") == "CMGVBB WF SIA"
    assert vigenere_encrypt("I shall pass this course "
                            "because I love programming", "hopefully") \
        == "P HLFFW NHGH YBTD JCJVXY MCJOJWJ T JVJT ULZRPHABMSA"

    assert vigenere_decrypt("", "abcd") == ""
    assert vigenere_decrypt(" ", "a") == " "
    assert vigenere_decrypt("abcde", "a") == "ABCDE"
    assert vigenere_decrypt("RTQITCOOKPI", "C") == "PROGRAMMING"
    assert vigenere_decrypt("qawiqq", "bcd") == "PYTHON"
    assert vigenere_decrypt("EPHNFN", "programming") == "PYTHON"
    assert vigenere_decrypt("CMGVBB WF SIA", "no") == "PYTHON IS FUN"
    assert vigenere_decrypt("P HLFFW NHGH YBTD JCJVXY "
                            "MCJOJWJ T JVJT ULZRPHABMSA", "HOPEFULLY") \
        == "I SHALL PASS THIS COURSE BECAUSE I LOVE PROGRAMMING"


if __name__ == '__main__':
    main()
