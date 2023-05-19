#include <cassert>
#include <sstream>
#include <string>
#include <set>

/* Implementujte typ ‹set›, který reprezentuje množinu libovolných
 * celých čísel, s operacemi:
 *
 *  • ‹add› – přidá prvek,
 *  • ‹has› – ověří přítomnost prvku,
 *  • ‹size› – vrátí počet prvků.
 *
 * Dále nechť je hodnoty typu ‹set› možné číst z a zapisovat do
 * vstupně-výstupních proudů. Na výstupu budou mít množiny tuto
 * formu:
 *
 *     {}
 *     { 1 }
 *     { 1, 2 }
 *
 * Na vstupu akceptujte i varianty s jiným počtem bílých znaků
 * (včetně žádných). */

struct set{
    std::set<int> m;
    void add( int x )       { m.insert( x ); }
    bool has( int x ) const { return m.count( x ) > 0;}
    int size()        const { return static_cast<int>(m.size()); }
    friend std::ostream& operator<<( std::ostream& os , const set& s){
        os << '{';
        if (s.m.empty()){
            os << '}';
            return os;
        }
        for (int i: s.m){
            os << ' ' << i;
            if (i !=  *s.m.rbegin())
                os << ',';
        }
        os << " }";
        return os;
    }

    friend std::istream& operator>>( std::istream& is , set& s){
        s.m.clear();
        char dummy;
        is >> dummy;
        int i;
        while (is >> i){
            s.add( i );
            is >> dummy;
        }
        is.clear();
        if (dummy != '}')
            is >> dummy;
        return is;
    }
};

int main()
{
    std::stringstream s( "{3} {} {1} {1 } {1 ,2}" );
    set m;
    const auto &const_m = m;

    s >> m;
    assert( s && m.size() == 1 && m.has( 3 ) );
    s >> m;
    assert( s && const_m.size() == 0 && !m.has( 3 ) );
    s >> m;
    assert( s && m.size() == 1 && m.has( 1 ) );
    s >> m;
    assert( s && m.size() == 1 && const_m.has( 1 ) );
    s >> m;
    assert( s && m.size() == 2 && m.has( 1 ) && m.has( 2 ) );

    set n, o;
    n.add( 1 );

    s.str( "" );
    s.clear();

    s << const_m << " " << n << " " << o;
    assert( s.str() == "{ 1, 2 } { 1 } {}" );

    return 0;
}
