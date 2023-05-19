#include <cassert>

/* Nezáporná čísla ‹a›, ‹b› zapíšeme v poziční soustavě o základu
 * ‹base›. Spočtěte hammingovu vzdálenost těchto dvou zápisů (přitom
 * zápis kratšího čísla podle potřeby doplníme levostrannými
 * nulami). */

/** Some empty lines would help the readability, but otherwise a nice
 ** solution **/

int hamming( int a, int b, int base ){
    int res = 0;
    /** Imo a while loop would be better here, since you don't know how many
     ** times the loop will run  **/
    for (;a > 0 || b > 0; a /= base, b /= base){
        if (a % base != b % base){
            /** `res++` or `++res` might be a bit easier to read **/
            res += 1;
        }
    }
    return res;
}

int main()
{
    assert( hamming( 1, 3, 2 ) == 1 );
    assert( hamming( 1, 3, 3 ) == 2 );
    assert( hamming( 3, 3, 3 ) == 0 );
    assert( hamming( 0, 1, 3 ) == 1 );
    assert( hamming( 0, 2, 3 ) == 1 );

    return 0;
}
