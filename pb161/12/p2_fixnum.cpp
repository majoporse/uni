#include <cassert>
#include <sstream>
#include <charconv>
#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <iomanip>

/* V tomto příkladu se vrátíme k typu ‹fixnum› z předchozí kapitoly.
 * Jedná se o typ, který reprezentuje čísla s pevnou desetinnou
 * čárkou, konkrétně tvaru ‹123456.78›, se 6 desítkovými číslicemi
 * před a dvěma za desetinnou čárkou, a s těmito operacemi:
 *
 *  • sčítání, odečítání a násobení (operátory ‹+›, ‹-› a ‹*›),
 *  • sestrojení z celého čísla (implicitně nula),
 *  • přiřazení kopií,
 *  • srovnání dvou hodnot operátory ‹==› a ‹!=›,
 *  • čtení a zápis čísel z vstupně-výstupních proudů.
 *
 * Všechny aritmetické operace nechť zaokrouhlují směrem k nule na
 * nejbližší reprezentovatelné číslo. */
struct bad_format{};

struct fixnum{
    int value = 0;
    fixnum(int i) : value(i * 100) {}
    fixnum() = default;
    fixnum(std::string s){

        double num1{};
        auto [ptr1 , result1] = std::from_chars(s.data(), s.data() + s.size(), num1);

        int num2{};
        auto [ptr2, result2] = std::from_chars(s.data(), s.data() + s.size(), num2); 
    
        if (ptr2 != s.data() + s.size() && ptr1 != s.data() + s.size()){
            throw bad_format();
        }
        value = static_cast<int>(std::floor(std::stod(s) * 100));
    }
    fixnum operator+(fixnum other) const {
        auto res = fixnum();
        res.value = (value + other.value);
        return res;
    }
    fixnum operator-(fixnum other) const {
        auto res = fixnum();
        res.value = (value - other.value);
        return res;
    }
    fixnum operator*(fixnum other) const {
        auto res = fixnum();
        res.value = (value * other.value) / 100;
        return res;
    }
    friend bool operator==(const fixnum &a, const fixnum &b) = default;
    friend bool operator!=(const fixnum &a, const fixnum &b) = default;

    friend std::ostream &operator<<(std::ostream &os, const fixnum &a) {
        os << std::setw(1);
        os << (a.value / 100) << '.' << std::setw(2) << std::setfill('0') << std::right << (a.value % 100);
        os << std::setfill(' ');
        return os;
    }
    friend std::istream &operator>>(std::istream &is, fixnum &a) {
        
        double y;
        is >> std::setprecision(2) >> y;
        y *= 100;
        if (std::isdigit(is.peek()))
            is.setstate(std::ios::failbit);
    
        a = fixnum();
        a.value = std::round(y);

        return is;
    }
};

int main()
{
    std::stringstream s( "10 1" );
    fixnum x, y;
    s >> x >> y;

    assert( fixnum( 10 ) == x );
    assert( fixnum( 1 )  == y );

    s.clear();
    s.str( "0.5 5.5 0.01 0.05 0.27" );

    fixnum a( 10 ), b, c, d, e, f;
    s >> b >> c >> d >> e >> f;

    s.clear();
    s.str( "" );
    s << a << " " << std::setw( 2 ) << 0;
    auto aaa = s.str();
    assert( aaa == "10.00  0" );

    assert( a + b + b == fixnum( 11 ) );
    assert( c + b == fixnum( 6 ) );
    assert( c + c - fixnum( 1 ) == a );
    assert( a * a * d == fixnum( 1 ) );
    assert( fixnum( 5 ) * d == e );
    assert( a * b == fixnum( 5 ) );
    assert( d * d == fixnum( 0 ) );
    assert( a * a == fixnum( 100 ) );
    assert( e * fixnum( 100 ) == fixnum( 5 ) );
    assert( e * c == f );
    assert( fixnum( -1 ) * e * c == fixnum( -1 ) * f );

    s.clear();
    s.str( "123456.78 123456.00 0.78" );

    s >> b >> c >> e;

    assert( b - c == e );
    x = fixnum( 0 );

    for ( int i = 0; i < 1000; ++i )
        for ( fixnum j : { d, d, fixnum( -2 ) * d } )
            for ( int k = 0; k < 1000000; ++k )
                x = x + j;

    for ( int i = 0; i < 1000; ++i )
    {
        assert( x * fixnum( i ) == fixnum( 0 ) );
        assert( !( x * fixnum( i ) != fixnum( 0 ) ) );
        assert( x * fixnum( i ) != d );
        assert( !( x * fixnum( i ) == d ) );
    }

    s.clear();
    s.str( "123,x 1.1y 1.." );

    std::string sx, sy, se;
    s >> x >> sx >> y >> sy >> e >> se;
    assert( x == 123 );
    assert( sx == ",x" );
    assert( y == fixnum( 110 ) * d );
    assert( sy == "y" );
    assert( e == 1 );
    assert( se == "." );

    s.clear();
    s.str( "1.001" );
    s >> x;
    assert( !s );

    return 0;
}
