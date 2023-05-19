from typing import List

# Napište funkci ‹bowling_score›, která spočítá celkové skóre bowlingové hry,
# přičemž počty shozených kuželek jsou v seznamu ‹rolls› (předpokládejte, že
# tento seznam obsahuje validní hody a že je dostatečně dlouhý). Skóre v
# bowlingu se počítá takto: Hraje se na 10 kol, v každém kole se háže až
# dvakrát, kromě posledního, kde se za určitých okolností háže třikrát. Pokud
# hned prvním hodem kola dosáhne hráč 10 bodů («strike»), podruhé už neháže a
# do skóre se mu započítá 10 plus hodnoty dvou dalších «hodů». Pokud v součtu
# obou hodů dosáhne hráč 10 bodů («spare»), do skóre se mu započítá 10 plus
# hodnota jednoho dalšího «hodu». V ostatních případech se do skóre započítá
# součet obou hodů kola. Pokud hráč zahrál strike v posledním kole, háže ještě
# dvakrát. Pokud hráč zahrál spare v posledním kole, háže ještě jednou.
#
# Příklad: Pro vstup ‹[10, 10, 3, 6, 4, 5, 9, 1, 7, 3, 10, 0, 1, 10, 3, 7, 10]›
# funkce vrátí «149»; pro vstupní seznam obsahující dvanáctkrát «10» funkce
# vrátí «300».
#
# Vysvětlení prvního příkladu:
#
# 1. kolo: «strike», počítá se ⟦10 + 10 + 3 = 23⟧ bodů
# 2. kolo: «strike», počítá se ⟦10 + 3 + 6 = 19⟧ bodů
# 3. kolo: ⟦3 + 6 = 9⟧ bodů
# 4. kolo: ⟦4 + 5 = 9⟧ bodů
# 5. kolo: «spare», počítá se ⟦9 + 1 + 7 = 17⟧ bodů
# 6. kolo: «spare», počítá se ⟦7 + 3 + 10 = 20⟧ bodů
# 7. kolo: «strike», počítá se ⟦10 + 0 + 1 = 11⟧ bodů
# 8. kolo: ⟦0 + 1 = 1⟧ bod
# 9. kolo: «strike», počítá se ⟦10 + 3 + 7 = 20⟧ bodů
# 10. kolo: «spare», háže se tedy ještě jednou a počítá se
#     ⟦3 + 7 + 10 = 20⟧ bodů. Celkem «149» bodů.
#
# Rozdělení hodů do jednotlivých kol pro názornost:
#
#  ┌────┬────┬─────┬─────┬─────┬─────┬────┬─────┬────┬────────┐
#  │ 10 │ 10 │ 3 6 │ 4 5 │ 9 1 │ 7 3 │ 10 │ 0 1 │ 10 │ 3 7 10 │
#  └────┴────┴─────┴─────┴─────┴─────┴────┴─────┴────┴────────┘
#
# Vysvětlení druhého příkladu:

# V každém kole padne «strike», počítá se tedy ⟦10 + 10 + 10 = 30⟧
# bodů. V posledním kole rovněž padne «strike», háže se tedy ještě dvakrát
# a počítá se opět ⟦10 + 10 + 10 = 30⟧ bodů. Dohromady tedy «10» kol po «30»
# bodech, což je «300» bodů. Rozdělení hodů do jednotlivých kol pro názornost:
#
#  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬──────────┐
#  │ 10 │ 10 │ 10 │ 10 │ 10 │ 10 │ 10 │ 10 │ 10 │ 10 10 10 │
#  └────┴────┴────┴────┴────┴────┴────┴────┴────┴──────────┘


def bowling_score(rolls: List[int]) -> int:
    score = 0
    last_strike = 0
    for index, roll in enumerate(rolls):
        if index < len(rolls) - (3 if rolls[-2] + rolls[-3] > 10 else 2):
            if roll == 10:
                score += rolls[index + 1] + rolls[index + 2]
                last_strike = index
            elif rolls[index] + rolls[index - 1] == 10 and \
                    (index - last_strike) % 2 == 0:
                score += rolls[index + 1]
        score += roll

    return score


def main() -> None:
    assert bowling_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]) \
        == 300
    assert bowling_score(
        [10, 10, 3, 6, 4, 5, 9, 1, 7, 3, 10, 0, 1, 10, 3, 7, 10]) == 149
    assert bowling_score(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 7, 3]) \
        == 20


if __name__ == "__main__":
    main()
