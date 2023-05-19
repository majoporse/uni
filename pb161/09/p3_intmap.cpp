#include <cassert>
#include <vector>
#include <variant>
#include <tuple>

/* Navrhněte typ, který bude reprezentovat operaci nad polem celých
 * čísel. Vyhodnocení sestavené operace se provede metodou:
 *
 *  • ‹eval( v )› – aplikuje operaci na vektor celých čísel ‹v›
 *    (přepsáním vstupního vektoru),
 *
 * Celkový efekt operace bude lze postupně zadat připojováním
 * elementárních operací „na konec“ stávající operace ‹op› (‹n›
 * představuje celé číslo, ‹v› představuje vektor celých čísel):
 *
 *  • ‹op.add( n )› – přičte ke všem prvkům vstupu hodnotu ‹n› (tzn.
 *    ‹out[ i ] = in[ i ] + n›),
 *  • ‹op.add( v )› – cyklicky přičte hodnoty z ‹v› ke vstupnímu
 *    vektoru (tzn. ‹out[ i ] = in[ i ] + v[ i ]›; padne-li ‹i› mimo
 *    rozsah vektoru ‹v›, pokračuje se opět prvním prvkem ‹v›,
 *    atd.),
 *  • ‹op.rotate( n )› – přesune prvek na indexu ‹i› na index ‹i + n›
 *    (tzn. ‹out[ i + n ] = in[ i ]›; je-li ‹i + n› mimo meze,
 *    použije se vhodný index v mezích tak, aby operace realizovala
 *    rotaci),
 *  • ‹op.pop()› – zapomene posledně vloženou elementární operaci.
 */
struct add_const{
    int n;
};
struct add_vec{
    std::vector<int> v;
    int pos;
};
struct srotate{
    int n;
};
struct update{
    std::vector<int> &vec;
    void operator()(add_const a){
        for (auto &i : vec)
            i += a.n;
    }
    void operator()(add_vec a){
        for (std::size_t i = 0; i < vec.size(); ++i, a.pos = (a.pos + 1) % a.v.size()){
            vec[i] += a.v[a.pos];
        }
    }
    void operator()(srotate a){
        std::vector<int> res(vec.size(), 0);
        for (std::size_t i = 0; i < res.size(); ++i)
            res[(i + a.n) % res.size()] = vec[i];
        vec = std::move(res);
    }
};

struct intmap{
    using operation = std::variant<add_const, add_vec, srotate>;
    std::vector<operation> operations;
    void eval(std::vector<int> &in){
        for (auto &op: operations)
            std::visit(update{in}, op);
    }
    void add( int n ){operations.emplace_back(add_const{n});}
    void add( std::vector<int> vec ){operations.emplace_back(add_vec{vec, 0});}
    void rotate(int n) {operations.emplace_back(srotate{n});}
    void pop() {operations.pop_back();}

};

int main()
{
    intmap op{};
    std::vector< int > numbers( 6, 0 );

    op.add( { 1, 2 } );
    op.rotate( 1 );
    op.add( { 1, 2 } );
    op.eval( numbers );

    assert(( numbers == std::vector{ 3, 3, 3, 3, 3, 3 } ));

    op.pop();
    op.add( 3 );
    op.eval( numbers );

    assert(( numbers == std::vector{ 8, 7, 8, 7, 8, 7 } ));

    op.add( { 10, 20, 15, 4, 7, 6, 9, 33, 14 } );
    op.rotate( 4 );
    op.eval( numbers );

    assert(( numbers == std::vector{ 27, 16, 19, 18, 22, 32 } ));
    return 0;
}
