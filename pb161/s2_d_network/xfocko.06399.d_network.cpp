/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [-] clearly describes solution to the problem
 **   * I don't really understand the overload of `connect()` that just calls
 ** `connect()` from the other side
 ** * [-] correctly decomposes the problem
 **   * Related to previous point
 **   * Loop-related functions, I don't understand why you have decided to put the
 ** DFS »inside« the nodes, it's very weird choice, it also makes the code feel
 ** fragmented, cause you have bit of implementation here, the other bit there;
 ** ideally move it to the network
 ** * [-] doesn't have code duplication
 **   * Overload that you don't need
 **   * `has_loops` vs `fix_loops`; Do you think that you could fix it? If not, feel
 **  free to reach out, it's not very straightforward nor easy
 ** * [x] uses correct abstractions, algorithms and data structures
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * n/a
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <cassert>
#include <set>
#include <memory>
#include <vector>
#include <queue>

/* Vaším úkolem bude tentokrát naprogramovat simulátor počítačové
 * sítě, s těmito třídami, které reprezentují propojitelné síťové
 * uzly:
 *
 *  • ‹endpoint› – koncový uzel, má jedno připojení k libovolnému
 *    jinému uzlu,
 *  • ‹bridge› – propojuje 2 nebo více dalších uzlů,
 *  • ‹router› – podobně jako bridge, ale každé připojení musí být
 *    v jiném segmentu.
 *
 * Dále bude existovat třída ‹network›, která reprezentuje síťový
 * segment jako celek. Každý uzel patří právě jednomu segmentu.
 * Je-li segment zničen, musí být zničeny (a odpojeny) i všechny
 * jeho uzly.
 *
 * Třída ‹network› bude mít tyto metody pro vytváření uzlů:
 *
 *  • ‹add_endpoint()› – vytvoří nový (zatím nepřipojený) koncový
 *    uzel, převezme jeho vlastnictví a vrátí vhodný ukazatel na
 *    něj,
 *  • ‹add_bridge( p )› – podobně pro ‹p›-portový bridge,
 *  • ‹add_router( i )› – podobně pro směrovač s ‹i› rozhraními.
 *
 * Jsou-li ‹m› a ‹n› libovolné typy uzlů, musí existovat vhodné
 * metody:
 *
 *  • ‹m->connect( n )› – propojí 2 uzly. Metoda je symetrická v tom
 *    smyslu, že ‹m->connect( n )› a ‹n->connect( m )› mají tentýž
 *    efekt. Metoda vrátí ‹true› v případě, že se propojení podařilo
 *    (zejména musí mít oba uzly volný port).
 *  • ‹m->disconnect( n )› – podobně, ale uzly rozpojí (vrací ‹true›
 *    v případě, že uzly byly skutečně propojené).
 *  • ‹m->reachable( n )› – ověří, zda může uzel ‹m› komunikovat
 *    s uzlem ‹n› (na libovolné vrstvě, tzn. včetně komunikace skrz
 *    routery; jedná se opět o symetrickou vlastnost; vrací hodnotu
 *    typu ‹bool›).
 *
 * Konečně třída ‹network› bude mít tyto metody pro kontrolu (a
 * případnou opravu) své vnitřní struktury:
 *
 *  • ‹has_loops()› – vrátí ‹true› existuje-li v síti cyklus,
 *  • ‹fix_loops()› – rozpojí uzly tak, aby byl výsledek acyklický,
 *    ale pro libovolné uzly, mezi kterými byla před opravou cesta,
 *    musí platit, že po opravě budou nadále vzájemně dosažitelné.
 *
 * Cykly, které prochází více sítěmi (a tedy prohází alespoň dvěma
 * směrovači), neuvažujeme. */

struct network;
struct router;

struct node{
    std::size_t max_nodes = 1;
    network *segment;
    std::set<node *> nodes;
    node(network *s): segment{s}{}

    bool full() const{ return max_nodes <= nodes.size();}
    bool connected(node *n) const{ return nodes.contains(n);}

    virtual bool can_connect(node *n){
        return n != this && !full() && segment == n->segment && !connected(n);
    }

    virtual bool connect(node* n) {
        if ( !can_connect(n) || !(n->can_connect(this)))
            return false;
        nodes.emplace(n);
        n->nodes.emplace(this);
        return true;
    }

/** I would ideally move this specific case into the `can_connect`. The `connect()`
 ** code, I believe, will be totally same with the exception of checking the
 ** segments. **/
    virtual bool connect(router *r);

