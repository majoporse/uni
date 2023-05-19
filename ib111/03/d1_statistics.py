from math import sqrt


# Tato ukázka demonstruje základní použití seznamů: zejména jejich
# «indexaci» a «iteraci». Oba tyto koncepty si demonstrujeme na
# výpočtu jednoduchých statistik nad prvky předem daného seznamu:
# průměru, mediánu a směrodatné odchylky.

# Jako první statistiku vypočteme «průměr», který získáme jako podíl
# součtu všech prvků vstupního seznamu a jeho délky. Protože obě
# tyto operace jsou v Pythonu zabudované, je definice velice
# jednoduchá:

def average(data):
    return sum(data) / len(data)


# Protože indexace je v určitém smyslu jednodušší než iterace,
# budeme pokračovat výpočtem mediánu: medián je hodnota, která se
# objeví v «uspořádaném» souboru čísel uprostřed. Tento soubor dat
# budeme reprezentovat «neprázdným» seznamem:

def median(data):

    # První problém, který musíme vyřešit, je ona uspořádanost:
    # naštěstí je to v Pythonu problém velice jednoduchý, protože
    # máme k dispozici vestavěnou (čistou) funkci ‹sorted›, která
    # vytvoří ze vstupního seznamu nový, vzestupně uspořádaný:

    data = sorted(data)

    # Zde je možná vhodné připomenout, že přiřazení do proměnné mění
    # «vazbu» – to, na kterou hodnotu proměnná odkazuje – a nemá
    # vliv na samotnou hodnotu. Vstupní seznam tedy není tímto
    # přiřazením nijak dotčen, a funkce ‹median› je funkcí čistou.

    # Dalším krokem je výpočet indexu, na kterém nalezneme medián:
    # tady nastávají dvě možnosti: buď je seznam liché, nebo sudé
    # délky. Délku seznamu zjistíme vestavěnou (čistou) funkcí
    # ‹len›:

    if len(data) % 2 == 1:

        # Případ liché délky je jednodušší, proto jej vyřešíme
        # první. V tomto případě existuje skutečný prostřední prvek,
        # a my pouze vrátíme jeho hodnotu. Celočíselné dělení dvěma
        # nám dá právě ten správný index – přesvědčte se o tom!

        return data[len(data) // 2]

    else:

        # V opačném případě je seznam sudé délky (prázdný seznam
        # neuvažujeme, nevyhovuje vstupní podmínce). Běžná definice
        # mediánu v tomto případě říká, že výsledkem má být
        # aritmetický průměr obou „prostředních“ hodnot (těch, které
        # jsou nejblíže pomyslnému středu, který se nachází přesně
        # mezi nimi).

        return (data[len(data) // 2] + data[len(data) // 2 - 1]) / 2


# Poslední a nejsložitější statistikou je tzv. «směrodatná odchylka»
# ⟦s⟧. Tuto spočítáme jako odmocninu tzv. «rozptylu» ⟦s²⟧, který je
# popsaný následovným vztahem (⟦n⟧ je počet prvků, ⟦xᵢ⟧ jsou
# jednotlivé prvky a ⟦m⟧ je průměr):
#
# ⟦ s² = 1/(n - 1) ∑ᵢ₌₁ⁿ (xᵢ - m)² ⟧

def stddev(data):

    # Pro výpočet jednotlivých členů budeme potřebovat průměr,
    # který již máme implementovaný výše. Dále si nachystáme
    # «střadač» (akumulátor), do kterého sečteme jednotlivé
    # kvadratické odchylky ⟦(xᵢ - m)²⟧:

    mean = average(data)
    square_error_sum = 0

    # Chceme-li pro každý prvek seznamu provést nějakou akci nebo
    # výpočet, použijeme k tomu «cyklus». Mohli bychom samozřejmě
    # použít konstrukce, které již známe: indexovou proměnnou,
    # cyklus tvaru ‹for i in range(n)›, funkci ‹len› a indexaci
    # seznamu ‹data›. V případě, že ale indexovou proměnnou
    # nepotřebujeme k ničemu jinému, než indexaci jednoho seznamu,
    # lze použít mnohem úspornější a čitelnější zápis:

    for x_i in data:

        # V těle takovéhoto cyklu máme v proměnné ‹x_i› uloženy
        # přímo «hodnoty» ze seznamu ‹data›, nemusíme tedy vůbec
        # indexovat.

        square_error_sum += (x_i - mean) ** 2

    # Protože rozptyl (variance) je vlastně střední (průměrná)
    # kvadratická odchylka s drobnou korekcí, vypočteme…

    variance = square_error_sum / (len(data) - 1)

    # … a celkový výsledek získáme jako odmocninu rozptylu:

    return sqrt(variance)


# Konečně funkčnost ověříme na několika jednoduchých příkladech.

def main():
    assert median([1, 2, 3]) == 2
    assert median([1, 3]) == 2

    sample = [2, 4, 4, 4, 5, 5, 5, 7, 9]
    assert average(sample) == 5
    assert median(sample) == 5
    assert stddev(sample) == 2


if __name__ == '__main__':
    main()
