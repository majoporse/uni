#include "c_real.cpp"
#include <iostream>
#include <cassert>
#include <cmath>

real abs(real x) { return x.abs();}
void print(real x) {
    std::cout << x.nom.to_double() << " / " << x.denom.to_double() << "\n";
}

int main()
{
    {
        real zero = 0;
        print(zero);
        real one = 1;
        print(one);
        real ten = 10;
        print(ten);
        real half = one / 2;
        print(half);
        real third = 0.3333;
        print(third);
        real better_third = 0.333333333;
        print(better_third);

    }
    {
        real half = 0.5;
        print(half);
        real a = 0.25;
        print(a);
        real b = 0.78;
        print(b);
        real c = 0.375;
        print(c);
    }
    {
        real a = 0.1;
        print(a);
        real b = 0.01;
        print(b);
        real c = 0.001;
        print(c);
        real d = 0.0001;
        print(d);
    }

    const real EPSILON{10e-5};

    // test_constructor
    {
        real a(1.234);
        print(a);
        assert(abs(a - 1.234) < EPSILON);
    }

    // test_copy_constructor
    {
        real a(1.234);
        real b(a);
        assert(abs(b - 1.234) < EPSILON);
    }

    // test_assignment_operator
    {
        real a(1.234);
        real b;
        b = a;
        assert(abs(b - 1.234) < EPSILON);
    }

    // test_addition_operator
    {
        real a(1.234);
        real b(5.678);
        real c = a + b;
        print(c);
        assert(abs(c - 6.912) < EPSILON);
    }

    // test_subtraction_operator
    {
        real a(5.678);
        real b(1.234);
        real c = a - b;
        print(c);
        assert(abs(c - 4.444) < EPSILON);
    }

    // test_multiplication_operator
    {
        real a(1.234);
        print(a);
        real b(5.678);
        print(b);
        real c = a * b;
        print(c);
        print(7.006652);
        print(c - 7.006652);
        assert(abs(c - 7.006652) < EPSILON);
    }

    // test_division_operator
    {
        real a(5.678);
        real b(1.234);
        real c = a / b;
        assert(abs(c - 4.60129659643) < EPSILON);
    }

    // test_addition_assignment_operator
    {
        real a(1.234);
        real b(5.678);
        a += b;
        assert(abs(a - 6.912) < EPSILON);
    }

    // test_subtraction_assignment_operator
    {
        real a(5.678);
        real b(1.234);
        a -= b;
        assert(abs(a - 4.444) < EPSILON);
    }

    // test_multiplication_assignment_operator 
    {
        real a(1.234);
        real b(5.678);
        a *= b;
        assert(abs(a - 7.006652) < EPSILON);
    }

    // test_division_assignment_operator
    {
        real a(5.678);
        real b(1.234);
        a /= b;
        assert(abs(a - 4.60129659643) < EPSILON);
    }

    // test_equality_operator
    {
        real a(1.234);
        real b(1.234);
        assert(a == b);
    }

    // test_inequality_operator
    {
        real a(1.234);
        real b(5.678);
        assert(a != b);
    }

    // test_less_than_operator
    {
        real a(1.234);
        real b(5.678);
        assert(a < b);
    }

    // test_less_than_or_equal_to_operator
    {
        real a(1.234);
        real b(5.678);
        real c(1.234);
        assert(a <= b);
        assert(a <= c);
    }

    // test_greater_than_operator
    {
        real a(5.678);
        real b(1.234);
        assert(a > b);
    }

    // test_greater_than_or_equal_to_operator
    {
        real a(5.678);
        real b(1.234);
        real c(5.678);
        assert(a >= b);
        assert(a >= c);
    }

    // test_negation_operator 
    {
        real a(1.234);
        real b = -a;
        assert(abs(a + b) <= EPSILON);
    }

    {
        const real EPSILON = 10e-3;

        real a(1.234);
        assert(abs(static_cast<real>(a) - 1.234) < EPSILON);

        real b(2.0);
        assert(abs(static_cast<real>(b) - 2.0) < EPSILON);

        real c = a + b;
        assert(abs(static_cast<real>(c) - 3.234) < EPSILON);

        c = a - b;
        print(c);
        assert(c.is_negative);
        print(static_cast<real>(c) + 0.766);
        assert(abs(static_cast<real>(c) + 0.766) < EPSILON);

        c = a * b;
        assert(abs(static_cast<real>(c) - 2.468) < EPSILON);

        c = a / b;
        assert(abs(static_cast<real>(c) - 0.617) < EPSILON);

        a += b;
        assert(abs(static_cast<real>(a) - 3.234) < EPSILON);

        a -= b;
        assert(abs(static_cast<real>(a) - 1.234) < EPSILON);

        a *= b;
        assert(abs(static_cast<real>(a) - 2.468) < EPSILON);

        a /= b;
        assert(abs(static_cast<real>(a) - 1.234) < EPSILON);

        assert((a == b) == false);
        assert((a != b) == true);
        assert((a < b) == true);
        assert((a <= b) == true);
        assert((a > b) == false);
        assert((a >= b) == false);

        real d = -a;
        assert(abs(static_cast<real>(d) + 1.234) < EPSILON);

        d = a.abs();
        assert(abs(static_cast<real>(d) - 1.234) < EPSILON);

        d = a.reciprocal();
        assert(abs(static_cast<real>(d) - 0.810) < EPSILON);

        d = a.power(-1);
        print(d);
        assert(abs(static_cast<real>(d) - 0.810) < EPSILON);

        d = a.power(2);
        assert(abs(static_cast<real>(d) - 1.522) < EPSILON);

        d = a.power(3);
        assert(abs(static_cast<real>(d) - 1.874) < EPSILON);

        d = a.sqrt(EPSILON);
        assert(abs(static_cast<real>(d) - 1.111) < EPSILON);

        // d = (real{1,1,true}).exp(EPSILON);
        // print(d);
        // assert(abs(static_cast<real>(d) - 2.71828) < EPSILON);

        d = a.exp(EPSILON);
        print(a);
        print(d);
        assert(abs(static_cast<real>(d) - 3.43494186) < EPSILON);

        real e{0.567};
        d = e.log1p(EPSILON);
        print(d);
        assert(abs(static_cast<real>(d) - 0.449162963) < EPSILON);
    }


    {
        real zero = 0;
        real one = 1;
        real ten = 10;
        real half = one / 2;

        real eps = ten.power( -3 );

        real pi( 3.14159265 );
        real sqrt2( 1.41421356 );
        real e( 2.71828182 );
        real l_half( 0.40546511 );

        assert( ( one.exp( eps ) - e ).abs() < eps );
        assert( zero.log1p( eps ).abs() < eps );
        assert( ( half.log1p( eps ) - l_half ).abs() < eps );
        print({1});
        print(one);
        assert( static_cast< real >( 1.0 ) == one );
        assert( one + -one == zero );
        assert( one * ten == ten );

    }

    {
        real zero = 0;
        real zero2 = zero * zero;
        real a = -1;
        real b = -a;
        real zero3 = a + b;
        real zero4 = b + a;
        assert(zero * zero == zero);
        assert(zero == zero2);
        assert(zero == zero3);
        assert(zero == zero4);
    }


    std::cout << "All tests passed!" << std::endl;

    return 0;

}
