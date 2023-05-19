/** Grade: @B
 **
 ** ---
 **
 ** x = OK, - = minor issues, ! = major issues
 **
 ** * [x] clearly describes solution to the problem
 ** * [x] correctly decomposes the problem
 ** * [-] doesn't have code duplication
 **   * `&` vs `&&`, `set` vs `take`
 **     please try to think about it, in case you have any issue with it, feel free
 ** to reach out
 ** * [-] uses correct abstractions, algorithms and data structures
 **   * you definitely don't have to compute the size recursively, it was intended
 ** to be used as it usually is on the containers, just the direct “successors”
 **
 ** ---
 **
 ** Summary (+1s, suggestions, rants, confessions, etc.):
 ** * messages in the exceptions /o\
 **
 ** ---
 **
 ** In case you have anything to discuss or want to clarify any of my comments
 ** from the review, feel free to reach out via mail or Discord. **/
#include <memory>
#include <vector>
#include <cassert>
#include <map>

/* Uvažujme stromovou strukturu, která má 4 typy uzlů, a která
 * představuje zjednodušený JSON:
 *
 *  • ‹node_bool› – listy typu ‹bool›,
 *  • ‹node_int› – listy typu ‹int›,
 *  • ‹node_array› – indexované celými čísly souvisle od nuly,
 *  • ‹node_object› – klíčované libovolnými celými čísly.
 *
 * Typ ‹tree› pak reprezentuje libovolný takový strom (včetně
 * prázdného a jednoprvkového). Pro hodnoty ‹t› typu ‹tree›, ‹n›
 * libovolného výše uvedeného typu ‹node_X› a ‹idx› typu ‹int›, jsou
 * všechny níže uvedené výrazy dobře utvořené.
 *
 * Práce s hodnotami typu ‹tree›:
 *
 *  • ‹t.is_null()› – vrátí ‹true› reprezentuje-li tato hodnota
 *    «prázdný strom»,
 *  • ‹*t› – platí-li ‹!t.is_null()›, jsou ‹(*t)› a ‹n› záměnné,
 *    jinak není definováno,
 *  • implicitně sestrojená hodnota reprezentuje prázdný strom,
 *  • hodnoty typu ‹tree› lze také vytvořit volnými funkcemi
 *    ‹make_X›, kde výsledkem je vždy strom s jediným uzlem typu
 *    ‹node_X› (v případě ‹make_bool› resp. ‹make_int› s hodnotou
 *    ‹false› resp. ‹0›, není-li v parametru uvedeno jinak).
 *
 * Hodnoty typu ‹node_X› lze sestrojit implicitně, a reprezentují
 * ‹false›, ‹0› nebo prázdné pole (objekt).
 *
 * Skalární operace (výsledkem je zabudovaný skalární typ):
 *
 *  • ‹n.is_X()› – vrátí ‹true›, je-li typ daného uzlu ‹node_X›
 *    (např. ‹is_bool()› určí, je-li uzel typu ‹node_bool›),
 *  • ‹n.size()› vrátí počet potomků daného uzlu (pro listy 0),
 *  • ‹n.as_bool()› vrátí ‹true› je-li ‹n› uzel typu ‹node_bool› a
 *    má hodnotu ‹true›, nebo je to uzel typu ‹node_int› a má
 *    nenulovou hodnotu, nebo je to neprázdný uzel typu ‹node_array›
 *    nebo ‹node_object›,
 *  • ‹n.as_int()› vrátí 1 nebo 0 pro uzel typu ‹node_bool›, hodnotu
 *    uloženou n uzlu ‹node_int›, nebo skončí výjimkou
 *    ‹std::domain_error›.
 *
 * Operace přístupu k potomkům:
 *
 *  • ‹n.get( idx )› vrátí odkaz (referenci) na potomka:
 *    ◦ s indexem (klíčem) ‹idx› vhodného typu tak, aby
 *      s ní bylo možné pracovat jako s libovolnou hodnotou typu
 *      ‹node_X›, nebo
 *    ◦ skončí výjimkou ‹std::out_of_range› když takový potomek
 *      neexistuje,
 *  • ‹n.copy( idx )› vrátí potomka na indexu (s klíčem) ‹idx› jako
 *    «hodnotu» typu ‹tree›, nebo skončí výjimkou
 *    ‹std::out_of_range› neexistuje-li takový.
 *
 * Operace, které upravují existující strom:
 *
 *  • ‹n.set( idx, t )› nastaví potomka na indexu nebo u klíče ‹i› na
 *    hodnotu ‹t›, přitom samotné ‹t› není nijak dotčeno, přitom:
 *    ◦ je-li ‹n› typu ‹node_array›, je rozšířeno dle potřeby tak,
 *      aby byl ‹idx› platný index, přitom takto vytvořené indexy
 *      jsou «prázdné»),
 *    ◦ je-li ‹n› typu ‹node_bool› nebo ‹node_int›, skončí
 *      s výjimkou ‹std::domain_error›,
 *  • ‹n.take( idx, t )› totéž jako ‹set›, ale podstrom je z ‹t›
 *    přesunut, tzn. metoda ‹take› nebude žádné uzly kopírovat a po
 *    jejím skončení bude platit ‹t.is_null()›.
 *
 * Všechny metody a návratové hodnoty referenčních typů musí správně
 * pracovat s kvalifikací ‹const›. Vytvoříme-li kopii hodnoty typu
 * ‹tree›, tato bude obsahovat kopii celého stromu. Je-li umožněno
 * kopírování jednotlivých uzlů, nemá určeno konkrétní chování. */
