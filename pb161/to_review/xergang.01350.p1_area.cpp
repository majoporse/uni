#include <set>
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

struct point {
    double x, y;
};

struct polygon {
    int edges_count;
    double radius;
    point center;
};
struct circle {
    double radius;
    point center;
};

polygon make_polygon(int edges_count, point center, point vertex) {
    polygon p;
    p.edges_count = edges_count;
    p.center = center;
    p.radius = std::abs(sqrt(std::pow(center.x - vertex.x, 2) +
                             std::pow(center.y - vertex.y, 2)));
    return p;
}

polygon make_polygon(int edges_count, point center, double radius) {
    polygon p;
    p.edges_count = edges_count;
    p.center = center;
    p.radius = radius;
    return p;
}

circle make_circle(point center, point on_circumference) {
    circle c;
    c.center = center;
    c.radius = std::abs(sqrt(std::pow(center.x - on_circumference.x, 2) +
                             std::pow(center.y - on_circumference.y, 2)));
    return c;
}

circle make_circle(point center, double radius) {
    circle c;
    c.center = center;
    c.radius = radius;
    return c;
}

double area(polygon p) {
    return p.edges_count * std::pow(p.radius, 2) / 2 *
           sin(2 * M_PI / p.edges_count);
}

double area(circle c) { return M_PI * c.radius * c.radius; }

int main() {
    point p00{.x = 0, .y = 0}, p01{.x = 0, .y = 1}, p10{.x = 1, .y = 0},
        p11{.x = 1, .y = 1}, p20{.x = 2, .y = 0};

    polygon square = make_polygon(4, p00, std::sqrt(2));
    assert(std::fabs(area(square) - 4) < .001);

    polygon hexagon = make_polygon(6, p00, p01);
    assert(std::fabs(area(hexagon) - 2.598) < .001);

    circle c1 = make_circle(p00, p10);
    circle c2 = make_circle(p00, p20);
    circle c3 = make_circle(p00, p11);

    assert(std::fabs(area(c1) - 3.1415) < .001);
    assert(std::fabs(area(c2) - 4 * 3.1415) < .001);
    assert(std::fabs(area(c3) - 2 * 3.1415) < .001);

    return 0;
}
