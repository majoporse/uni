#include <vector>
#include <cstdint>
#include <cassert>
#include <set>
#include <cmath>

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

        else if (cur == 0 || used.empty()) {}

        else if (!used[square.size() - cur + 1]) //numbers are represented backwards for easier iteration
            used[square.size() - cur + 1] = true;

        else
            used[0] = true; // this means error because 0 cannot be used
    }
    return sum;
}

int is_correct_insert(const magic &square, int x, int y, int m_sum, int side){
    std::vector<bool> NO_CHECK;
    
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
    std::vector<bool> NO_CHECK;
    
    int sum_row;
    int sum_col;
    bool full;

    for (int x = 0, y = 0; x < side && y < side; ++x, ++y){
        full = true;
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

    if (square[pos] != 0)
        return try_solve(square, side, pos + 1, used, m_sum);

    for(;(cur = get_unused(used, min_num)) != -1; square[pos] = 0){
        int cur1 = side*side - cur + 1;
        square[pos] = cur1;

        int state;
        if ((state = is_correct_insert(square, x, y, m_sum, side)) == BIGGER)
            continue;
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
    std::vector<bool> used(in.size() + 1, false);
    int side = std::sqrt(in.size());
    int m_sum = (side * (side*side +1)) / 2;;
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