struct node;
/** I'm a bit afraid after seeing this… **/
void set_unique(std::unique_ptr<node>&,const node*);

struct tree{
/** Have you ever heard of `clang-format`? **/
    std::unique_ptr<node>root;
    bool is_null() const { return root == nullptr; }
    tree &operator=(const tree&t){
        set_unique(root, t.root.get());
        return *this;
    }
/** This can be `default` IMO. **/
    tree &operator=(tree&&t){
        root = std::move(t.root);
        return *this;
    }

    tree() = default;
    tree(std::unique_ptr<node>r): root{std::move(r)}{}
    tree(const tree&t){
        set_unique(root, t.root.get());
    }
    tree(tree&&t){
        root = std::move(t.root);
    }
    const node &operator*()const{
        return *root;
    }
    node &operator*(){
        return *root;
    }
};

struct node{
    virtual bool is_bool() const   { return false; }
    virtual bool is_int() const    { return false; }
    virtual bool is_array() const  { return false; }
    virtual bool is_object() const { return false; }
    virtual int size() const       { return 0; }

/** I hope that you do that at work too :) Would it be »that« hard to just write
 ** some »useful« messages in the exceptions? **/
    virtual int as_int() const         { throw std::domain_error("AAAAAA"); }
    virtual node &get(int)             { throw std::out_of_range("AJAJAJ"); }
    virtual const node &get(int) const { throw std::out_of_range("AJAJAJ"); }
    virtual tree copy(int)const        { throw std::out_of_range("EJEJEJ"); }
    virtual void set(int,const tree&)  { throw std::domain_error("OJOJOJ"); }
    virtual void set(int, tree&&)      { throw std::domain_error("OJOJOJ"); }
    virtual void take(int, tree&)      { throw std::domain_error("UJUJUJ"); }
    virtual void take(int, tree&&)     { throw std::domain_error("UJUJUJ"); }
    virtual bool as_bool() const = 0;

    virtual ~node() = default;
};

struct node_bool : public node {
    bool value;
    node_bool &operator=(const node_bool&) = default;
    node_bool(const node_bool &) = default;
    node_bool(bool value): value{value}{}
    node_bool() = default;
    bool is_bool() const override { return true; }
    bool as_bool() const override { return value; }
    int as_int()const override { return value; }
};

struct node_int : public node {
    int value;
    node_int &operator=(const node_int&) = default;
    node_int(const node_int&) = default;
    node_int() = default;
    node_int(int val): value{val}{}

    bool is_int() const override { return true; }
    bool as_bool() const override { return value != 0; }
    int as_int()const override { return value; }
};

struct node_object : public node {
/** I would probably use some type alias for the `std::unique_ptr<node>`, it would
 ** make the code much more readable. **/
    std::map<int, std::unique_ptr<node>> data = {};
    node_object &operator=(const node_object&) = default;
    node_object(const node_object&o){
        for (auto & [k, v] : o.data)
            set_unique(data[k], v.get());
    }
    node_object() = default;
    bool is_object() const override { return true; }
/** ```suggestion:-0+0
 **     bool as_bool() const override { return !data.empty(); }
 ** ```
 **
 ** Be careful about the fact that computing the size »can« be less efficient than a
 **  plain check for emptiness. **/
    bool as_bool() const override { return size() > 0; }
    void set(int k, const tree&t) override {
        std::unique_ptr<node> a;
        set_unique(a, t.root.get());
        data[k] = std::move(a);
    }
    void set(int k, tree&&t) override { data[k] = std::move(t.root); }
    
