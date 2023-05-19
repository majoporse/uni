#include <cassert>
#include <stdexcept>
#include <vector>

/* Naprogramujte typ ‹queue›, který bude reprezentovat «omezenou»
 * frontu celých čísel (velikost fronty je zadaná jako parametr
 * konstruktoru), s metodami:
 *
 *   • ‹pop()› – vrátí nejstarší vložený prvek,
 *   • ‹push( x )› – vloží nový prvek ‹x› na konec fronty,
 *   • ‹empty()› vrátí ‹true› je-li fronta prázdná.
 *
 * Metody ‹pop› a ‹push› nechť v případě selhání skončí výjimkou
 * ‹queue_empty› resp. ‹queue_full›. Všechny operace musí mít
 * složitost O(1). Metody ‹push› ani ‹pop› nesmí alokovat dodatečnou
 * paměť. */

struct queue_empty : public std::runtime_error
{
public:
    queue_empty() : std::runtime_error( "queue empty" ) {}
};
struct queue_full : public std::runtime_error
{
public:
    queue_full() : std::runtime_error( "queue full" ) {}
};

struct queue
{
    std::vector< int > data;
    size_t front_index = 0;
    size_t back_index = 0;
    bool _empty = true;

    queue( int size ) : data( size ) {}

    bool empty() { return _empty; }
    int pop()
    {
        if ( _empty ) throw queue_empty();

        int old = front_index++;
        front_index %= data.size();
        _empty = back_index == front_index;
        return data[ old ];
    }

    void push( int input )
    {
        if ( !_empty && front_index == back_index ) throw queue_full();
        int old = back_index++;
        back_index %= data.size();
        data[ old ] = input;
        _empty = false;
    }
};

int main()
{
    queue q( 4 );
    assert( q.empty() );

    {
        bool throws = false;
        try
        {
            q.pop();
        }
        catch ( queue_empty & )
        {
            throws = true;
        }

        assert( throws );
    }

    q.push( 42 );
    assert( !q.empty() );
    q.push( 1729 );
    q.push( 6174 );
    q.push( 2520 );

    assert( q.pop() == 42 );
    q.push( 3435 );

    {
        bool throws = false;
        try
        {
            q.push( 666 );
        }
        catch ( queue_full & )
        {
            throws = true;
        }

        assert( throws );
    }

    assert( q.pop() == 1729 );
    assert( q.pop() == 6174 );

    return 0;
}
