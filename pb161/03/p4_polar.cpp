#define _USE_MATH_DEFINES
#include <cmath>
#include <cassert>


/* Vaším úkolem je implementovat typ ‹polar›, který realizuje
 * polární reprezentaci komplexního čísla. Protože tato podoba
 * zjednodušuje násobení a dělení, implementujeme v této úloze právě
 * tyto operace (sčítání jsme definovali v příkladu ‹e2_cartesian›).
 *
 * Krom násobení a dělení nechť je možné pro hodnoty typu polar
 * určit jejich rovnost operátory ‹==› a ‹!=›.  Rovnost
 * implementujte s ohledem na nepřesnost aritmetiky s plovoucí
 * desetinnou čárkou. V tomto příkladě můžete pro reálná čísla (typu
 * ‹double›) místo ‹x == y› použít ‹std::fabs( x - y ) < 1e-10›.
 *
 * Pozor! Argument komplexního čísla je «periodický»: buďto jej
 * normalizujte tak, aby ležel v intervalu ⟦[0, 2π)⟧, nebo
 * zajistěte, aby platilo ‹polar( 1, x ) == polar( 1, x + 2π )›. */

struct polar{
    double angle;
    double r;
    friend bool operator==(const polar &x, const polar &y){
        
        return  std::fabs(x.angle - y.angle) < 1e-10 &&
                std::fabs(x.r - y.r) < 1e-10;
    }

    friend bool operator!=(const polar &x, const polar &y){
        return !(x == y);
    }

    polar & operator*=(const polar &x){
        r *= x.r;
        if (r > 0)
            angle += x.angle;
        if (angle > M_PI)
            angle -= 2*M_PI;
        return *this;
    }

    polar operator/=(const polar &x){
        r /= x.r;
        if (r > 0)
            angle -= x.angle;
        if (angle < -M_PI)
            angle += 2*M_PI;
        return *this;
    }

    friend polar operator/(polar x, const polar &y){
        x /= y;
        return x;
    }

    friend polar operator*(polar x, const polar &y){
        x *= y;
        return x;
    }
};

polar make_polar( double r, double angle){
    while (std::fabs(angle) > M_PI)
        angle -= M_PI;
    polar res = {angle, r};
    return res;
}

int main()
{
    polar zero = make_polar( 0, 0 ),
          one = make_polar( 1, 0 ),
          i = make_polar( 1, 2 * std::atan( 1 ) ),
          minus_one = make_polar( 1, 4 * std::atan( 1 ) );
    
    polar a = make_polar(1, M_PI / 4.0);
    polar b = make_polar(1, M_PI / 2.0);
    polar test;
    a = a * b; assert( a != b);
    test = a; a = b; b = test; assert( a != b);
    a = a / b; assert( a != b);
    a = a / b; assert( a == b);

    assert( zero * one == zero );
    assert( zero * i == zero );
    assert( one * i == i );
    assert( i * i == minus_one );
    assert( i / i == one );
    assert( one / i == minus_one * i );
    assert( minus_one * minus_one == one );
    assert( minus_one / minus_one == one );

    return 0;
}