    node &get(int k) override { 
        if (!data.contains(k) || !data[k]) throw  std::out_of_range("AJAJAJ");
        return *(data[k]);
    }
    const node &get(int k) const override{ 
        if (!data.contains(k) || !data.at(k)) throw  std::out_of_range("AJAJAJ");
        return *(data.at(k));
    }

    void take(int i, tree &t) override { data[i] = std::move(t.root); }
/** Isn't this one enough? :think: **/
    void take(int i, tree &&t) override { data[i] = std::move(t.root); }
    
/** I understand that it may not be that explicit in the assignment, but it should
 ** be just the count of children, so `data.size()`. Please fix it. **/
    int size()const override{
        int res = 0;
        for(const auto &[k, v] : data){
            if (v)
                res += v->size() + 1;
        }
        return res;
    }
    tree copy(int)const override;
};

struct node_array : public node {
    std::vector<std::unique_ptr<node>> vec;
    node_array &operator=(const node_array&) = default;
    node_array() = default;
    node_array(const node_array& other){
        for (auto &p : other.vec){
            vec.emplace_back(nullptr);
            set_unique(vec.back(), p.get());
        }
    }
    bool is_array()const override { return true; }
    bool as_bool()const override { return size() > 0; }
    node &get(int i) override{
        if (i >= static_cast<int>(vec.size()) || !vec[i])
            throw std::out_of_range("AJAJAJ");
        return *(vec[i]);
    }
    const node &get(int i)const override{
        if (i >= static_cast<int>(vec.size()) || !vec[i])
            throw std::out_of_range("AJAJAJ");
        return *(vec[i]);
    }
    tree copy(int)const override;

/** Could you try to think about a way how to reduce this copy-paste? **/
    void set(int i, const tree &t) override{
        std::unique_ptr<node> a;
        set_unique(a, t.root.get());
        if (i >= static_cast<int>(vec.size())) vec.resize(i + 1);
        vec[i] = std::move(a);
    }

    void set(int i, tree &&t) override{
        if (i >= static_cast<int>(vec.size())) vec.resize(i + 1);
        vec[i] = std::move(t.root);
    }

    void take(int i, tree &t) override{
        if (i >= static_cast<int>(vec.size())) vec.resize(i + 1);
        vec[i] = std::move(t.root);
    }

    void take(int i, tree &&t) override{
        if (i >= static_cast<int>(vec.size())) vec.resize(i + 1);
        vec[i] = std::move(t.root);
    }
    int size()const override{
        int res = 0;
        for(const auto &p : vec){
            if (p)
                res += p->size() + 1;
        }
        return res;
    }
};

/** I would probably go with something like `.clone` or `.copy` as a virtual method. **/
void set_unique(std::unique_ptr<node>&plac, const node *p){
    if (!p)
        plac = nullptr;
    else if (p->is_array())
        plac = std::make_unique<node_array>(*dynamic_cast<const node_array*>(p));
    else if (p->is_bool())
        plac = std::make_unique<node_bool>(*dynamic_cast<const node_bool*>(p));
    else if (p->is_int())
        plac = std::make_unique<node_int>(*dynamic_cast<const node_int*>(p));
    else if (p->is_object())
        plac = std::make_unique<node_object>(*dynamic_cast<const node_object*>(p));
}

tree make_bool(bool val){return {std::make_unique<node_bool>(val)};}
tree make_bool(){return {std::make_unique<node_bool>()};}
tree make_int(){return {std::make_unique<node_int>()};}
tree make_int(int val){return {std::make_unique<node_int>(val)};}
tree make_array(){return {std::make_unique<node_array>()};}
tree make_object(){return {std::make_unique<node_object>()};}

tree node_array::copy(int i)const{
    if (i >= static_cast<int>(vec.size()))
        throw std::out_of_range("EJEJEJ");
    std::unique_ptr<node> a;
    set_unique(a, vec[i].get());
    return {std::move(a)};
}
tree node_object::copy(int i)const{
    if (!data.contains(i))
        throw std::out_of_range("EJEJEJ");
    std::unique_ptr<node> a;
    set_unique(a, data.at(i).get());
    return {std::move(a)};
}

