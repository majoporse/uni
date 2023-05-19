#include <variant>
#include <memory>
#include <cassert>

/* Máte zadané následující typy, které reprezentují jednoduchý
 * aritmetický výraz. */

struct constant;
struct add;
struct subtract;
struct multiply;
struct divide;

using expr = std::variant< constant, add, subtract, multiply, divide >;
using expr_ptr = std::unique_ptr< expr >;

struct constant
{
    constant( int v ) : value( v ) {}
    int value = 0;
};

struct binary
{
    expr_ptr left, right;
    binary( expr a, expr b );
};

struct add      : binary { using binary::binary; };
struct subtract : binary { using binary::binary; };
struct multiply : binary { using binary::binary; };
struct divide   : binary { using binary::binary; };

binary::binary( expr a, expr b )
    : left{ std::make_unique< expr >( std::move( a ) ) },
      right{ std::make_unique< expr >( std::move( b ) ) }
{}
struct evaluator{
    int operator()(add &a) {return std::visit(evaluator{}, *(a.left)) + std::visit(evaluator{}, *(a.right)); }
    int operator()(subtract &s) {return std::visit(evaluator{}, *(s.left)) - std::visit(evaluator{}, *(s.right)); }
    int operator()(multiply &m){ return std::visit(evaluator{}, *(m.left)) * std::visit(evaluator{}, *(m.right)); }
    int operator()(divide &d) { return std::visit(evaluator{}, *(d.left)) / std::visit(evaluator{}, *(d.right)); }
    int operator()(constant &c) { return c.value; }
};

int eval(expr &e){
    return std::visit(evaluator{}, e);
}
/* Vaším úkolem je naprogramovat funkci ‹eval›, která takto zadaný
 * výraz vyhodnotí na celé číslo. */

int main()
{
    expr e1 = add( multiply( 1, 2 ), 1 );
    expr e2 = add( subtract( 3, multiply( 1, 2 ) ), 1 );

    assert( eval( e1 ) == 3 );
    assert( eval( e2 ) == 2 );

    return 0;
}
