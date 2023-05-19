#define _USE_MATH_DEFINES
#include <cassert>
#include <cmath>

/* Doplňte definice typů ‹point›, ‹polygon› a ‹circle› tak, abyste
 * pak mohli s jejich pomocí možné implementovat tyto čisté funkce:
 *
 *  • ‹make_polygon›, která přijme jako parametr celé číslo (počet
 *    stran) a dále:
 *    ◦ 2 body (střed a některý vrchol), nebo
 *    ◦ 1 bod (střed) a 1 reálné číslo (poloměr opsané kružnice),
 *  • ‹make_circle› které přijme jako parametry:
 *    ◦ 2 body (střed a bod na kružnici), nebo
 *    ◦ 1 bod a 1 reálné číslo (střed a poloměr),
 *  • ‹area›, které přijme ‹polygon› nebo ‹circle› a vrátí plochu
 *    odpovídajícího útvaru.
 *
 * Typ ‹point› nechť má složky ‹x› a ‹y› (reálná čísla). */

struct point{
    double x, y;
};

struct polygon{
    struct point centre;
    int sides;
    double diameter;
};

struct circle{
    struct point centre;
    double diameter;
};

polygon make_polygon(int sides, point centre, point outer){
    double diameter = std::sqrt((centre.x - outer.x)*(centre.x - outer.x) + 
                                (centre.y - outer.y)*(centre.y - outer.y));
    polygon res = {centre, sides, diameter};
    return res;
}

polygon make_polygon(int sides, point centre, double diameter){
    polygon res = {centre, sides, diameter};
    return res;
}


struct circle make_circle(point centre, point outer){
    double diameter = std::sqrt((centre.x - outer.x)*(centre.x - outer.x) + 
                                (centre.y - outer.y)*(centre.y - outer.y));
    circle res = {centre, diameter};
    return res;
}

struct circle make_circle(point centre, double diameter){
    circle res = {centre, diameter};
    return res;
}

double area(polygon p){
    return p.sides * p.diameter * p.diameter * std::sin(2 * M_PI / p.sides) / 2.0;
}

double area(circle c){
    return M_PI * c.diameter * c.diameter;
}

int main()
{
    point p00{ .x = 0, .y = 0 },
          p01{ .x = 0, .y = 1 },
          p10{ .x = 1, .y = 0 },
          p11{ .x = 1, .y = 1 },
          p20{ .x = 2, .y = 0 };

    polygon square = make_polygon( 4, p00, std::sqrt( 2 ) );
    assert( std::fabs( area( square ) - 4 ) < .001 );

    polygon hexagon = make_polygon( 6, p00, p01 );
    assert( std::fabs( area( hexagon ) - 2.598 ) < .001 );

    circle c1 = make_circle( p00, p10 );
    circle c2 = make_circle( p00, p20 );
    circle c3 = make_circle( p00, p11 );

    assert( std::fabs( area( c1 ) -     3.1415 ) < .001 );
    assert( std::fabs( area( c2 ) - 4 * 3.1415 ) < .001 );
    assert( std::fabs( area( c3 ) - 2 * 3.1415 ) < .001 );

    return 0;
}