int main()
{

   
    tree tt = make_bool( true ),
         tf = make_bool(),
         ta = make_array(),
         to = make_object();

    const tree &c_tt = tt,
               &c_ta = ta,
               &c_to = to;

    auto &na = *ta;
    const auto &c_na = *c_ta;
    auto &no = *to;
    const auto &c_no = no;

    assert( (*c_tt).as_bool() );
    assert( !(*tf).as_bool() );
    assert( !c_na.as_bool() );

    na.set( 0, ta );
    na.take( 1, make_bool() );

    assert( !ta.is_null() );
    assert( !c_ta.is_null() );
    assert( !c_to.is_null() );

    no.set( 1, ta );
    na.take( 1, to );

    assert( to.is_null() );
    assert( !(*ta).get( 0 ).as_bool() );
    assert( !(*c_ta).get( 0 ).as_bool() );
    assert( c_no.get( 1 ).size() == 2 );

    {
        tree t{};
        t = make_bool(false);
        assert(!(t.is_null()));
        auto xx = t;
        assert(!(xx.is_null()));
        assert((*t).is_bool());

        tree t1 = make_object();
        (*t1).set(1, t);
        (*t1).set(5, make_int(69420));

        assert((*t).is_bool());
        assert((*t1).is_object());
        assert((*t1).get(1).is_bool());

        (*t1).take(2, t);

        assert(t.is_null());
        assert((*t1).get(2).as_bool() == false);

        tree x = make_array();
        (*x).set(0, t1);
        (*x).take(1, t1);
        assert(t1.is_null());
        assert((*x).get(0).get(1).as_bool() == false);
        assert((*x).get(1).get(1).as_bool() == false);
        assert((*x).get(0).get(2).as_bool() == false);
        assert((*x).get(1).get(2).as_bool() == false);
        assert((*x).get(0).get(5).as_int() == 69420);
        assert((*x).get(1).get(5).as_int() == 69420);

    {
            tree t1 = make_array();
    tree t2 = make_int(1);
    tree t3 = make_int(2);
    tree t4 = make_int(3);
    tree t5 = make_bool();
    assert(t4.root->as_int() == 3);
    (*t1).set(0, t2);
    (*t1).set(1, t3);
    (*t1).set(2, t4);
    (*t1).set(3, t5);
    assert((*t1).size() == 4);

    (*t1).set(4, t1);
    assert((*t1).size() == 9);
    (*t1).set(5, t1);

    assert((*t1).size() == 19);

    const auto& n1 = (*t1).get(4);
    assert(n1.size() == 4);
    const auto& n2 = n1.get(1);
    assert(n2.as_int() == 2);

    const tree &c_t1 = t1;
    assert((*c_t1).get(4).get(1).as_int() == 2);

    tree t1_cpy = (*t1).copy(4);
    assert((*t1_cpy).get(3).is_bool());
    assert((*t1_cpy).get(2).as_int() == 3);
    assert((*t1_cpy).size() == 4);

    (*t1).take(6, t1_cpy);
    assert(t1_cpy.is_null());
    assert((*t1).size() == 24);
    }
    }
    {
        tree t{};
        t = make_object();
        tree child_tree = t;
        (*t).set( 0, child_tree );
        (*t).set( 3153600, child_tree );
        (*t).set( 63072000, child_tree );

    assert(!t.is_null());// → , empty → 
    assert(!(*t).get(0).is_bool()); //n_id → 0
    assert(!(*t).get(0).is_int()); //n_id → 0
    assert(!(*t).get(0).is_array()); //n_id → 0
    assert((*t).is_object()); //n_id → 0
    assert((*t).get(0).is_object()); //n_id → 0
    assert((*t).get(3153600).is_object()); //n_id → 0
    assert((*t).get(63072000).is_object()); //n_id → 0

    }
    {
        tree t = make_object();
        tree f = make_array();
        (*t).set(42, tree{});
        (*f).set(42, tree{});
        int c = 0;
        try{ (*t).get(42); } catch (std::out_of_range&){++c;}
        try{ (*f).get(42); } catch (std::out_of_range&){++c;}

        tree t2 = (*t).copy(42);
        assert(t2.is_null());
        tree f2 = (*f).copy(42);
        assert(f2.is_null());
        assert(c == 2);
    }


    return 0;
}

// clang-tidy: -clang-analyzer-cplusplus.Move
