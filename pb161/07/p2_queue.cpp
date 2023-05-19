#include <cassert>
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

struct queue_empty{};
struct queue_full{};


struct queue{
private:
    std::vector< int > data;

public:
    int front = -1, rear = -1;
    int size;

    queue(int size) :data{std::vector< int >(size, 0)}, size{size} {}
    void push(int val) {
        if ((front == 0 && rear == size-1) || (front == rear+1))
            throw queue_full();
        
        if (front == -1) {
            front = 0;
            rear = 0;
        } else {
            if (rear == size - 1)
            rear = 0;
            else
            rear = rear + 1;
        }
        data[rear] = val ;
    }

    int pop() {
        if (front == -1)
            throw queue_empty();
        
        int res = data[front];
        
        if (front == rear) {
            front = -1;
            rear = -1;
        } else {
            if (front == size - 1)
                front = 0;
            else
                front = front + 1;
        }
        return res;
    }

    bool empty(){return front == -1;}

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
        } catch ( queue_full & )
        {
            throws = true;
        }

        assert( throws );
    }

    assert( q.pop() == 1729 );
    assert( q.pop() == 6174 );

    return 0;
}
