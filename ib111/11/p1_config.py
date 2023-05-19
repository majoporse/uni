from typing import Dict
import os

# Napište proceduru ‹write_config›, která do souboru zadaného cestou
# ‹filename› zapíše konfiguraci ze slovníku ‹config›. (Pokud už
# takový soubor existuje, přepište jej.) Struktura slovníku je
# taková, že klíč je název sekce a hodnotou další slovník, který již
# obsahuje dvojice klíč-hodnota typu řetězec.
#
# Formát výstupního souboru nechť je následující:
#
#  • prázdné sekce (takové, kterým je přiřazený prázdný slovník)
#    ignorujeme,
#  • pro každou neprázdnou sekci zapíšeme řádek ‹[jméno sekce]› a na
#    další řádky postupně vypíšeme obsah příslušného slovníku ve
#    formátu ‹klíč = "hodnota"›.
#  • sekce i jednotlivé klíče v každé sekci uspořádejte na výstupu
#    podle abecedy.
#
# Příklad: pro vstupní slovník
#
#     { 'main': { 'code': 'IB111',
#                 'name': 'Základy programování' },
#       'empty': {},
#       'exams': { 'hard': 'no' } }
#
# se do zadaného souboru zapíše toto:
#
#     [exams]
#     hard = "no"
#     [main]
#     code = "IB111"
#     name = "Základy programování"
#
# Pro slovník s konfigurací si zavedeme typové synonymum ‹Config›:

Config = Dict[str, Dict[str, str]]


def write_config(filename: str, config: Config) -> None:
    with open(filename, "w") as file:
        keys = list(config.keys())
        keys.sort()
        for key in keys:
            if config[key] == {}:
                continue
            print(f'[{key}]', file=file)
            keys2 = list(config[key].keys())
            keys2.sort()
            for key2 in keys2:
                print(f'{key2} = "{config[key][key2]}"', file=file)


def main() -> None:
    test_file = "ib111_tmp_config.txt"
    if os.path.exists(test_file):
        os.remove(test_file)
    write_config(
        test_file,
        {'main': {'code': 'IB111',
                  'name': 'Základy programování'},
         'empty': {},
         'exams': {'hard': 'no'}})

    with open(test_file, 'r') as config:
        assert config.read() == \
               ('[exams]\n'
                'hard = "no"\n'
                '[main]\n'
                'code = "IB111"\n'
                'name = "Základy programování"\n')

    os.remove(test_file)
    write_config(
        test_file,
        {'entry': {},
         'main': {'code': 'IB111',
                  'name': '',
                  'cred': '6',
                  'term': 'spring term'},
         'mid': {},
         'chapters': {'1': 'conditions',
                      '2': 'loops',
                      '3': 'recursion'},
         'empty': {}})

    with open(test_file, 'r') as config:
        assert config.read() == \
               ('[chapters]\n'
                '1 = "conditions"\n'
                '2 = "loops"\n'
                '3 = "recursion"\n'
                '[main]\n'
                'code = "IB111"\n'
                'cred = "6"\n'
                'name = ""\n'
                'term = "spring term"\n')
#     os.remove(test_file)


if __name__ == '__main__':
    main()
