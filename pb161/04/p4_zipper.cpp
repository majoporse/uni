#include <cassert>
#include <vector>

/* V tomto příkladu implementujeme jednoduchou datovou strukturu,
 * které se říká «zipper» – reprezentuje sekvenci prvků, přitom
 * právě jeden z nich je «aktivní» (angl. focused). Abychom se
 * nemuseli zabývat generickými datovými typy, vystačíme si
 * celočíselnými položkami. Typ ‹zipper› nechť má toto rozhraní:
 *
 *  • konstruktor vytvoří jednoprvkový ‹zipper› z celého čísla,
 *  • ‹shift_left› (‹shift_right›) aktivuje prvek vlevo (vpravo) od
 *    toho dosud aktivního, a to v čase O(1); metody vrací ‹true›
 *    bylo-li posun možné provést (jinak nic nezmění a vrátí
 *    ‹false›),
 *  • ‹insert_left› (‹insert_right›) přidá nový prvek těsně vlevo
 *    (vpravo) od právě aktivního prvku (opět v čase O(1))
 *  • ‹focus› zpřístupní aktivní prvek (pro čtení i zápis)
 *    
 *  • «volitelně» metody ‹erase_left› (‹erase_right›) které odstraní
 *    prvek nalevo (napravo) od aktivního, v čase O(1), a vrátí
 *    ‹true› bylo-li to možné
 */

struct zipper{

    std::vector<int> datal;
    std::vector<int> datar;
    int activated;

    zipper(int i): activated{i} {}

    bool shift_left(){
        if (datal.empty())
            return false;
        datar.emplace_back(activated);
        activated = datal.back();
        datal.pop_back();
        return true;
    }

    bool shift_right(){
        if (datar.empty())
            return false;
        datal.emplace_back(activated);
        activated = datar.back();
        datar.pop_back();
        return true;
    }

    void insert_left(int i){
        datal.emplace_back(i);
    }

    void insert_right(int i){
        datar.emplace_back(i);
    }

    bool erase_left(){
        if (datal.empty())
            return false;
        datal.pop_back();
        return true;
    }

    bool erase_right(){
        if (datar.empty())
            return false;
        datar.pop_back();
        return true;
    }

    const int &focus()const{
        return activated;
    }
    int &focus(){
        return activated;
    }
};

int main()
{
    zipper a( 7 ); // [7]
    const zipper &c = a;

    assert( c.focus() == 7 ); /* constant read works */
    assert( !a.shift_left() );
    assert( c.focus() == 7 );
    assert( !a.shift_right() );
    assert( c.focus() == 7 );

    a.insert_left( 3 );        // 3 [7]
    assert( c.focus() == 7 );
    assert( a.shift_left() );  // [3] 7
    assert( c.focus() == 3 );
    assert( !a.shift_left() );
    assert( a.shift_right() ); // 3 [7]
    assert( c.focus() == 7 );
    assert( !a.shift_right() );

    zipper b = a;

    a.insert_left( 2 );   // 3 2 [7]
    a.insert_right( 4 );  // 3 2 [7] 4
    a.insert_right( 11 ); // 3 2 [7] 11 4
    a.focus() = 8; /* assignment to focus() works */

    assert( c.focus() == 8 );
    assert( a.shift_right() ); // 3 2 8 [11] 4
    assert( c.focus() == 11 );
    assert( a.shift_right() ); // 3 2 8 11 [4]
    assert( !a.shift_right() );

    assert( a.shift_left() ); // 3 2 8 [11] 4
    assert( a.focus() == 11 );
    assert( a.shift_left() ); // 3 2 [8] 11 4
    assert( a.focus() == 8 );
    assert( a.shift_left() ); // 3 [2] 8 11 4
    assert( a.focus() == 2 );
    assert( a.shift_left() ); // [3] 2 8 11 4
    assert( a.focus() == 3 );
    assert( !a.shift_left() );

    assert( b.focus() == 7 );
    assert( !b.shift_right() );

    return 0;
}
