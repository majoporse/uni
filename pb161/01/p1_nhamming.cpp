#include <cassert>

/* Nezáporná čísla ‹a›, ‹b› zapíšeme v poziční soustavě o základu
 * ‹base›. Spočtěte hammingovu vzdálenost těchto dvou zápisů (přitom
 * zápis kratšího čísla podle potřeby doplníme levostrannými
 * nulami). */

int hamming( int a, int b, int base ){
    int res = 0;
    for (;a > 0 || b > 0; a /= base, b /= base){
        if (a % base != b % base){
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
