#include <memory>
#include <string>
#include <map>
#include <cassert>

/* TODO: use single-character variables */

/* Consider an abstract syntax tree of a very simple imperative
 * programming language with structured control flow. Let there be 3
 * types of statements:
 *
 *  1. a variable increment, ‹a ++›,
 *  2. a while loop of the form ‹while (a != b) stmt›, and finally
 *  3. a block, which is a sequence of statements. */

class statement;
using stmt_ptr = std::unique_ptr< statement >;

/* We will represent variables as strings. Provide an ‹eval› method
 * which takes variable assignment as an argument and returns the
 * same as a result. Variables used in the program but not given in
 * the input start as 0. The variable assignment (i.e. the «state»
 * of the program) is represented as an ‹std::map› from strings to
 * integers. */

using state = std::map< std::string, int >;

/* The constructors should be as follows:
 *
 *  • ‹stmt_inc› takes the name of the variable to be incremented,
 *  • ‹stmt_while› takes 2 variable names and an ‹stmt_ptr› for the
 *     body, and
 *  • ‹stmt_block› is default-constructed as a noop, but provides an
 *    ‹append› method to insert a ‹stmt_ptr› at the end. */

class stmt_inc;
class stmt_while;
class stmt_block;

int main()
{
    auto mk_inc = []( auto var )
    {
        return std::make_unique< stmt_inc >( var );
    };

    auto mk_while = []( auto v1, auto v2, auto &&body )
    {
        return std::make_unique< stmt_while >( v1, v2,
                                               std::move( body ) );
    };

    auto body = std::make_unique< stmt_block >();
    body->append( mk_inc( "a" ) );
    body->append( mk_inc( "b" ) );

    auto loop = mk_while( "a", "c", body );
    std::map< std::string, int > vars = { { "a", 0 },
                                          { "b", 3 },
                                          { "c", 7 } };

    vars = mk_inc( "a" )->eval( vars );
    assert( vars[ "a" ] == 1 );
    assert( vars[ "b" ] == 3 );
    assert( vars[ "c" ] == 7 );

    vars = loop->eval( vars );
    assert( vars[ "a" ] == 7 );
    assert( vars[ "b" ] == 9 );
    assert( vars[ "c" ] == 7 );

    body = std::make_unique< stmt_block >();
    body->append( std::move( loop ) );
    body->append( mk_inc( "b" ) );

    loop = mk_while( "b", "d", body );
    vars[ "c" ] = 11;
    vars[ "d" ] = 17;

    vars = loop->eval( vars );
    assert( vars[ "a" ] == 11 );
    assert( vars[ "b" ] == 17 );
    assert( vars[ "c" ] == 11 );
    assert( vars[ "d" ] == 17 );

    return 0;
}
