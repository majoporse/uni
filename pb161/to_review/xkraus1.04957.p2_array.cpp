#include <climits>
#include <cassert>
#include <vector>
#include <tuple>
#include <stdexcept>

/* Implementujte dvourozměrné pole, kde vnitřní pole na daném indexu
 * může být buď obyčejné pole celých čísel (‹std::vector›), nebo
 * konstantní pole neomezené délky, nebo neomezené pole, kde hodnota
 * na libovolném indexu je rovna tomuto indexu. Metody:
 *
 *  • ‹a.get( i, j )› vrátí hodnotu (typu ‹int›) na zadaných
 *    souřadnicích, nebo vyhodí výjimku ‹std::out_of_range›, není-li
 *    některý index platný,
 *  • ‹a.size()› vrátí délku vnějšího pole,
 *  • ‹a.size( i )› vrátí délku ‹i›-tého vnitřního pole (pro
 *    neomezená vnitřní pole vrátí ‹INT_MAX›),
 *  • po volání ‹a.append_iota()› pro libovolné ‹i› platí
 *    ‹a.get( a.size() - 1, i ) == i›,
 *  • po volání ‹a.append_const( n )› pro libovolné ‹i› platí
 *    ‹a.get( a.size() - 1, i ) == n›,
 *  • pro vektor čísel ‹v› volání ‹a.append( v )› vloží ‹v› jako
 *    poslední prvek vnějšího pole ‹a›. */

struct array {
    using intvec = std::vector<int>;    

    enum class type {
        iota,
        constant,
        vector
    };

    std::vector<std::pair<type, intvec>> arr;

    int size() const { return arr.size(); }

    int size( int i ) const {
        switch ( arr[i].first ) {
            case type::iota:
            case type::constant:
                return INT_MAX;
            case type::vector:
                return arr[i].second.size();
        }

        assert( false );
    }

    int get( int i, int j ) const {
        if ( i >= size() ) {
            throw std::out_of_range( "i is out of range" );
        }

        if ( j >= size( i ) ) {
            throw std::out_of_range( "j is out of range" );
        }

        switch ( arr[i].first ) {
            case type::iota:
                return j;
            case type::constant:
                return arr[i].second[0];
            case type::vector:
                return arr[i].second[j];
        }

        assert( false );
    }

    void append_iota() {
        arr.emplace_back( type::iota, intvec{} );
    }

    void append_const( int n ) {
        arr.emplace_back( type::constant, intvec{ n } );
    }

    void append( const intvec & v ) {
        arr.emplace_back( type::vector, v );
    }
};

int main()
{
    array arr{};

    assert( arr.size() == 0 );

    try
    {
        arr.get( 2, 0 );
        assert( false );
    } catch ( std::out_of_range & ) {}

    arr.append_iota();
    arr.append_const( 10 );

    assert( arr.size() == 2 );
    assert( arr.get( 0, 150 ) == 150 );
    assert( arr.get( 1, 35 ) == 10 );
    assert( arr.size( 0 ) == INT_MAX );
    assert( arr.size( 1 ) == INT_MAX );

    arr.append( { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 } );
    assert( arr.size() == 3 );
    assert( arr.get( 0, 7 ) == 7 );
    assert( arr.size( 2 ) == 11 );

    try
    {
        arr.get( 2, 14 );
        assert( false );
    }
    catch ( std::out_of_range & ) {}

    return 0;
}
