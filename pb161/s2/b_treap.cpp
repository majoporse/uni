#include <memory>
#include <cassert>
#include <vector>
#include <cstdlib>

/* Datová struktura «treap» kombinuje binární vyhledávací strom a
 * binární haldu. Samozřejmě jedna struktura nemůže splnit obě
 * vlastnosti na stejném klíči:
 *
 *  • vyhledávací strom požaduje, aby hodnoty v levém podstromě byly
 *    menší (a hodnoty v pravém větší) než hodnota v kořenu,
 *  • maximová halda vyžaduje, aby hodnoty v obou podstromech byly
 *    menší, než hodnota v kořenu.
 *
 * Proto bude «treap» uchovávat dvojici hodnot: «klíč» a «prioritu».
 * Strom bude uspořádán tak, aby tvořil vzhledem ke klíči
 * vyhledávací strom a binární haldu vzhledem k prioritě.
 *
 * Smyslem haldové části struktury je udržet strom přibližně
 * vyvážený. Algoritmus vložení prvku pracuje takto:
 *
 *  1. na základě klíče vložíme uzel na vhodné místo tak, aby nebyla
 *     porušena vlastnost vyhledávacího stromu,
 *  2. je-li porušena vlastnost haldy, budeme «rotacemi» přesouvat
 *     nový uzel směrem ke kořenu, a to až do chvíle, než se tím
 *     vlastnost haldy obnoví.
 *
 * Budou-li priority přiděleny náhodně, vložení uzlu do větší
 * hloubky vede i k vyšší pravděpodobnosti, že tím bude vlastnost
 * haldy porušena; navíc rotace, které obnovují vlastnost haldy,
 * zároveň snižují maximální hloubku stromu. */

/* Implementujte typ ‹treap›, který bude reprezentovat množinu
 * pomocí datové struktury «treap» a poskytovat tyto operace (‹t› je
 * hodnota typu ‹treap›, ‹k›, ‹p› jsou hodnoty typu ‹int›):
 *
 *  • implicitně sestrojená instance ‹treap› reprezentuje prázdnou
 *    množinu,
 *  • ‹t.insert( k, p )› vloží klíč ‹k› s prioritou ‹p› (není-li
 *    uvedena, použije se náhodná); metoda vrací ‹true› pokud byl
 *    prvek skutečně vložen (dosud nebyl přítomen),
 *  • ‹t.erase( k )› odstraní klíč ‹k› a vrátí ‹true› byl-li
 *    přítomen,
 *  • ‹t.contains( k )› vrátí ‹true› je-li klíč ‹k› přítomen,
 *  • ‹t.priority( k )› vrátí prioritu klíče ‹k› (není-li přítomen,
 *    chování není definováno),
 *  • ‹t.clear()› smaže všechny přítomné klíče,
 *  • ‹t.size()› vrátí počet uložených klíčů,
 *  • ‹t.copy( v )›, kde ‹v› je reference na ‹std::vector< int >›,
 *    v lineárním čase vloží na konec ‹v› všechny klíče z ‹t› ve
 *    vzestupném pořadí,
 *  • metodu ‹t.root()›, které výsledkem je ukazatel ‹p›, pro který:
 *    ◦ ‹p->left()› vrátí obdobný ukazatel na levý podstrom,
 *    ◦ ‹p->right()› vrátí ukazatel na pravý podstrom,
 *    ◦ ‹p->key()› vrátí klíč uložený v uzlu reprezentovaném ‹p›,
 *    ◦ ‹p->priority()› vrátí prioritu uzlu ‹p›,
 *    ◦ je-li příslušný strom (podstrom) prázdný, ‹p› je ‹nullptr›.
 *  • konečně hodnoty typu ‹treap› nechť je možné přesouvat,
 *    kopírovat a také přiřazovat (a to i přesunem).¹
 *
 * Metody ‹insert›, ‹erase› a ‹contains› musí mít složitost lineární
 * k «výšce» stromu (při vhodné volbě priorit tedy očekávaně
 * logaritmickou k počtu klíčů). Metoda ‹erase› nemusí nutně
 * zachovat vazbu mezi klíči a prioritami (tzn. může přesunout klíč
 * do jiného uzlu aniž by zároveň přesunula prioritu). */
enum status{found, not_found};

struct treap_node{
    int k;
    int prio;
    std::unique_ptr< treap_node > l; 
    std::unique_ptr< treap_node > r;
    treap_node *parent = nullptr;
    treap_node(int k, int prio): k{k}, prio{prio}{}
    treap_node(int k): k{k}{}
    int key()const{
        return k;
    }
    int priority()const{
        return prio;
    }
    treap_node *left(){
        return l.get();
    }
    treap_node *right(){
        return r.get();
    }
};

struct treap{
    std::unique_ptr< treap_node > rot;
    int _size = 0;

    std::pair<treap_node *, status> search(int key)const{
        treap_node *cur = root();

        while ( cur->k != key){
            if (key < cur->k){
                if (cur->l == nullptr)
                    return {cur, status::not_found};
                cur = cur->left();
            } else{
                if (cur->r == nullptr)
                    return {cur, status::not_found};
                cur = cur->right();
            }
        }
        return {cur, status::found};
    }

