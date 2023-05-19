/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [x] clearly describes solution to the problem
 ** * [x] correctly decomposes the problem
 ** * [!] doesn't have code duplication
 **   * Please fix the repeated insertion to the vectors in loops. You don't need to
 **  do that.
 ** * [x] uses correct abstractions, algorithms and data structures
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * You use some “brave” constructions here-and-there, and I know myself how to
 ** abuse the C++ :eyes:
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <tuple>
#include <map>
#include <vector>
#include <cassert>
#include <cstdint>

/* V tomto úkolu budeme pracovat s dvourozměrnou „mapou města“,
 * kterou reprezentujeme jako čtvercovou síť. Na každém políčku
 * může stát budova (tvaru kvádru), která má barvu a celočíselnou
 * výšku (budova výšky 1 má tvar krychle). Pro práci s mapou si
 * zavedeme:
 *
 *  • typ ‹building›, který reprezentuje budovu,
 *  • typ ‹coordinates›, který určuje pozici budovy a nakonec
 *  • typ ‹city›, který reprezentuje mapu jako celek.
 *
 * Jihozápadní (levý dolní) roh mapy má souřadnice ⟦(0, 0)⟧, ⟦x⟧-ová
 * souřadnice roste směrem na východ, ⟦y⟧-ová směrem na sever. */

struct building
{
    int height;
    int colour;
};

using coordinates = std::tuple< int, int >;
using city = std::map< coordinates, building >;

/* Nejsou-li nějaké souřadnice v mapě přítomny, znamená to, že na
 * tomto místě žádná budova nestojí.
 *
 * Vaším úkolem je podle zadané mapy spočítat pravoúhlý boční pohled
 * na město (panorama), které vznikne při pohledu z jihu, a které
 * bude popsáno typy:
 *
 *  • ‹column›, který reprezentuje jeden sloupec a pro každou
 *    viditelnou jednotkovou krychli obsahuje jedno číslo, které
 *    odpovídá barvě této krychle,
 *  • ‹skyline›, které obsahuje pro každou ‹x›-ovou souřadnici mapy
 *    jednu hodnotu typu ‹column›, kde index příslušného sloupce
 *    odpovídá jeho ‹x›-ové souřadnici. */

using column = std::vector< int >;
using skyline = std::vector< column >;

/* Vstup a odpovídající výstup si můžete představit např. takto:
 *
 *                                   ┌───┐
 *                                   │░░░│ 4
 *                                   ├───┤
 *                                   │░░░│ 3
 *   ┌───┬───┬───┬───┐   ┌───┬───┐   ├───┤
 *   │░1░│░3░│   │░5░│   │▒▒▒│░░░│   │░░░│ 2
 *   ├───┼───┼───┼───┤   ├───┼───┤   ├───┤
 *   │   │ 2 │   │   │   │▒▒▒│   │   │░░░│ 1
 *   ├───┼───┼───┼───┤   ├───┼───┤   ├───┤
 *   │▒3▒│▒1▒│   │   │   │▒▒▒│▒▒▒│   │░░░│ 0
 *   └───┴───┴───┴───┘   └───┴───┴───┴───┘
 *                         0   1   2   3
 *
 * Napište čistou funkci ‹compute_skyline› která výpočet provede.
 * Počet prvků každého sloupce musí být právě výška nejvyšší budovy
 * s danou ⟦x⟧-ovou souřadnicí. */

skyline compute_skyline( const city &c ){

/** Do you really think it saves that much work?
 **
 ** ---
 **
 ** I've looked below, it doesn't save anything, just catches »your own« edge case. **/
    if (c.empty())
        return {};

/** Now this is very naughty… I would probably go with something like:
 ** ```suggestion:-0+0
 **     const int max = std::get<0>(c.rbegin()->first);
 ** ```
 **
 ** And this is the place where you create your own edge case, you can solve it
 ** without finding the maximum, or with finding the maximum and handling this in a
 ** different way. **/
    const int max = std::get<0>((--c.end())->first);

    std::vector<column> res(max + 1);

    for (auto &[key, build] : c){
/** nice **/
        auto [x, y] = key;

        if (static_cast<int>(res[x].size()) < build.height){
/** ```suggestion:-1+0
 **             res[x].insert(res[x].end(), build.height - res[x].size(),
 ** build.colour);
 ** ```
 **
 ** (careful about underflow though) **/
            for(int n = build.height - res[x].size(); n > 0; --n)
                res[x].emplace_back(build.colour);
        }
        
    }
    return res;
}

int main()
{
    city example{ { { 0, 0 }, { 3, 0 } },
                  { { 1, 0 }, { 1, 2 } },
                  { { 1, 1 }, { 2, 0 } },
                  { { 0, 2 }, { 1, 2 } },
                  { { 1, 2 }, { 3, 1 } },
                  { { 3, 2 }, { 5, 1 } } };

    skyline expected{ { 0, 0, 0 }, { 2, 0, 1 }, {}, { 1, 1, 1, 1, 1 } };
    assert( compute_skyline( example ) == expected );

    return 0;
}
