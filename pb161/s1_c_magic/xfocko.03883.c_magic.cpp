/** Grade: @C
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [!] clearly describes solution to the problem
 **   * `BIGGER` vs `SMALLER`: what do they mean? I understood from context that
 ** they signalize whether you successfully inserted a value into the field, but I
 ** have no clue how can you get something smaller when you're inserting numbers in
 ** place of the zeroes; Without any comments this part is rather hard to
 ** comprehend.
 **   * Empty branch: Please don't, it's related to the next point where I'll
 ** discuss it a bit further
 **   * `NO_CHECK`: If I understand correctly, you sometimes want to update the
 ** `unused` and sometimes not…You can easily notice that you're doing so »only« at
 ** the beginning, so I would recommend factoring that part, of preparing `unused`,
 ** to its own function and calling it only once at the beginning.
 **     Apart from that, there is a bit more elegant solution to this problem and
 ** that would utilize `optional<T>`, so you either get something or you don't and
 ** can easily decide based on that.
 **   * naming: `BIGGER`, `SMALLER`, `m_sum`, etc.
 **   * `get_unused`: Why do you need to pass in the reference, if you're not even
 ** using it? You use `min_num` with `cur` interchangebly, you need just one, I
 ** would remove `min_num` and keep the `cur`, since it requires least amount of
 ** changes to adjust.
 ** * [-] correctly decomposes the problem
 **   * `is_correct_whole` vs `is_correct_insert`: they are very similar; I would
 ** start with trying to compress all 4 “branches” to a loop (you know the direction
 **  (`dx, dy`), you can deduce the start, in case of diagonals (and in your case,
 ** of course) I cannot think about any elegant ways how to approach it, if you have
 **  some idea, let me know, I'll try to think about it a bit more)
 **   * `get_line_sum`: it's doing too many things, as I suggested above, try to
 ** take out the part that initializes `unused` and let the sum do just the sum and
 ** nothing else
 ** * [!] doesn't have code duplication
 **   * `std::sqrt`, you can feel free to use the built-in implementation
 **   * also related to the previous point
 **   * you could implement `get_unused` with `std::find`
 ** * [x] uses correct abstractions, algorithms and data structures
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * n/a
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <vector>
#include <cstdint>
#include <cassert>
#include <set>

#define BIGGER 1
#define SMALLER 2

/* Magický čtverec je čtvercová síť o rozměru ⟦n × n⟧, kde
 *
 *  1. každé políčko obsahuje jedno z čísel ⟦1⟧ až ⟦n²⟧ (a to tak,
 *     že se žádné z nich neopakuje), a
 *  2. má tzv. «magickou vlastnost»: součet každého sloupce, řádku a
 *     obou diagonál je stejný. Tomuto součtu říkáme „magická
 *     konstanta“.
 *
 * Částečný čtverec je takový, ve kterém mohou (ale nemusí) být
 * některá pole prázdná. Vyřešením částečného čtverce pak myslíme
 * doplnění případných prázdných míst ve čtvercové síti tak, aby měl
 * výsledný čtverec obě výše uvedené vlastnosti. Může se samozřejmě
 * stát, že síť takto doplnit nelze. */

using magic = std::vector< std::int16_t >;

/* Vaším úkolem je naprogramovat backtrackující solver, který
 * čtverec doplní (je-li to možné), nebo rozhodne, že takové
 * doplnění možné není.
 *
 * Napište podprogram ‹magic_solve›, o kterém platí:
 *
 *  • návratová hodnota (typu ‹bool›) indikuje, bylo-li možné
 *    vstupní čtverec doplnit,
 *  • parametr ‹in› specifikuje částečný čtverec, ve kterém jsou
 *    prázdná pole reprezentována hodnotou 0, a který je
 *    uspořádaný po řádcích a na indexu 0 je levý horní roh,
 *  • je-li výsledkem hodnota ‹true›, zapíše zároveň doplněný
 *    čtverec do výstupního parametru ‹out› (v opačném případě
 *    parametr ‹out› nezmění),
 *  • vstupní podmínkou je, že velikost vektoru ‹in› je druhou
 *    mocninou, ale o stavu předaného vektoru ‹out› nic předpokládat
 *    nesmíte.
 *
 * Složitost výpočtu může být až exponenciální vůči počtu prázdných
 * polí, ale solver nesmí prohledávat stavy, o kterých lze v čase
 * ⟦O(n²)⟧ rozhodnout, že je doplnit nelze. Prázdná pole vyplňujte
 * počínaje levým horním rohem po řádcích (alternativou je zajistit,
 * že výpočet v jiném pořadí nebude výrazně pomalejší). */


/** `std::sqrt` is a thing. **/
int square_root(int x)
{
    int n = 0;
    while (n*n < x) n++;
    return n;
}

int get_sum(int n){
    return (n * (n*n +1)) / 2;
}


int get_line_sum(int x, int y,const magic &square, int side, int dx, int dy, bool &full, std::vector<bool> &used){

    int sum = 0;
    for (int cur; x < side && x >= 0 && y < side && y >= 0; x += dx, y += dy){
        
        cur = square[x + y * side];
        sum += cur;

        if (full && cur == 0)
            full = false;

/** Why? If it does nothing. **/
        else if (cur == 0 || used.empty()) {}

        else if (!used[square.size() - cur + 1]) //numbers are represented backwards for easier iteration
            used[square.size() - cur + 1] = true;

        else
/** So you set an error flag and carry on with your life? Not sure how helpful this
 ** error flag is then, you even finish the outer loop from which you're calling
 ** this function. **/
            used[0] = true; // this means error because 0 cannot be used
    }
    return sum;
}

