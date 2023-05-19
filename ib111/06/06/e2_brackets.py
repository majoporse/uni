# Řetězec je korektně uzávorkován právě tehdy, když buďto neobsahuje
# závorky žádné, nebo pro každou závorku v něm existuje taková
# opačná závorka, že řetězec uvnitř tohoto páru závorek je korektně
# uzávorkován.
#
# V této úloze budeme uvažovat následující typy závorek:
#
#  • kulaté závorky: otevírací ‹(› a uzavírací ‹)›,
#  • hranaté závorky ‹[›, ‹]›, a konečně
#  • složené závorky ‹{›, ‹}›.
#
# Každá otevírací závorka musí být spárována s právě jednou
# uzavírací. Žádné další znaky za závorky nepovažujeme.

# Například:
#
#  • řetězec ‹abc› je korektně uzávorkován, protože žádné závorky
#    neobsahuje,
#  • řetězec ‹()› je správně uzávorkován, protože ‹(› lze spárovat
#    s ‹)› tak, že vnitřní řetězec je prázdný a tedy dobře
#    uzávorkovaný,
#  • ‹[()]› je také korektně uzávorkovaný protože ‹[› lze spárovat tak,
#    že vnitřní řetězec je ‹()› o kterém již víme, že je správně
#    uzávorkovaný, a konečně
#  • ‹([)]› korektně uzávorkován není, protože k ‹(› obsahuje
#    jediný možný pár, ale vzniklý vnitřní řetězec ‹[› nemá pro ‹[›
#    žádnou uzavírací závorku.


# Napište predikát, kterého výsledek bude ‹True›, dostane-li
# v parametru korektně uzávorkovaný řetězec, ‹False› jinak.

def correct_parentheses(text: str) -> bool:
    stack = []
    for i in text:
        if not i.isalpha():
            if stack != [] and (i == ')' and stack[-1] == '(' \
           or i == '}' and stack[-1] == '{' \
           or i == ']' and stack[-1] =='['):
                stack.pop(-1)
            else:
                stack.append(i)
        
    if stack == []:
        return True
    return False
        

def main() -> None:
    assert correct_parentheses("")
    assert correct_parentheses("abc")
    assert correct_parentheses("([])")
    assert correct_parentheses("python()py[tho{n}]{{()}}")
    assert correct_parentheses("(p{y}[t]ho(n[]))")

    assert not correct_parentheses("([)]")
    assert not correct_parentheses("(p{y}[t]ho(n[])")
    assert not correct_parentheses("p{y}[t]ho(n[]))")
    assert not correct_parentheses("{python]")
    assert not correct_parentheses("pyt[]]hon")
    assert not correct_parentheses("p(y()thon")


if __name__ == '__main__':
    main()
