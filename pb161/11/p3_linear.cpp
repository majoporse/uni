#include <cassert>
#include <cmath>
#include <utility>
#include <string>
#include <string_view>
#include <cctype>
#include <vector>
#include <set>

/* Ve cvičení ‹07/p6_linear› jsme napsali jednoduchý program, který
 * řeší systémy lineárních rovnic o dvou neznámých. Tento program
 * nyní rozšíříme o načítání vstupu z řetězce. */

/* Naprogramujte čistou funkci ‹solve›, která má jediný parametr
 * (řetězec předaný jako hodnota typu ‹std::string_view›). Vstup
 * obsahuje právě dvě rovnice, na každém řádku jedna, se dvěma
 * jednopísmennými proměnnými a celočíselnými koeficienty. Každý
 * člen je oddělen od operátorů (‹+› a ‹-›) a znaku rovnosti
 * mezerami, jednotlivý člen (koeficient včetně znaménka a případná
 * proměnná) naopak mezery neobsahuje. Není-li vstup v očekávaném
 * formátu, situaci řešte jak uznáte za vhodné (můžete např. ukončit
 * funkci výjimkou ‹no_parse›).
 *
 * Výsledkem bude dvojice čísel typu ‹double›. Pořadí výsledku nechť
 * je abecední (např. dvojice ‹x›, ‹y›). Jinak se funkce ‹solve›
 * chová stejně, jak je popsáno v zmiňovaném příkladu
 * ‹07/p6_linear›. */

struct no_solution : std::exception {};
struct no_parse    : std::exception {};

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

int stack_to_int( std::vector<int> &stack ){
    int res = 0;
    for (int i = stack.size() - 1; i >= 0; --i)
        res = res * 10 + stack[i];
    return res;
}
std::pair< double, double > oldsolve(equasion a, equasion b){
    double D = a.x * b.y - (a.y * b.x);
    if (D == 0)
        throw no_solution();
    double D1 = -a.res * b.y - (a.y * -b.res);
    double D2 = a.x * -b.res - (-a.res * b.x);
    double x = D1 / D;
    double y = D2 / D;
    return {x, y};
}

std::pair< double, double > solve( std::string_view eq ){
    std::vector<equasion> eqs = {{}, {}, {}, {}};
    bool sign = true;
    int xc = 0, yc = 0;
    std::vector<int> stack;
    int ptr = 0;
    std::set<char> expect = {'x', 'y', 'n'};
    for (std::size_t pos = 0; (pos = eq.find_first_not_of(' ', pos )) != std::string::npos; pos++){
        switch(eq[pos]){
            case 'x': if (!expect.contains('x')) throw no_parse();
                    xc += (sign ? 1 : -1) * (stack.empty() ? 1 : stack_to_int(stack));
                    stack.clear(); 
                    sign = true;
                    expect = {'+', '-', '='};
                    break;

            case 'y': if (!expect.contains('y')) throw no_parse();
                    yc += (sign ? 1 : -1) * (stack.empty() ? 1 : stack_to_int(stack));
                    stack.clear();
                    sign = true;
                    expect = {'+', '-', '='};
                    break;

            case '+': if (!expect.contains('+')) throw no_parse();
                    sign = true; expect = {'x', 'y', 'n'}; break;

            case '-': if (!expect.contains('-')) throw no_parse();
                    sign = false; expect = {'x', 'y', 'n'}; break;

            case '=': if (!expect.contains('=')) throw no_parse();
                    if (eq[pos] == '=') pos++;
                    eqs[ptr++] = {xc, yc, (sign ? 1 : -1) * stack_to_int(stack)};
                     stack.clear();
                     sign = true;
                     expect = {'x', 'y', 'n', '-'};
                     xc = 0, yc = 0; break;

            case '\n':
                    eqs[ptr++] = {xc, yc, (sign ? 1 : -1) * stack_to_int(stack)};
                    stack.clear();
                    sign = true;
                    expect = {'x', 'y', 'n'};
                    xc = 0, yc = 0; break;
            default:
                if (!expect.contains('n')) throw no_parse();
                if (isdigit(eq[pos]))
                    stack.push_back(eq[pos] - '0');
                expect = {'x', 'y', '=', 'n'};
        }
    }
    eqs[0] = eqs[0] == eqs[1];
    eqs[2] = eqs[2] == eqs[3];
    return oldsolve(eqs[0], eqs[2]);
}

int main()
{
    std::pair a( 1.0, 0.0 ), b( -1.0, 0.0 ), c( .6, -.2 );

    auto check = []( auto s, auto val )
    {
        auto [ u, v ] = solve( s );
        auto [ x, y ] = val;
        return std::abs( u - x ) < 1e-6 &&
               std::abs( v - y ) < 1e-6;
    };

    assert( check( " x + y     =  1\n x -  y     =  1\n", a ) );
    assert( check( " x + y     = -1\n x -  y     = -1\n", b ) );
    assert( check( " x + y     =  x\n x +  y     =  1\n", a ) );
    assert( check( "2x + y     =  1\n x - 2y     =  1\n", c ) );
    assert( check( " x + y - 1 =  0\n x -  y - 1 =  0\n", a ) );
    assert( check( "10x + 10y  = 10\n x -  y     =  1\n", a ) );

    try
    {
        solve( "x + y == 1\nx + y == 2\n" );
        assert( false );
    }
    catch ( const no_solution & ) {}

    return 0;
}