int is_correct_insert(const magic &square, int x, int y, int m_sum, int side){
    std::vector<bool> NO_CHECK = {};
    
    bool full = true;
    int sum_row = get_line_sum(0, y, square, side, 1, 0, full, NO_CHECK);

    if (sum_row > m_sum || (full && (m_sum != sum_row))) 
        return (sum_row > m_sum) ? BIGGER : SMALLER;
    
    full = true;
    int sum_col = get_line_sum(x, 0, square, side, 0, 1, full, NO_CHECK);

    if (sum_col > m_sum || (full && (m_sum != sum_col)))
        return (sum_col > m_sum) ? BIGGER : SMALLER;
    
    if (y == -x + side -1) { //this means that [x, y] is on a diagonal
        full = true;
        int sum_diar = get_line_sum(side - 1, 0, square, side, -1, 1, full, NO_CHECK);
    
        if (sum_diar > m_sum || (full && (m_sum != sum_diar)))
            return (sum_diar > m_sum) ? BIGGER : SMALLER;
    }
    
    if (x == y){
        full = true;
        int sum_dial = get_line_sum(0, 0, square, side, 1, 1, full, NO_CHECK);

        if (sum_dial > m_sum || (full && (m_sum != sum_dial))) 
            return (sum_dial > m_sum) ? BIGGER : SMALLER;
    }
    return 0;
}

bool is_correct_whole(const magic &square, int side, std::vector<bool> &used, int m_sum){
/** What? Why is it in upper-case if it's not a constant? **/
    std::vector<bool> NO_CHECK = {};
    
    int sum_row;
    int sum_col;
    bool full;

    for (int x = 0, y = 0; x < side && y < side; ++x, ++y){
        full = true;
/** ```suggestion:-0+0
 **         int sum_row = get_line_sum(0, y, square, side, 1, 0, full, used);
 ** ```
 **
 ** And remove the declaration before the loop; similarly for the column **/
        sum_row = get_line_sum(0, y, square, side, 1, 0, full, used);

        if (full && (m_sum != sum_row)) 
            return false;

        full = true;
        sum_col = get_line_sum(x, 0, square, side, 0, 1, full, NO_CHECK);

        if (full && (m_sum != sum_col)) 
            return false;
    }

    if (used[0])
        return false;

    full = true; 
    int sum_dial = get_line_sum(0, 0, square, side, 1, 1, full, NO_CHECK);

    if (full && (m_sum != sum_dial)) 
        return false;

    full = true;
    int sum_diar = get_line_sum(side - 1, 0, square, side, -1, 1, full, NO_CHECK);

    return !full || (m_sum == sum_diar);
}

/** This is a relatively simple function based on what you want it to do, but you're
 **  overengineering stuff without any need.
 **
 ** 1º Switch the references… You're making it very complicated
 **    • You're passing `used` as a value, it gets copied ⇒ each time you call this
 ** function you make a copy of the `vector` that you don't even modify! Switch it
 ** to `const std::vector<bool>&`
 **    • `min_num` via reference; You return that value from the function, I'm
 ** trying to wrap my head around what you have going on here, cause it's very hard
 ** to follow and this definitely doesn't help it.
 **
 ** 2º You have the `used` offset by 1 (zero index for error), just use `min_num` as
 **  index (passed in by-value) and simply use a for loop and return it. There's no
 ** need to complicate it like this. **/
int get_unused(std::vector<bool> used, int &min_num){
    ++min_num;
    auto it = used.begin() + min_num;

    for(;it != used.end(); ++it){
        if (!*it){
            min_num = it - used.begin();
            return min_num;
        }
    }
    return -1;
}

bool try_solve(magic &square, int side, std::size_t pos, std::vector<bool> &used, int m_sum){
    int cur;

    int x = pos % side;
    int y = pos / side;
    int min_num = 0;

    if (pos >= square.size())
        return true;

/** I wouldn't abuse the recursion that much… IMO it's enough to do here something
 ** like:
 **
 **     while (pos < square.size() && square[pos] != 0) {
 **         pos++;
 **     }
 **
 **     if (pos >= square.size()) {
 **         return true;
 **     } **/
    if (square[pos] != 0)
        return try_solve(square, side, pos + 1, used, m_sum);

    for(;(cur = get_unused(used, min_num)) != -1; square[pos] = 0){
        int cur1 = side*side - cur + 1;
        square[pos] = cur1;

        int state;
        if ((state = is_correct_insert(square, x, y, m_sum, side)) == BIGGER)
            continue;
/** How can you get smaller value when you add something to the field? **/
        else if (state == SMALLER){
            square[pos] = 0;
            break;
        }
        
        used[cur] = true;

        if (try_solve(square, side, pos + 1, used, m_sum))
            return true;

        used[cur] = false;
    }
    return false;
}

bool magic_solve( const magic &in, magic &out ){
/** You could also substitute one when indexing. **/
    std::vector<bool> used(in.size() + 1, false);
    int side = square_root(in.size());
    int m_sum = get_sum(side);
    if (side == 0)
        return false;

    if (!is_correct_whole(in, side, used, m_sum))
        return false;
    magic res = in;
    if (try_solve(res, side, 0, used, m_sum)){
        out = res;
        return true;
    }
    return false;
}

int main()
{
    magic test = {  2, 16, 13,  3,
                    11,  5,  8,  0,
                    7,  9, 12,  6,
                    14,  4,  1, 15,
                  };

    
    magic in{ 0 }, out = {};
    magic_solve(test, out);
    assert( magic_solve( in, out ) );
    assert( out.size() == 1 );
    assert( out[ 0 ] == 1 );

    return 0;
}
