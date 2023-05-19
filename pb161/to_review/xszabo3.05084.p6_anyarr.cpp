#include <cassert>
#include <any>
#include <vector>
#include <cstddef>

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
    std::vector<std::any> myarray;
    void append(auto a){
        myarray.push_back(std::make_any<decltype(a)>(a));
    }
    size_t size()const{
        return myarray.size();
    }
    void transform_int(auto f){
        for(auto& idx : myarray){
            if (auto* ptr = std::any_cast<int>(&idx)) {
                idx = f(*ptr);
            }
        }
    }
    bool equals(int i, auto v) const{
        if (auto* ptr = std::any_cast<decltype(v)>(&myarray[i])) {
            return *ptr == v;
        }
        return false;
    }
    void remove_integers(){
        int top = 0;
        int current = 0;
        while(current != static_cast<int>(myarray.size())){
            if (!std::any_cast<int>(&myarray[current])) {
                myarray[top] = myarray[current];
                ++top;
            }
            ++current;
        }
        myarray.resize(top);
    }
    void remove_floats(){
        int top = 0;
        int current = 0;
        while(current != static_cast<int>( myarray.size() )){
            if (!std::any_cast<float>(&myarray[current]) && !std::any_cast<double>(&myarray[current])) {
                myarray[top] = myarray[current];
                ++top;
            }
            ++current;
        }
        myarray.resize(top);
    }

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

