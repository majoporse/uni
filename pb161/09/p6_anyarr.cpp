#include <cassert>
#include <any>
#include <vector>
#include <functional>

/* Naprogramujte typ ‹any_array›, který bude reprezentovat dynamické
 * pole libovolných hodnot, a bude mít tyto metody:
 *
 *  • ‹size› – vrátí počet uložených hodnot,
 *  • ‹append› – přijme hodnotu libovolného typu a vloží ji
 *    na konec pole,
 *  • ‹transform_int› – přijme libovolnou unární funkci
 *    ‹int f( int )›, a každou uloženou hodnotu ‹x› typu ‹int›
 *    upraví na ‹f( x )› (přitom ostatní hodnoty nezmění),
 *  • ‹remove_integers› – odstraní hodnoty typu ‹int›,
 *  • ‹remove_floats› – odstraní hodnoty typu ‹float› a ‹double›,
 *  • ‹equals› – přijme index ‹i› a hodnotu libovolného typu ‹v›
 *    a vrátí ‹true› je-li na indexu ‹i› uložena hodnota stejného
 *    typu jako ‹v› a tyto hodnoty se rovnají.
 *
 * Metody ‹remove_integers› a ‹remove_floats› musí mít nejvýše
 * lineární časovou složitost, zatímco metoda ‹equals› konstantní. */

struct any_array{
    std::vector<std::any> data;
    void append(std::any a) { data.emplace_back(a);}
    void transform_int(std::function<int(int)> f){
        for (auto &a: data){
            if (a.type() == typeid(int))
                a = f(std::any_cast<int>(a));
        }
    }
    void remove_integers(){
        for (auto it = data.begin(); it != data.end(); ++it){
            if (it->type() == typeid(int))
                it = --data.erase(it);
        }
    }
    void remove_floats(){
        for (auto it = data.begin(); it != data.end(); ++it){
            if (it->type() == typeid(float) || it->type() == typeid(double))
                it = --data.erase(it);
        }

    }
    bool equals(int i, std::any t) const {return data[i].type() == t.type();}
    int size() const {return static_cast<int>(data.size());}

};

int main()
{
    any_array arr;
    const any_array &c_arr = arr;

    arr.append( 3 );
    assert( c_arr.equals( 0, 3 ) );
    assert( !arr.equals( 0, 3.0 ) );

    arr.transform_int( []( int x ) { return x - 2; } );

    arr.remove_floats();
    assert( arr.equals( 0, 1 ) );

    arr.append( 3.3 );
    assert( arr.equals( 1, 3.3 ) );
    arr.remove_integers();
    assert( arr.equals( 0, 3.3 ) );
    arr.remove_floats();
    assert( c_arr.size() == 0 );

    return 0;
}
