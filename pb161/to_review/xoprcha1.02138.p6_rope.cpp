#include <cassert>
#include <vector>
#include <memory>

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


struct rope_node
{
    bool is_leaf;
    std::vector<int> values;
    int left_size;
    std::shared_ptr<rope_node> left;
    std::shared_ptr<rope_node> right;
};

struct rope
{
    std::shared_ptr<rope_node> root;
    int size;

    rope(std::vector<int> input)
    {
        root = std::make_shared<rope_node>();
        root->is_leaf = true;
        root->left_size = input.size();
        size = input.size();
        root->values = std::move(input);
    }

    rope(rope &one, rope &two)
    {
        root = std::make_shared<rope_node>();
        root->is_leaf = false;
        root->left_size = one.size;
        size = one.size + two.size;

        root->left = one.root;
        root->right = two.root;
    }

    int &find(int index) const
    {
        rope_node *node = root.get();

        while(!node->is_leaf)
        {
            if (index < node->left_size)
            {
                node = node->left.get();
            }
            else
            {
                index -= node->left_size;
                node = node->right.get();
            }
        }

        return node->values[index];
    }

    int get(int index) const
    {
        return find(index);
    }

    void set(int index, int value)
    {
        find(index) = value;
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
