#include <memory>
#include <cassert>
#include <vector>

/* An s-expression is a tree in which each node has an arbitrary
 * number of children. To make things a little more interesting, our
 * s-expression nodes will own their children. */

/* The base class will be called ‹node› (again) and it will have
 * single (virtual) method: ‹value›, with no arguments and an ‹int›
 * return value. */

class node {
public:
    virtual int value() = 0;
    virtual ~node() = default;
};

using node_ptr = std::unique_ptr< node >;

/* There will be two types of internal nodes: ‹sum› and ‹product›,
 * and in this case, they will compute the sum or the product of all
 * their children, regardless of their number. A sum with no
 * children should evaluate to 0 and a product with no children
 * should evaluate to 1.
 *
 * Both will have an additional method: ‹add_child›, which accepts
 * (by value) a single ‹node_ptr› and both should have default
 * constructors. It is okay to add an intermediate class to the
 * hierarchy. */

class operation : public node {
protected:
    std::vector<node_ptr> children;
public:
    void add_child(node_ptr &&p) { children.push_back(std::move(p)); }
};

class sum : public operation {
public:
    int value() override {
        int result = 0;
        for (auto& child : children) { result += child->value(); }
        return result;
    }
};

class product : public operation {
public:
    int value() override {
        int result = 1;
        for (auto& child : children) { result *= child->value(); }
        return result;
    }
};

/* Leaf nodes carry an integer constant, given to them via a
 * constructor. */

class constant : public node {
    int n;
public:
    constant( int n ) : n{n} {}

    int value() override { return n; }
};

int main()
{
    auto mk_const = []( int n )
    {
        return std::make_unique< constant >( n );
    };

    auto mk_sum = []{ return std::make_unique< sum >(); };
    auto mk_prod = []{ return std::make_unique< product >(); };

    auto s = mk_sum();
    auto p = mk_prod();

    s->add_child( mk_const( 2 ) );
    s->add_child( mk_const( 3 ) );

    assert( s->value() == 5 );

    p->add_child( mk_const( 2 ) );
    p->add_child( std::move( s ) );

    assert( p->value() == 10 );

    p->add_child( mk_const( 7 ) );

    assert( p->value() == 70 );

    s = mk_sum();
    assert( s->value() == 0 );

    s->add_child( std::move( p ) );
    assert( s->value() == 70 );

    s->add_child( mk_const( 30 ) );
    assert( s->value() == 100 );

    return 0;
}