    virtual bool disconnect(node *n){
        if (!connected(n) || !n->connected(this))
            return false;
        nodes.erase(n);
        n->nodes.erase(this);
        return true;
    };

/** :thumbsup: for the `const` **/
    bool reachable(const node *n) const{
        std::set<const node*> visited;
        std::deque<const node*> q;
        q.emplace_back(this);

        while (!q.empty()){

            const auto to = q.front();
            q.pop_front();

            if (to == n)
                return true;

            visited.insert(to);
/** `dev`? **/
            for (auto dev: to->nodes){
                if (!visited.contains(dev))
                    q.emplace_back(dev);
            }
        }
        return false;
    }

/** Does this »need to« be part of the `node` itself? **/
    bool dfs(node *parent, std::set<node*>&visited, bool ret, std::vector<std::tuple<node*, node*>> &to_remove){
        visited.insert(this);

        for (auto *child : nodes){
            if (child->segment != segment || child == parent)
                continue;
            if (visited.contains(child)){
                if (ret) return true;
                to_remove.emplace_back(this, child);
            }
            else if(child->dfs(this, visited, ret, to_remove))
                return true;
        }
        return false;
    }

    virtual ~node() = default;
};

struct endpoint : public node{
    endpoint(network* s): node(s){}
};

struct bridge : public node{
/** ```suggestion:-0+0
 **     bridge(int i, network* s): node(s), max_nodes(i) {}
 ** ```
 **
 ** Come on… **/
    bridge(int i, network* s): node(s){max_nodes = i;}
};

struct router : public node{
    router(int p, network* s): node(s){max_nodes = p;}

/** OK, so this is ideal… **/
    bool can_connect(node *n) override{
        for (node* node : nodes){
            if (node->segment == n->segment)
                return false;
        }
/** This is faster check then the for-loop above, ideally you would do an early
 ** return of `false` if this is not satisfied. **/
        return !full() && !n->full();
    }
};

/** Why do you need this then? **/
bool node::connect(router *r){return r->connect(this);}

struct network{
    std::vector<std::unique_ptr<node>> devices;

    endpoint* add_endpoint(){
        devices.emplace_back(std::make_unique<endpoint>(this));
/** Eh… You could probably return the `node` too… **/
        return dynamic_cast<endpoint*>(devices.back().get());
    }
    bridge* add_bridge( int p ){
        devices.emplace_back(std::make_unique<bridge>(p, this)); 
        return dynamic_cast<bridge*>(devices.back().get());
    }
    router* add_router( int i ){
        devices.emplace_back(std::make_unique<router>(i, this)); 
        return dynamic_cast<router*>(devices.back().get());
    }

    bool has_loops() const{
        std::set<node*> visited;
        std::vector<std::tuple<node*, node*>> to_remove;
        for (auto &n: devices){
            if (visited.contains(n.get())) 
                continue;
/** I don't really like the fact that you have this »here« and DFS »there«. Ideally
 ** keep it all in one place and that would be the `network` class IMO. Cause as a
 ** network node, I don't really care about the loops. **/
            if (n->dfs(nullptr, visited, true, to_remove))
                return true;
        }
        return false;
    }

/** Similarly here, though :thumbsup: for using just one algorithm for both of the
 ** tasks. **/
    void fix_loops(){
        std::set<node*> visited;
        std::vector<std::tuple<node*, node*>> to_remove;
        for (auto &n: devices){
            if (visited.contains(n.get()))
                continue;
            n->dfs(nullptr, visited, false, to_remove);
        }
        for(auto [from, to]: to_remove)
            from->disconnect(to);
    }
    ~network(){
        for (auto &d: devices){
            std::vector<node*>to_remove;
            for (auto &dn: d->nodes)
                if (dn->segment != this){
                    to_remove.emplace_back(dn); //cannot iterate through set and change its content
                }
            for (auto *dn: to_remove){
                d->disconnect(dn);
            }
        }
        devices.clear();
    }
};

