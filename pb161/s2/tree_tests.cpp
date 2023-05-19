#include "e_tree.cpp"

int main(){
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
        tree empty;
        tree empty2;
        tree empty3{empty};
        empty = empty2;
        tree object1 = make_object();
        (*object1).set(1, empty);
        (*object1).set(69, make_int(69));
        (*object1).set(42, make_int(42));
        (*object1).set(1337, make_int(1337));

        assert((*object1).size() == 3);

        tree object2{object1};
        assert((*object2).size() == 3);

        (*object2).take(42049, object1);
        
        assert(object1.is_null());
        assert((*object2).size() == 7);

        object1 = make_object();
        (*object1).set(123123, empty);
        (*object1).set(535431, empty);
        (*object1).set(345351, empty);
        assert((*object1).as_bool() == false);
        tree arr1 = make_array();
        (*arr1).take(42, make_int(42));
        assert((*arr1).as_bool() == true);
        (*arr1).set(42, empty);
        assert((*arr1).as_bool() == false);
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

    return 0;
}