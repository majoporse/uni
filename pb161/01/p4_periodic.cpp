#include <cstdint>
#include <cassert>
#include<iostream>
using namespace std;

/* Najděte nejmenší nezáporné číslo ⟦n⟧ takové, že 64-bitový zápis
 * čísla ‹word› lze získat zřetězením nějakého počtu binárně
 * zapsaných kopií ⟦n⟧. Protože potřebný zápis ⟦n⟧ může obsahovat
 * levostranné nuly, do výstupního parametru ‹length› uložte jeho
 * délku v bitech. Je-li možné ‹word› sestavit z různě dlouhých
 * zápisů nějakého ⟦n⟧, vyberte ten nejkratší možný.
 *
 * Příklad: pro ‹word = 0x100000001› bude hledané ⟦n = 1⟧, protože
 * ‹word› lze zapsat jako dvě kopie čísla 1 zapsaného do 32 bitů. */

std::uint64_t periodic( std::uint64_t word, int &length ){
    std::uint64_t res = word;
    std::uint64_t cmp = word;

    for (int exp = 6; exp >= 0; --exp){
        
        int num = 1<<exp;
        cmp >>= num;
        
        std::uint64_t cur = word;
        bool b = false;
        
        for (int i = 64/num - 1; i > 0; cur >>= num, --i){
            std::uint64_t a = 1UL<<(num);
            cout << num << " " << cmp << " "<< cur % a;
            if (cmp != (cur % a)){
                cout << "*";
                b = true;
                cout << "\n";
                break;
            }
            cout << "\n";
        }
        
        if (!b){
            length = num;
            res = cmp;
        }
    }
    cout <<length <<"\n" << res << "\n";
    return res;
}

int main()
{
    int length;

    assert( periodic( 0x100000001u, length ) == 1 );
    assert( length == 32 );
    assert( periodic( 0x1212121212121212u, length ) == 0x12 );
    assert( length == 8 );
    assert( periodic( 0x1234123412341234u, length ) == 0x1234 );
    assert( length == 16 );
    assert( periodic( 0, length ) == 0 );
    assert( length == 1 );
    assert( periodic( 1, length ) == 1 );
    assert( length == 64 );

    return 0;
}
