#include <cassert>
#include <cstdint>
#include <vector>
#include <ranges>

/* Vaším úkolem je vytvořit typ ‹mountain_range›, který bude
 * reprezentovat rekurzivní pohoří. Rekurzivní pohoří má tento tvar:
 *
 *  1. levý svah (může být prázdný), který může na každém kroku
 *     libovolně stoupat,
 *  2. libovolný počet (i nula) vnitřních pohoří stejného typu
 *     (první z nich začíná ve výšce, na které skončil levý svah),
 *  3. pravý svah, který je zrcadlovým obrazem toho levého.
 *
 * Například (hlavní pohoří má prázdný svah; závorky naznačují
 * začátky a konce jednotlivých vnitřních pohoří):
 * 
 * 
 * pohori h + List[pohorie] + svah^-1
 *
 *          ┌───┐                   ┌───┐
 *          │   │ ┌───┐     ┌───┐ ┌─┘   └─┐
 *        ┌─┘   └─┘   │   ┌─┘   └─┘       │
 *      ┌─┘           └───┘               └─┐
 *     ╶┘                                   └╴
 *       1 2 4 4 2 3 3 1 1 2 3 3 2 3 4 4 3 1
 *       ( (     )     ) ( (     ) (     ) )
 *
 * Je-li ‹outer› hodnota typu ‹mountain_range›, nechť:
 *
 *  1. ‹outer.get( i )› vrátí výšku ‹i›-tého pole pohoří ‹outer›, a
 *  2. ‹outer.set_slope( slope )› pro zadaný vektor čísel ‹slope›
 *     nastaví «oba» svahy tak, aby ten «levý» odpovídal výškám
 *     v ‹slope›,
 *  2. ‹outer.insert( inner )› vloží nové vnitřní pohoří zadané
 *     hodnotou ‹inner› typu ‹mountain_range›, a to těsně před pravý
 *     svah.
 *
 * Dobře si rozmyslete vhodnou reprezentaci. Požadujeme:
 *
 *  • metoda ‹get› musí mít konstantní složitost,
 *  • metoda ‹set_slope› může být vůči argumentu lineární, ale nesmí
 *    záviset na délce vnitřních pohoří,
 *  • metoda ‹insert› může být vůči vkládanému pohoří (‹inner›)
 *    lineární, vůči tomu vnějšímu (‹outer›) ale musí být
 *    amortizovaně konstantní.
 *
 * Nově vytvořená hodnota typu ‹mountain_range› reprezentuje prázdné
 * pohoří (prázdný svah a žádná vnitřní pohoří). */

struct mountain_range{
    std::vector<int> slope;
    std::vector<int> mountains;

    int get( std::size_t i)const{
        if (i < slope.size())
            return slope[i];
        if (i >= slope.size() + mountains.size())
            return slope[2 * slope.size() + mountains.size() - i - 1];
        
        return mountains[i - slope.size()];
    }

    void set_slope(std::vector<int> new_slope){
        slope = new_slope;
    }

    void insert(mountain_range m){
        for (int i : m.slope)
            mountains.emplace_back(i + slope.back());
        
        for (int i : m.mountains)
            mountains.emplace_back(i + slope.back());
        
        for (std::size_t i = 0; i < m.slope.size(); ++i)
            mountains.emplace_back(m.slope[m.slope.size() - i -1] + slope.back());
    }
};

int main()
{
    mountain_range a, b;
    a.set_slope( { 1, 2 } );

    assert( a.get( 0 ) == 1 );
    assert( a.get( 1 ) == 2 );
    assert( a.get( 2 ) == 2 );
    assert( a.get( 3 ) == 1 );

    b = a;
    a.insert( b );

    assert( a.get( 0 ) == 1 );
    assert( a.get( 1 ) == 2 );
    assert( a.get( 2 ) == 3 );
    assert( a.get( 3 ) == 4 );
    assert( a.get( 4 ) == 4 );
    assert( a.get( 5 ) == 3 );
    assert( a.get( 6 ) == 2 );
    assert( a.get( 7 ) == 1 );

    a.insert( b );
    const mountain_range &c = a;

    assert( c.get( 0 ) == 1 );
    assert( c.get( 1 ) == 2 );
    assert( c.get( 2 ) == 3 );
    assert( c.get( 3 ) == 4 );
    assert( c.get( 4 ) == 4 );
    assert( c.get( 5 ) == 3 );
    assert( c.get( 6 ) == 3 );
    assert( c.get( 7 ) == 4 );
    assert( c.get( 8 ) == 4 );
    assert( c.get( 9 ) == 3 );
    assert( c.get( 10 ) == 2 );
    assert( c.get( 11 ) == 1 );

    return 0;
}
