#include <vector>
#include <cassert>
#include <map>
#include <list>

/* Napište podprogram ‹reorder( s, weight )›, který pro zadanou
 * posloupnost ‹s› a funkci ‹weight› na místě přeuspořádá ‹s› tak,
 * že pro ⟦u < w⟧ budou prvky s váhou ⟦u⟧ předcházet prvkům s váhou
 * ⟦w⟧. Zároveň pro prvky se stejnou váhou platí, že se objeví ve
 * stejném pořadí, v jakém byly v původní posloupnosti ‹s›.
 *
 * Podprogram musí pracovat v čase nejvýše ⟦O(k⋅n)⟧ kde ⟦k⟧ je počet
 * různých vah, které se objeví na vstupu, a ⟦n⟧ je délka
 * posloupnosti ‹s›. Je také povoleno využít lineární množství
 * dodatečné paměti. */


// find first smaller weight index or equal index of last_indexes
template<typename SIter, typename IIter, typename W, typename F>
bool equal_bin_search(const std::vector<SIter>& last_indexes, const W& weight, IIter& pos, F func) {
    auto left = last_indexes.cbegin(),
         right = --last_indexes.cend();

    while (std::distance(left, right) >= 0) {
        auto mid = std::next(left, std::distance(left, right)/2);
        const W& cmp_weight = func(*(*mid));
        if (weight == cmp_weight) {
            pos = mid;
            return true;
        } else if (weight < cmp_weight) {
            pos = mid;
            right = std::prev(mid);
        } else {
            left = std::next(mid);
        }
    }
    return false;
}

template<typename T, typename F>
void reorder(std::vector<T>& s, F func) {
    if (s.empty()) return;

    std::list<T> slist(std::make_move_iterator(s.begin()),
                       std::make_move_iterator(s.end()));

    std::vector<decltype(slist.begin())> last_indexes;
    for(auto iter = slist.begin(); iter != slist.end();) {
        const auto& weight = func(*iter);
        if (last_indexes.empty() || weight > func(*last_indexes.back())) {
            last_indexes.push_back(iter);
            ++iter;
            continue;
        }

        auto backup_iter = iter;
        ++iter;

        auto indexes_iter = --last_indexes.cend();
        bool is_equal = equal_bin_search(last_indexes, weight, indexes_iter, func);
        if (!is_equal) { //patří před tuto váhu
            auto insert_pos = slist.begin();
            if (indexes_iter != last_indexes.cbegin()) {
                insert_pos = std::next(*std::prev(indexes_iter));
            }

            const auto new_iter = slist.insert(insert_pos, std::move(*backup_iter));
            slist.erase(backup_iter);
            last_indexes.insert(indexes_iter, new_iter);
        } else if (is_equal) { // patří na konec této váhy
            if (indexes_iter != --last_indexes.end()) {
                slist.insert(std::next(*indexes_iter), std::move(*backup_iter));
                slist.erase(backup_iter);
            }
            last_indexes[std::distance(last_indexes.cbegin(), indexes_iter)] = std::next(*indexes_iter);
        }
    }

    std::vector<T> reordered_s(std::make_move_iterator(slist.begin()),
                              std::make_move_iterator(slist.end()));
    s = std::move(reordered_s);
}


int main() {
    std::vector a{ 1, 3, 4, 2 };

    reorder( a, []( int x ) { return x / 2; } );
    assert(( a == std::vector{ 1, 3, 2, 4 } ));
    reorder( a, []( int x ) { return -x / 2; } );
    assert(( a == std::vector{ 4, 3, 2, 1 } ));
    
    std::vector b{ 1, 3, 5, 4, 2 };

    reorder( b, []( int x ) { return x % 4; } );
    assert(( b == std::vector{ 4, 1, 5, 2, 3 } ));
    
    struct token
    {
        int value;

        token( int v ) : value( v ) {}

        token( const token & ) = delete;
        token( token && ) = default;

        token &operator=( const token & ) = delete;
        token &operator=( token && ) = default;

        bool operator==( const token & ) const = default;
    };

    struct weight
    {
        int value;
        weight( int v ) : value( v ) {}

        weight( const weight & ) = delete;
        weight( weight && ) = delete;

        weight &operator=( const weight & ) = delete;
        weight &operator=( weight && ) = delete;

        bool operator==( const weight &o ) const = default;
        auto operator<=>( const weight &o ) const = default;
    };

    std::vector< token > x, y;
    int ops = 0;
    int count = 1024 * 512;

    for ( int i = 0; i < count; ++i )
    {
        x.emplace_back( i );
        y.emplace_back( i );
    }

    auto one_way = [&]( const auto &t )
    {
        ++ops;
        return weight( -t.value / count );
    };

    auto two_way = [&]( const auto &t )
    {
        ++ops;
        return weight( -t.value / ( count / 2 ) );
    };

    reorder( x, one_way );
    assert( ops <= 4 * count );
    assert( x == y );
    ops = 0;

    reorder( x, two_way );
    assert( ops <= 8 * count );
    assert( x != y );
    ops = 0;

    assert( x.front().value == count / 2 );
    assert( x.back().value == count / 2 - 1 );
    assert( x[ count / 2 ].value == 0 );
    assert( x[ count / 2 - 1 ].value == count - 1 );
    
    return 0;
}
