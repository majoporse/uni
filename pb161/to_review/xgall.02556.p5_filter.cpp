#include <cassert>
#include <set>
#include <memory>
#include <iostream>

/* This exercise will be another take on a set of numbers. This
 * time, we will add a capability to filter the numbers on output.
 * It will be possible to change the filter applied to a given set
 * at runtime. */

/* The «base class» for representing filters will contain a single
 * pure ‹virtual› method, ‹accept›. The method should be marked
 * ‹const›. */

class filter{
public:
    virtual bool accept(int n) const = 0;

    virtual ~filter() = default;
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

class set;

class set_iterator{
    std::set<int>::iterator _holding;
    std::set<int>::iterator _end;
    std::set<int> &_domain;
    filter* _judge;
    

public:
    set_iterator(std::set<int>::iterator given, std::set<int> &domain, filter* judge) : _holding{given}, _domain{domain}, _judge{judge} {
        _end = _domain.end();
    }

    inline bool operator!=(set_iterator &rhs){
        return this->_holding != rhs._holding;
    }

    set_iterator &operator++(){
        do {
            _holding++;
        } while (_holding != _end && _judge && !(_judge->accept(*_holding))); // (not reached end) and (have judge) and (judge rejects)
        return *this;
    }

    inline int operator*(){
        return *_holding;
    }
};

class set{
    filter_ptr filtering = nullptr;
    std::set<int> content;
    friend set_iterator;

public:
    bool has(int target) const {
        if (!content.contains(target)) return false;
        if (filtering.get() && !filtering->accept(target))
            return false;
        return true;
    }

    void add(int n) {
        content.insert(n);
    }

    set_iterator begin(){
        auto candidate = set_iterator{content.begin(), content, filtering.get()};
        if (!has(*candidate)) return ++candidate;



        return candidate;
    }

    set_iterator end() { return set_iterator{content.end(), content, filtering.get()};}

    void set_filter(filter_ptr given){
        filtering.reset();
        filtering = std::move(given);
    }
};

/* Finally, implement a filter that only accepts odd numbers. */

class odd : public filter{
public:
    bool accept(int n) const override{
        return n % 2 == 1;
    }
};

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
