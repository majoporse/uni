#include <cassert>
#include <tuple>
#include <vector>
#include <functional>

/* Implementujte typ ‹program›, který bude reprezentovat výpočet nad
 * stavem určeným dvojicí celých čísel. Na konec stávajícího výpočtu
 * je možné přidat další krok metodou ‹append›, která přijme
 * libovolnou funkci, které lze předat 2 celá čísla. */

struct program{
    std::vector<std::function<void(int&, int&)>> func;
    void add(auto f){
        func.push_back(f);
    }
    std::tuple<int, int> eval(int a, int b){
        for(const auto& f : func){
            f(a, b);
        }
        return {a, b};
    }
};

int main()
{
    program p;

    p.add( []( int &a, int &  ) { a += 3; } );
    p.add( []( int &a, int &b ) { b  = a; } );
    p.add( []( int &a, int &b ) { a *= b; } );

    assert(( p.eval( 0, 0 ) == std::tuple{  9, 3 } ));
    assert(( p.eval( 1, 0 ) == std::tuple{ 16, 4 } ));
    assert(( p.eval( 1, 1 ) == std::tuple{ 16, 4 } ));

    return 0;
}

