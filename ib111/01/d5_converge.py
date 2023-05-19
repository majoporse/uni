from math import sin


# † Každá «omezená» posloupnost – tedy taková, která nabývá hodnoty
# pouze z nějakého konečného intervalu – má tzv. konvergentní
# podposloupnost. Co tyto termíny přesně znamenají nás nemusí
# trápit (více se dozvíte v matematické analýze): nám bude stačit
# intuice.

# Podposloupnost je posloupnost, která vznikne „přeskočením“
# některých prvků původní posloupnosti (zde je ⟦B⟧ podposloupnost
# sestávající z lichých prvků posloupnosti ⟦A⟧):

#  ⟦ A → 1, 2, 3, 4, 5, …
#    B → 1,    3,    5, … ⟧

# Konvergentní posloupnost je pak taková, že se její prvky postupně
# blíží nějaké konkrétní hodnotě (tzv. limitě ⟦L⟧) – přibližně
# platí, že čím větší index ⟦i⟧, tím je vzdálenost ⟦ |L - aᵢ| ⟧
# menší.

# Naším úkolem bude nějakou takovou konvergentní podposloupnost
# najít: začneme omezenou posloupností ⟦aᵢ = \sin(i)⟧ a budeme
# budovat konvergentní podposloupnost B s prvky ⟦bⱼ⟧. Pozor: hledáme
# libovolnou podposloupnost s potřebnou vlastností, nikoliv nějakou
# konkrétní – máme tak při implementaci relativně velkou volnost.
# Jak tedy na to?

# První pozorování je, že se stačí zabývat kladnými hodnotami ⟦aᵢ⟧.
# Dále pak stačí zabezpečit, aby platilo ⟦bⱼ₊₁ ≤ bⱼ⟧. Při výběru
# hodnoty ⟦b₁⟧ máme mnoho možností, ale je výhodné zvolit ⟦a₁ = b₁
# = \sin(1)⟧. Zapišme nyní funkci ‹convergent(n)›, které výsledkem
# bude hodnota ⟦bₙ⟧:

def convergent(n):

    # Pro samotný výpočet budeme potřebovat dva indexy: index ‹i›
    # náleží posloupnosti ⟦A⟧ (čísluje tedy prvky ⟦aᵢ⟧) zatímco
    # index ‹j› náleží posloupnosti ⟦B⟧ (čísluje prvky ⟦bⱼ⟧).

    i = 1
    j = 1

    # Navíc si potřebujeme pamatovat poslední nalezenou hodnotu ⟦bⱼ⟧
    # – proměnná ‹last› bude vždy (opět s výjimkou krátkého okamžiku
    # mezi dvěma sousedními příkazy uvnitř cyklu) obsahovat ‹j›-tou
    # hodnotu posloupnosti ⟦B⟧ (kde ‹j› značí hodnotu proměnné ‹j›
    # zavedené výše). Vzpomeňte si také, že ⟦a₁ = b₁⟧.

    last = sin(i)

    # Následuje samotný cyklus, který bude hledat hodnotu ⟦bⱼ⟧.
    # Tento bude postupně procházet prvky ⟦aᵢ⟧ posloupnosti ⟦A⟧.
    # Vždy, když nalezneme nové ⟦aᵢ⟧, pro které platí ⟦aᵢ ≤ bⱼ⟧ –
    # kde ⟦bⱼ⟧ je uloženo v proměnné ‹last› – můžeme toto ⟦aᵢ⟧
    # přidat do posloupnosti ⟦B⟧, jako ⟦bⱼ₊₁⟧, a odpovídajícím
    # způsobem upravit proměnné ‹j› a ‹last›. V programu zapisujeme
    # ⟦aᵢ⟧ jako ‹sin(i)›.

    while j < n:
        i += 1
        if sin(i) > 0 and sin(i) <= last:
            j += 1
            last = sin(i)

    # Po ukončení cyklu platí ‹j == n› (před cyklem platilo ‹j ≤ n›,
    # cyklus ukončíme jakmile přestane platit ‹j < n› a zároveň
    # hodnotu ‹j› v každé iteraci zvýšíme nejvýše o 1). Protože
    # v každém kroku platí, že proměnná ‹last› obsahuje prvek ⟦bⱼ⟧ a
    # nyní zároveň platí ‹j = n›, celkem dostáváme, že po ukončení
    # cyklu je v proměnné ‹last› uložena hodnota ⟦bₙ⟧.

    return last


def main():  # demo
    assert convergent(1) == sin(1)
    assert convergent(2) == sin(3)
    assert convergent(3) == sin(44)

    # Krom obvyklých konkrétních případů, které testujeme výše,
    # můžeme ověřovat i «vlastnosti» námi implementovaných funkcí.
    # Například níže kontrolujeme monotónnost (posloupnost je
    # nestoupající) a omezenost zespodu (nulou). Tyto dvě vlastnosti
    # dohromady zaručují, že posloupnost je konvergentní:
    # samozřejmě, v konečném čase lze takto ověřit pouze konečný
    # počet případů, a «testy» nám tedy ani jednu ze zmiňovaných tří
    # vlastností «nemohou zaručit».

    for i in range(5):
        assert convergent(i + 1) <= convergent(i)
        assert convergent(i) > 0


if __name__ == '__main__':
    main()
