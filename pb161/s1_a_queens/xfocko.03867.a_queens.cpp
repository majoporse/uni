/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [x] clearly describes solution to the problem
 ** * [-] correctly decomposes the problem
 **   * You don't have a bad decomposition, but it's not ideal, since it still leads
 **  you to some amount of copy-paste
 ** * [-] doesn't have code duplication
 **   * Related to the previous point
 ** * [x] uses correct abstractions, algorithms and data structures
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * You were going in the right direction and took the wrong turn, it doesn't need
 **  much to be fixed.
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <cstdint>
#include <cassert>

/* V této úloze budete programovat řešení tzv. problému osmi
 * královen (osmi dam). Vaše řešení bude predikát, kterého vstupem
 * bude jediné 64-bitové bezznaménkové číslo (použijeme typ
 * ‹uint64_t›), které popisuje vstupní stav šachovnice: šachovnice
 * 8×8 má právě 64 polí, a pro reprezentaci každého pole nám stačí
 * jediný bit, který určí, je-li na tomto políčku umístěna královna.
 *
 * Políčka šachovnice jsou uspořádána počínaje levým horním rohem
 * (nejvyšší, tedy 64. bit) a postupují zleva doprava (druhé pole
 * prvního řádku je uloženo v 63. bitu, tj. druhém nejvyšším) po
 * řádcích zleva doprava (první pole druhého řádku je 56. bit),
 * atd., až po nejnižší (první) bit, který reprezentuje pravý dolní
 * roh.
 *
 * Predikát nechť je pravdivý právě tehdy, není-li žádná královna na
 * šachovnici ohrožena jinou. Program musí pracovat správně i pro
 * případy, kdy je na šachovnici jiný počet královen než 8.
 * Očekávaná složitost je v řádu 64² operací – totiž O(n²) kde ⟦n⟧
 * představuje počet políček.
 *
 * Poznámka: preferované řešení používá pro manipulaci se šachovnicí
 * pouze bitové operace a zejména nepoužívá standardní kontejnery.
 * Řešení, které bude nevhodně používat kontejnery (spadá sem např.
 * jakékoliv použití ‹std::vector›) nemůže získat známku A. */

/** Get rid of this function please, it does you more harm than good. **/
void modify_mask(int row, int col, std::uint64_t &mask, int dy, int dx){
    if (row >= 8 || row < 0 || col >= 8 || col < 0)
        return;
    mask |= 1ULL << (row * 8 + col );
    modify_mask(row + dy, col + dx, mask, dy, dx);
}

bool in_danger(int row, int col, std::uint64_t board){
    std::uint64_t mask = 0;
    // std::uint64_t &maskp = mask;
/** Idea is relatively fine, but get rid of the helper function… All you need to do
 ** is just go bit-by-bit to the end and check each position.
 **
 ** Your current solution does similar thing, but with the difference that it checks
 **  all positions at once, which… well, you can see, leads to a lot of copy-paste
 ** in this place…
 **
 ** If you don't feel like being able to reduce it to a simple loop, try to move the
 **  check to a helper function that will take the `dx, dy` and check it bit-by-bit
 ** instead of modifying the mask. Also one hint, try to think whether you have to
 ** go backwards or not, e.g. `dx = -1, dy = -1`. **/
    modify_mask(row + 1, col + 1, mask, 1, 1);
    modify_mask(row + 1, col - 1, mask, 1, -1);
    modify_mask(row - 1, col + 1, mask, -1, 1);
    modify_mask(row - 1, col - 1, mask, -1, -1);
    modify_mask(row, col + 1, mask, 0, 1);
    modify_mask(row, col - 1, mask, 0, -1);
    modify_mask(row + 1, col, mask, 1, 0);
    modify_mask(row - 1, col, mask, -1, 0);
    return (board & mask) > 0;
}

bool queens( std::uint64_t board ){
    std::uint64_t mask = 1;

    for (int row = 0; row < 8; ++row){

        for (int col = 0; col < 8; ++col, mask <<= 1){

            if ((board & mask) == 0) {
                continue;
            }

            if (in_danger(row, col, board))
                return false;
        
        }
    }
    return true;
}

int main()
{
    assert( queens( 0 ) );
    assert( !queens( 3 ) );
    // bool a = queens(1170937021957408770  );

    return 0;
}
