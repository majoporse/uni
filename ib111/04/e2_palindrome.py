# Napište predikát, kterého hodnota bude ‹True›, pokud v parametru
# dostane řetězec, který je palindrom, ‹False› jinak. Řetězec je
# palindrom, když jej můžeme přečíst v obou směrech (zprava doleva i
# zleva doprava) a jeho význam se nezmění. Palindromy jsou například
# „oko“, „kajak“ a „madam“.

# U řetězcových palindromů nehledíme na to, zda jsou jednotlivá
# písmena velká nebo malá, tudíž palindromem je i slovo „Anna“.
# Podobně nebereme v úvahu mezery – „jelenovi pivo nelej“ je tedy
# rovněž palindrom. Pro zjednodušení budeme ale v této úloze
# považovat znaky lišící se pouze diakritikou za různé.

def is_palindrome(text):
    pass


def main():
    assert is_palindrome("oko")
    assert is_palindrome("jelenovi pivo nelej")
    assert is_palindrome("Anna")
    assert is_palindrome("a")
    assert is_palindrome("kuna nese nanuk")

    assert not is_palindrome("python")
    assert not is_palindrome("až")
    assert not is_palindrome("okó")
    assert not is_palindrome("_Anna.")
    assert not is_palindrome("kobyla má malý bok")


if __name__ == '__main__':
    main()
