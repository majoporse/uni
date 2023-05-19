#include <cassert>
#include <set>
#include <memory>

/* This exercise will be another take on a set of numbers. This
 * time, we will add a capability to filter the numbers on output.
 * It will be possible to change the filter applied to a given set
 * at runtime. */

/* The «base class» for representing filters will contain a single
 * pure ‹virtual› method, ‹accept›. The method should be marked
 * ‹const›. */

class filter{
public:
    virtual bool accept(int)const = 0;
    virtual ~filter() = default;
};

class odd : public filter{
public:
int i = 1;
    bool accept(int i)const override{
        return i % 2 != 0;
    }
};

class all : public filter{
public:
int i = 0;
    bool accept(int)const override{
        return true;
    }
};

/* The ‹set› (which we will implement below) will «own» the filter
 * instance and hence will use a ‹unique_ptr› to hold it. */

using filter_ptr = std::unique_ptr< filter >;

/* The ‹set› should have standard methods: ‹add› and ‹has›, the
 * latter of which will respect the configured filter (i.e. items
 * rejected by the filter will always test negative on ‹has›). The
 * method ‹set_filter› should set the filter. If no filter is set,
 * all numbers should be accepted. Calling ‹set_filter› with a
 * ‹nullptr› argument should clear the filter. */

/* Additionally, ‹set› should have ‹begin› and ‹end› methods (both
 * ‹const›) which return very simple iterators that only provide
 * «dereference» to an ‹int› (value), pre-increment and inequality.
 * It is a good idea to keep «two» instances of
 * ‹std::set< int >::iterator› in attributes (in addition to a
 * pointer to the output filter): you will need to know, in the
 * pre-increment operator, that you ran out of items when skipping
 * numbers which the filter rejected. */
class set_iterator;

class set{
    std::set< int >data;

public:
    std::set<int>::iterator b;
    std::set<int>::iterator e;
    std::unique_ptr< filter > _filter;
    
    void add(int i){data.emplace(i); b = data.begin(); }
    bool has(int i){return data.contains(i) && _filter->accept(i);}
    set_iterator begin()const;
    set_iterator end()const;
    set() : b{data.begin()}, e{data.end()}, _filter{std::make_unique< all >()}{}
    void set_filter(std::unique_ptr< filter > f){ _filter = f ? std::move(f) : std::make_unique< all >();}
};

class set_iterator{
    const set *s;
    std::set< int >::iterator iter;
public:
    int operator*(){return *iter;}
    set_iterator &operator++(){
        do {++iter;} while(iter != s->e && !s->_filter->accept(*iter)); 
        return *this;
    }
    friend bool operator==(const set_iterator &, const set_iterator&) = default;
    set_iterator(const set *s, std::set< int >::iterator iter) : s{s}, iter{iter}{} 
};

set_iterator set::begin()const{return (_filter->accept(*b)) ? set_iterator(this, b) : ++set_iterator(this, b);}
set_iterator set::end()const{return {this, e};}

/* Finally, implement a filter that only accepts odd numbers. */


int main()
{
    set s;
    for ( int i : { 1, 2, 3, 4 } )
        s.add( i );

    assert( s.has( 1 ) );
    assert( s.has( 2 ) );

    int j = 0;
    for ( int i : s )
        assert( i == ++j );
    assert( j == 4 );

    s.set_filter( std::make_unique< odd >() );
    assert(  s.has( 1 ) );
    assert( !s.has( 2 ) );

    for ( int i : s )
        assert( i % 2 == 1 );

    j = 0;
    for ( int i : s )
        j ++, i ++;
    assert( j == 2 );

    s.add( 0 );
    assert( *s.begin() == 1 );

    return 0;
}
