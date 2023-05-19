#include <cassert>
#include <exception>
#include <utility>

/* † Napiste program, který bude řešit systémy lineárních rovnic
 * o dvou neznámých. Rozhraní bude lehce nekonvenční: přetěžte
 * operátory ‹+›, ‹*› a ‹==› a definujte globální konstanty ‹x› a
 * ‹y› vhodných typů tak, aby bylo možné rovnice zapisovat způsobem,
 * který vidíte níže v proceduře ‹main›. */

/* Uvědomte si, že návratový typ ‹==› nemusí být ‹bool› – naopak,
 * může se jednat o libovolný typ, včetně vlastních. Pro samotnou
 * implementaci funkce ‹solve› doporučujeme použít Cramerovo
 * pravidlo. */

/* Nemá-li zadaný systém řešení, funkce ‹solve› nechť skončí
 * výjimkou ‹no_solution› (tuto odvoďte od ‹std::exception›). */
struct no_solution : std::exception{};

struct equasion{
    int x = 0;
    int y = 0;
    int res = 0;

    friend equasion operator==( equasion a, const equasion &b){
        a.x -= b.x;
        a.y -= b.y;
        a.res -= b.res;
        return a;
    }

    friend equasion operator==(equasion a, int r){
        a.res += r;
        return a;
    }

    friend equasion operator+(equasion a, const equasion &b){
        a.x += b.x;
        a.y += b.y;
        a.res += b.res;
        return a;
    }
    friend equasion operator+(equasion a, int b){
        a.res -= b;
        return a;
    }
    
    friend equasion operator-(equasion a, const equasion &b){
        a.x -= b.x;
        a.y -= b.y;
        a.res -= b.res;
        return a;
    }

    friend equasion operator-(equasion a, int b){
        a.res += b;
        return a;
    }

    friend equasion operator*(int a, equasion b){
        b.x *= a;
        b.y *= a;
        return b;
    }
};

const equasion x = {1,0,0};
const equasion y = {0,1,0};

std::pair< double, double > solve(equasion a, equasion b){
    double D = a.x * b.y - (a.y * b.x);
    if (D == 0)
        throw no_solution();
    double D1 = a.res * b.y - (a.y * b.res);
    double D2 = a.x * b.res - (a.res * b.x);
    double x = D1 / D;
    double y = D2 / D;
    return {x, y};
}

int main()
{
    std::pair a( 1.0, 0.0 ), b( -1.0, 0.0 ), c( .6, -.2 );
    assert( solve(     x + y == 1,  x     - y ==  1 ) == a );
    assert( solve(     x + y == -1, x     - y == -1 ) == b );
    assert( solve(     x + y == x,  x     + y ==  1 ) == a );
    assert( solve( 2 * x + y == 1,  x - 2 * y ==  1 ) == c );
    assert( solve(     x + y - 1,   x     - y - 1   ) == a );

    try
    {
        solve( x + y == 1,  x + y == 2 );
        assert( 0 );
    }
    catch ( const std::exception &e ) {}

    try
    {
        solve( x + y == 1,  x + y == 2 );
        assert( 0 );
    }
    catch ( const no_solution &e ) {}

    return 0;
}
