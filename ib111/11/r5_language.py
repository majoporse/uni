# Jednou z možností, jak poznat v jakém (přirozeném) jazyce je
# nějaký dokument napsaný, je jednoduchá statistická analýza.
# Napište funkci, která dostane jako parametry dva názvy souborů,
# ‹lang_file› a ‹text_file›:
#
#  1. soubor ‹lang_file› bude ve formátu JSON a bude pro každý jazyk
#     obsahovat slovník tvaru ‹{ 'a': 357907, 'b': 113756, … }› kde
#     hodnota u každého písmene je počet jeho výskytů v nějakém
#     reprezentativním dokumentu,
#  2. soubor ‹text_file› je textový soubor, kterého jazyk chceme
#     určit.
#
# Jazyk určujte tak, že spočítáte frekvence jednotlivých písmen
# v souboru ‹text_file› a srovnáte je s těmi uloženými v souboru
# ‹lang_file›.
#
# Jak nalezneme nejlepší shodu? Informace o frekvenci písmen
# v nějakém dokumentu lze chápat jako vektory v 26-rozměrném
# prostoru (resp. vícerozměrném, uvažujeme-li písmena s diakritikou,
# ale přesná dimenze není podstatná). Za nejpodobnější budeme
# považovat vektory, které svírají nejmenší úhel. Tento získáte ze
# vztahu ⟦ a⋅b = |a|⋅|b|⋅\cos θ ⟧ (kde na levé straně je běžný
# skalární součin, „absolutní hodnoty“ na straně pravé jsou pak
# délky, které zjistíte ze vztahu ⟦ |a|² = a⋅a ⟧).


def recognize_language(lang_file: str, text_file: str) -> str:
    pass


def main() -> None:
    lang_file = "zz.language.json"
    lang_samples = [("english",
                     "Python is a great programming language. " +
                     "We love Python. And we love our school " +
                     "and learning." +
                     "And we apperently need more text, so that " +
                     "we will hopefully successfuly recognize " +
                     "english, as intended in the first place."),

                    ("german",
                     "Python ist eine großartige Programmiersprache." +
                     "Wir lieben Python. Und wir lieben unsere " +
                     "Schule und das Lernen."),

                    ("spanish",
                     "Python es un gran lenguaje de programación. " +
                     "Nos encanta Python. Y amamos " +
                     "nuestra escuela y nuestro aprendizaje."),

                    ("czech",
                     "Python je skvělý programovací jazyk. " +
                     "Zbožňujeme Python, naši školu a učení.")]

    for expect, content in lang_samples:
        with open('zt.language.txt', "w+") as file:
            file.write(content)
        lang = recognize_language(lang_file, 'zt.language.txt')
        assert lang == expect, (lang, expect)


if __name__ == "__main__":
    main()
