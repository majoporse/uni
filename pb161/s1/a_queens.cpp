#include <cstdint>
#include <cassert>
#include <cmath>

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

/* I tried to remove the code duplication and came up with this. 
I think, that having this function increases readability of the 
code instead of not having it. I changed it so it doesn't have to always 
compute the mask so it can detect colisions quicker.*/

bool danger_on_line(int row, int col, std::uint64_t &board, int dy, int dx){

    row += dy;
    col += dx;

    for (;row < 8 && row >= 0 && col < 8 && col >= 0; row += dy, col += dx){
        if ((board & (1ULL << (row * 8 + col))) > 0){
            return true;
        }
    }
    return false;
}

bool in_danger(int row, int col, std::uint64_t &board){

    for (int dx = -1; dx < 2; ++dx){
        for (int dy = -1; dy < 2;++dy){
            if (dy == 0 && dx == 0)
                continue;

            if(danger_on_line(row, col, board, dy, dx))
                return true;
        }
    }
    return false;
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
    // assert( queens( 0 ) );
    // assert( !queens( 3 ) );
    bool a = queens(1170937021957408770);
    assert(a);
    return 0;
}