    void rotate_left(treap_node *node){

        treap_node &r = *(node->r);
        treap_node &p = *(node->parent);

        auto nptr = !node->parent ? std::move(rot) : std::move((node->k < p.k ? p.l : p.r));
        auto rptr = std::move(node->r);
        auto rlptr = std::move(r.l);
                
        //right cannot be nullptr, rlptr == nullptr is fine
        if (node->parent){
            rptr->parent = &p;
            (node->k < p.k ? p.l : p.r) = std::move(rptr);
        }
        else{
            rptr->parent = nullptr;
            rot = std::move(rptr);
        }
        
        if (rlptr)
            rlptr->parent = node;
        node->parent = &r;

        node->r = std::move(rlptr);
        r.l = std::move(nptr);
    }

    void rotate_right(treap_node *node){


        treap_node &l = *(node->l);
        treap_node &p = *(node->parent);

        auto nptr = !node->parent ? std::move(rot) : std::move((node->k < p.k ? p.l : p.r));
        auto lptr = std::move(node->l);
        auto lrptr = std::move(l.r);
        

        if (node->parent){
            lptr->parent = &p;
            (node->k < p.k ? p.l : p.r) = std::move(lptr);
        } else{
            lptr->parent = nullptr;
            rot = std::move(lptr);
        }

        if (lrptr)
            lrptr->parent = node;
        node->parent = &l;

        node->l = std::move(lrptr);
        l.r = std::move(nptr);
    }

    bool is_correct(treap_node *node){
        return  ((!node->l) || (node->l && node->prio > node->l->prio)) &&
                ((!node->r) || (node->r && node->prio > node->r->prio));
    }

    void fix_rotation(treap_node *node){
        if (is_correct(node))
            return;
        if (((node->l && node->r) && (node->l->prio > node->r->prio)) || !node->r)
            rotate_right(node);
        else
            rotate_left(node);
        if(node->parent && node->parent->parent)
            fix_rotation(node->parent->parent);
    }

    bool insert( int k, int prio = std::rand()){
        if (root() == nullptr){
            rot = std::make_unique< treap_node >(k, prio);
            ++_size;
            return true;
        }

        auto [ptr, stat] = search(k);
        if (stat == status::found)
            return false;

        (k < ptr->k ? ptr->l : ptr->r) = std::make_unique< treap_node >(k, prio);
        (k < ptr->k ? ptr->l : ptr->r)->parent = ptr;

        fix_rotation(ptr);
        ++_size;
        return true;
    }

    void remove(treap_node *node){
        if(rot.get() == node)
            rot.reset();
        else
            (node->key() < node->parent->key() ? node->parent->l : node->parent->r).reset();
    }

    void replace(treap_node *node){
        treap_node *p = node->parent;
        ( node->l ? node->l : node->r)->parent = node->parent;
        (p ? (node->key() < p->key() ? p->l : p->r) : rot) = std::move(( node->l ? node->l : node->r));
    }

    void shift_down(treap_node *n){
        if (n->r->priority() > n->l->priority())
            rotate_left(n);
        else
            rotate_right(n);

    }
    void erase(treap_node *node){

        if (!node->l && !node->r)
            remove(node);
        else if ((!node->l && node->r) || (!node->r && node->l))
            replace(node);
        else{
            shift_down(node);
            erase(node);
        }
    }
    bool erase(int key){
        if (!root())
            return false;
        auto[ptr, stat] = search(key);
        if (stat == status::not_found)
            return false;
        erase(ptr);
        return true;
    }
    bool contains( int key )const {
        if (root() == nullptr)
            return false;
        auto[ptr, stat] = search(key);
        return stat == status::found;
    }
    int priority( int key )const{
        auto[ptr, stat] = search(key);
        return ptr ? ptr->prio : 0;
    }

    void clear(){
        rot.reset();
    }

    int size()const{
        return _size;
    }
    void copy_rec(std::vector< int > &v, treap_node *node)const{
        if (node->l)
            copy_rec(v, node->left());

        v.push_back(node->key());

        if (node->r)
            copy_rec(v, node->right());
    }

    void copy(std::vector< int > &v ){
        return copy_rec(v, root());
    }

    treap_node *root()const{
        return rot.get();
    }

};

/* ¹ Verze s přesunem můžete volitelně vynechat (v takovém případě
 *   je označte jako smazané). Budou-li přítomny, budou testovány.
 *   Implementace přesunu je podmínkou hodnocení kvality známkou A. */

int main()
{
    treap t;
    std::vector< int > vec;

    assert( t.size() == 0 );
    assert( t.insert( 1, 0 ) );
    assert( !t.insert( 1, 1 ) );

    t.copy( vec );
    assert(( vec == std::vector{ 1 } ));
    assert( t.root() != nullptr );
    assert( t.root()->left() == nullptr );
    assert( t.root()->right() == nullptr );
    assert( t.root()->key() == 1 );
    assert( t.root()->priority() == 0 );

    assert( t.contains( 1 ) );
    assert( !t.contains( 2 ) );
    assert( t.erase( 1 ) );
    assert( !t.erase( 1 ) );
    assert( !t.contains( 1 ) );

    treap t1{};
    t1.insert( 1, 2 ); 
    t1.insert( 3, 1 );

    treap test{};
    test.insert(20, 2);
    test.insert(40, 4);
    test.insert(30, 5);
    test.insert(70, 10);
    test.insert(50, 15);
    assert(test.erase(30));
    assert(!test.erase(30));

    return 0;
}
