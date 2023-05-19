#include <cstdint>
#include <cassert>
// #include<iostream>

/* Vstupem pro problém «subset sum» je množina povolených čísel ⟦A⟧
 * a hledaný součet ⟦n⟧. Řešením je pak podmnožina ⟦B ⊆ A⟧ taková,
 * že součet jejích prvků je právě ⟦n⟧.
 *
 * V tomto příkladu budeme pracovat pouze s množinami ⟦A⟧, které
 * obsahují kladná čísla ostře menší než 64, a které lze tedy
 * reprezentovat jediným bezznaménkovým číslem z rozsahu ⟦0⟧
 * (prázdná množina) až ⟦2⁶⁴ - 1⟧ (obsahuje všechna čísla ⟦1, 2, …,
 * 63⟧). Číslo ⟦1⟧ pak reprezentuje množinu ⟦{1}⟧, číslo ⟦2⟧ množinu
 * ⟦{2}⟧, číslo ⟦3⟧ množinu ⟦{1, 2}⟧ atd.
 *
 * Vašim úkolem je napsat funkci ‹subset_sum›, které výsledkem bude
 * ‹true›, má-li zadaná instance řešení. Toto řešení zároveň zapíše
 * do výstupního parametru. V případě, že řešení neexistuje, hodnotu
 * ‹solution› nijak neměňte. */

bool subset_sum( int n, std::uint64_t allowed,
                  std::uint64_t &solution ){
                    
    if (n < 0){
        return false;
    }

    if (n == 0){
        solution = 0;
        return true;
    }

    for(int i = 0; i < 64; ++i){
        
        std::uint64_t cur = 1UL<<i;
        if((allowed & cur) != cur){
            continue;
        } 
        
        if (subset_sum(n - i -1, allowed - cur, solution)){
            solution |= cur;
            // std::cout << n << "  " << allowed << "  " << solution << "\n";
            return true;
        }
    }
    // std::cout << n << "  " << allowed << "  " << solution << "\n";
    return false;
}

int main()
{
    std::uint64_t solution = 3;

    assert( !subset_sum( 1, 0b10, solution ) && solution == 3 );
    assert( subset_sum( 3, 0b11, solution ) && solution == 0b11 );

    assert( subset_sum( 5, 0b1111, solution ) );
    assert( solution == 0b0110 || solution == 0b1001 );

    assert( subset_sum( 7, 0b01101, solution ) && solution == 0b01100 );
    assert( subset_sum( 7, 0b10111, solution ) && solution == 0b10010 );

    return 0;
}
