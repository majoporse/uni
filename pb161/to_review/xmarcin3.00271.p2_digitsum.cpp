#include <cassert>

/* Funkce ‹digit_sum› sečte cifry nezáporného čísla ‹num› v zápisu
 * o základu ‹base›. Je-li výsledek ve stejném zápisu víceciferný,
 * sečte cifry tohoto výsledku, atd., až je výsledkem jediná cifra,
 * kterou vrátí jako svůj výsledek. */

int digit_sum(int num, int base)
{
    assert(num >= 0);

    int result = num;

    while (result >= base) {
        int tmp_result = 0;

        while (result > 0) {
            tmp_result += result % base;
            result /= base;
        }

        result = tmp_result;
    }

    return result;
}

int main()
{
    assert( digit_sum( 0b1, 2 ) == 1 );
    assert( digit_sum( 0b11, 2 ) == 1 );
    assert( digit_sum( 0b111, 2 ) == 1 );
    assert( digit_sum( 731, 10 ) == 2 );
    assert( digit_sum( 777, 8 ) == 7 );

    // my tests
    // assert(digit_sum( 7777, 8 ) == 7);

    return 0;
}
