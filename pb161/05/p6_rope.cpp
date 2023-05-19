#include <cassert>
#include <memory>
#include <vector>

/* Lano je datová struktura, která reprezentuje sekvenci,
 * implementovaná jako binární strom, který má v listech klasická
 * pole a ve vnitřních uzlech udržuje celočíselné váhy. Sdílení
 * podstromů je dovolené a očekávané.
 *
 * Váhou uzlu se myslí celková délka sekvence reprezentovaná jeho
 * levým podstromem. Díky tomu lze lana spojovat v konstantním čase,
 * a indexovat v čase lineárním k «hloubce» stromu.
 *
 * Naprogramujte:
 *
 *  • konstruktor, který vytvoří jednouzlové lano z vektoru,
 *  • konstruktor, který spojí dvě stávající lana,
 *  • metodu ‹get( i )›, která získá ‹i›-tý prvek,
 *  • a ‹set( i, value )›, která ‹i›-tý prvek nastaví na ‹value›.
 *
 * Pro účely tohoto příkladu není potřeba implementovat žádnou formu
 * vyvažování. */

struct node{
    int whole;
    std::vector< int > values;
    std::shared_ptr< node > l = nullptr;
    std::shared_ptr< node > r = nullptr;
};

struct rope{
    std::shared_ptr< node > root;

    rope(std::vector< int > n){
        root = std::make_shared< node >();
        root->values = n;
        root->whole = n.size();
    }

    rope( rope &a, rope &b){
        root = std::make_shared< node >();
        root->l = a.root;
        root->r = b.root;
        root->whole = a.root->whole + b.root->whole;
    }

    int get(int i)const{
        node *cur = root.get();
        while (cur->l != nullptr && cur->r != nullptr){
            if (i < cur->l->whole){
                cur = cur->l.get();
            } else{
                i -= cur->l->whole;
                cur = cur->r.get();
            }
        }
        return cur->values[i];
    }

    void set(int i, int n){

        node *cur = root.get();
        while (cur->l != nullptr && cur->r != nullptr){
            if (i < cur->l->whole){
                cur = cur->l.get();
            } else{
                i -= cur->l->whole;
                cur = cur->r.get();
            }
        }
        cur->values[i] = n;
    }
};

int main()
{
    rope h( { 104, 101, 108, 108, 111 } ),
         w( { 119, 111, 114, 108, 100 } );

    assert( h.get( 0 ) == 104 );
    assert( h.get( 4 ) == 111 );
    assert( w.get( 0 ) == 119 );
    assert( w.get( 4 ) == 100 );

    rope hw( h, w );
    assert( hw.get( 0 ) == 104 );
    assert( hw.get( 4 ) == 111 );
    assert( hw.get( 5 ) == 119 );
    assert( hw.get( 9 ) == 100 );

    rope hww( hw, w );
    assert( hww.get(  0 ) == 104 );
    assert( hww.get(  4 ) == 111 );
    assert( hww.get(  5 ) == 119 );
    assert( hww.get(  9 ) == 100 );
    assert( hww.get( 10 ) == 119 );
    assert( hww.get( 14 ) == 100 );

    const rope hhw( h, hw );
    assert( hhw.get( 0 ) == 104 );
    assert( hhw.get( 4 ) == 111 );
    assert( hhw.get( 5 ) == 104 );
    assert( hhw.get( 9 ) == 111 );
    assert( hhw.get( 10 ) == 119 );
    assert( hhw.get( 14 ) == 100 );

    h.set( 0, 120 );
    assert( h.get( 0 ) == 120 );
    assert( h.get( 4 ) == 111 );
    assert( w.get( 0 ) == 119 );
    assert( w.get( 4 ) == 100 );

    /* subtrees are shared */
    assert( hhw.get( 0 ) == 'x' );

    return 0;
}