int main()
{
    {
        network n;
    auto e1 = n.add_endpoint(),
         e2 = n.add_endpoint();
    auto b = n.add_bridge( 2 );
    auto r = n.add_router( 2 );

    assert( e1->connect( b ) );
    assert( b->connect( e2 ) );
    assert( e1->disconnect( b ) );
    assert( !e1->connect( e2 ) );
    assert( e2->reachable( b ) );
    assert( !n.has_loops() );
    n.fix_loops();
    assert( b->reachable( e2 ) );
    assert( r->connect( b ) );
    assert( !r->connect( e1 ) );
    }
    {
        network x;
        auto &t = *x.add_endpoint();
        auto &f = *x.add_endpoint(); 
        t.connect(&f);
        assert(f.reachable( &f ));
        assert(t.reachable( &f ));// from → 1, to → 1
        assert(f.reachable( &t ));// expect → 1, from → 1, to → 1
        assert(t.reachable( &t ));
        t.disconnect(&t);
        f.disconnect(&t);
        t.disconnect(&f);
        assert(!t.reachable(&f));
        assert(!f.reachable(&t));
        assert(t.reachable(&t));
        assert(!x.has_loops());
        x.fix_loops();
    }
    {
        network n;
        auto *b1 = n.add_bridge(3);
        auto *b2 = n.add_bridge(3);
        auto *b3 = n.add_bridge(3);
        b1->connect(b2);
        b2->connect(b3);
        b3->connect(b1);
        assert(n.has_loops());
        assert(b1->reachable(b2));
        assert(b1->reachable(b3));
        assert(b1->reachable(b1));
        assert(b2->reachable(b2));
        assert(b2->reachable(b3));
        assert(b2->reachable(b1));
        assert(b3->reachable(b2));
        assert(b3->reachable(b3));
        assert(b3->reachable(b1));
    n.fix_loops();
        n.has_loops();
        assert(b1->reachable(b2));
        assert(b1->reachable(b3));
        assert(b1->reachable(b1));
        assert(b2->reachable(b2));
        assert(b2->reachable(b3));
        assert(b2->reachable(b1));
        assert(b3->reachable(b2));
        assert(b3->reachable(b3));
        assert(b3->reachable(b1));
    }
    {
        network n;
        auto *b1 = n.add_bridge(3);
        auto *b2 = n.add_bridge(3);
        auto *b3 = n.add_bridge(3);
        auto *e1 = n.add_endpoint();
        auto *e2 = n.add_endpoint();
        auto *r1 = n.add_router(10);

        assert(e1->connect(b1));
        assert(!e1->connect(b1));
        assert(!e1->connect(b2));
        assert(b1->connect(b2));
        assert(b2->connect(b3));
        assert(b3->connect(b1));
        assert(e2->connect(b3));
        assert(r1->connect(b2));
        assert(e1->reachable(e2));
        assert(e2->reachable(e1));
        {
            network n2;
            auto *r2 = n2.add_router(10);
            auto *e3 = n2.add_endpoint();
            assert(!b1->connect(r2));
            assert(!e3->connect(b1));

            assert(r2->connect(e3));
            assert(r1->connect(r2));
            assert(!r1->connect(r2));

            assert(e1->reachable(e3));
            assert(e3->reachable(e1));

            assert(!n2.has_loops());
            n2.fix_loops();
            assert(n.has_loops());
            // assert(n.fix_loops());
            assert(r1->disconnect(r2));
            assert(!r1->disconnect(r2));
            assert(!e1->reachable(e3));
            assert(r1->connect(r2));
        }
        assert(e1->reachable(e2));
        assert(e2->reachable(e1));

    }
    {
        network s;

        assert(!s.has_loops());
        s.fix_loops();
        auto i = s.add_endpoint();
        assert(!s.has_loops());
        s.fix_loops();
        auto j = s.add_endpoint();
        i->connect(j);
        assert(!s.has_loops());
        s.fix_loops();
    }
    {
        network s;

        assert(!s.has_loops());
        s.fix_loops();
        auto i = s.add_bridge(5);
        assert(!s.has_loops());
        s.fix_loops();
        auto j = s.add_bridge(3);
        i->connect(j);
        assert(!s.has_loops());
        s.fix_loops();
    }
    {
        network s;
        assert(!s.has_loops());
        s.fix_loops();
        auto i = s.add_router(5);
        assert(!s.has_loops());
        s.fix_loops();
        auto j = s.add_bridge(3);
        i->connect(j);
        assert(!s.has_loops());
        s.fix_loops();
    }
    {
    network a;
    node *n1 = a.add_endpoint();//, ni.type → endpoint, ni.network → 1
    node *n4 = a.add_endpoint();//, ni.type → endpoint, ni.network → 1
    n1->connect(n4);// i → 1, j → 4
    assert(n1->reachable( n1 )); assert(n1->reachable( n1 )); //→ 1, from → 1, to → 1
    assert(n1->reachable( n1 )); //expect → 1, from → 1, to → 1
    assert(n1->reachable( n4 )); assert(n4->reachable( n1 )); //→ 1, from → 1, to → 4
    assert(n1->reachable( n4 )); //expect → 1, from → 1, to → 4
    assert(n4->reachable( n1 )); assert(n1->reachable( n4 )); //→ 1, from → 4, to → 1
    assert(n4->reachable( n1 )); //expect → 1, from → 4, to → 1
    assert(n4->reachable( n4 )); assert(n4->reachable( n4 )); //→ 1, from → 4, to → 4
    assert(n4->reachable( n4 )); //expect → 1, from → 4, to → 4
    assert(!a.has_loops( )); // → 0, n.has_loops() //→ 0, i → 0
    assert(!a.has_loops( )); // → 0, n.has_loops() //→ 0, i → 1
    assert(n1->disconnect( n4 )); //→ 1, was_connected → 1
    assert(n1->reachable( n1 )); assert(n1->reachable( n1 )); //→ 1, from → 1, to → 1
    assert(n1->reachable( n1 )); //expect → 1, from → 1, to → 1
    assert(!n1->reachable( n4 )); assert(!n4->reachable( n1 )); //→ 0, from → 1, to → 4
    assert(!n1->reachable( n4 )); //expect → 0, from //→ 1, to → 4
    assert(!n4->reachable( n1 )); assert(!n1->reachable( n4 )); //→ 0, from → 4, to → 1
    assert(!n4->reachable( n1 )); //expect → 0, from //→ 4, to → 1
    assert(n4->reachable( n4 )); assert(n4->reachable( n4 )); //→ 1, from → 4, to → 4
    assert(n4->reachable( n4 )); //expect → 1, from //→ 4, to → 4
    assert(!a.has_loops( ));// → 0, n.has_loops() → //0, i → 0
    assert(!a.has_loops( ));// → 0, n.has_loops() → //0, i → 1
    // input_number → 0x11
    // edge a → 1, b → 2
    // node i → 1, ni.capacity → 1, ni.type → endpoint
    // node i → 2, ni.capacity → 1, ni.type → endpoint
    node *a1 = a.add_endpoint();
    node *a2 = a.add_endpoint();
    assert(a1->connect(a2));
    assert(!a2->connect(a1));
    // g.at( j ).connect( g.at( i ) ) → 1, can_connect → 1, i → 1, j → 2
    // g.at( j ).connect( g.at( i ) ) → 0, can_connect → 0, i → 2, j → 1
    // edge a → 3, b → 6
    // node i → 3, ni.capacity → 3, ni.type → router
    // node i → 6, ni.capacity → 2, ni.type → router
    node *a3 = a.add_router(3);
    node *a6 = a.add_router(2);
    assert(a3->connect(a6));
//     eval/d_network.t.hpp:270: g.at( j ).connect( g.at( i ) ) == can_connect
// g.at( j ).connect( g.at( i ) ) = 0
//     can_connect                    = 1
//     i → 3, j → 6 
    }
    {
    network a;
    auto e1 = a.add_endpoint();
    auto e2 = a.add_endpoint();
    auto b1 = a.add_bridge(5);
    auto b2 = a.add_bridge(6);
    auto b3 = a.add_bridge(7);
    auto r1 = a.add_router(9);
    auto r2 = a.add_router(10);
    assert(b1->connect(b2));
    assert(b2->connect(b3));
    assert(b3->connect(b1));
    assert(r1->connect(e1));
    assert(r2->connect(e2));
    network b;
    auto e11 = b.add_endpoint();
    auto b11 = b.add_bridge(5);
    auto b12 = b.add_bridge(6);
    auto b13 = b.add_bridge(7);
    auto r11 = b.add_router(9);
    assert(b11->connect(b12));
    assert(b12->connect(b13));
    assert(b13->connect(b11));
    assert(r11->connect(b11));
    assert(e11->connect(b12));
    network c;
    auto r21 = c.add_router(9);
    auto e21 = c.add_endpoint();
    assert(e21->connect(r21));
    assert(r21->connect(r11));
    assert(r11->connect(r1));
    assert(e1->reachable(e21));
    assert(a.has_loops());
    a.fix_loops();
    assert(!a.has_loops());
    assert(b.has_loops());
    b.fix_loops();
    assert(!b.has_loops());
    assert(e1->reachable(e21));
    assert(e1->reachable(e11));
    assert(e21->reachable(e11));
    assert(!r1->connect(r11));
    assert(!r1->connect(e11));
    assert(!r1->connect(b11));
    assert(!e1->connect(e1));
    assert(!r2->connect(r11));
    assert(!e11->connect(b13));
    assert(e1->reachable(e21));
    assert(!b1->reachable(e21));
    assert(!b1->reachable(e1));
    assert(!b1->reachable(r1));
    assert(r21->connect(r1));
    assert(!b1->reachable(r1));
    assert(!a.has_loops());
    assert(!b.has_loops());
    assert(!c.has_loops());
    }

    return 0;
}
