#include <cassert>
#include <memory>
#include <list>
#include <cmath>
#include <vector>
#include <map>
#include <algorithm>
#include <utility>

/* V této úloze budete programovat jednoduchou hru, ve které se ve
 * volném třírozměrném prostoru pohybují robotické entity tří barev:
 *
 *  1. červený robot (třída ‹robot_red›):
 *     
 *     ◦ není-li uzamčený a na hrací ploše je alespoň jeden cizí
 *       zelený robot, uzamkne se na ten nejbližší, jinak stojí na
 *       místě,
 *     ◦ je-li na nějaký robot uzamčený, přibližuje se přímo k němu
 *       (tzn. směr pohybu je vždy v aktuálním směru tohoto robotu),
 *     
 *  2. zelený robot (třída ‹robot_green›):
 *     
 *     ◦ je-li nějaký cizí modrý robot ve vzdálenosti do 10 metrů,
 *       směruje přímo k tomu nejbližšímu,
 *     ◦ je-li nejbližší takový robot dále než 10 metrů, zelený
 *       robot se teleportuje do místa, které leží na jejich
 *       spojnici, 8 metrů od cílového robotu na jeho «vzdálenější»
 *       straně,
 *     ◦ jinak stojí na místě.
 *     
 *  3. modrý robot (třída ‹robot_blue›):
 *     
 *     ◦ směruje k nejbližšímu cizímu červenému robotu, existuje-li
 *       nějaký,
 *     ◦ jinak se «poloviční rychlostí» pohybuje po přímce ve směru,
 *       který měl naposledy,
 *     ◦ na začátku hry je otočen směrem k začátku souřadnicového
 *       systému (je-li přímo v počátku, chování není určeno).
 *
 * Roboty se pohybují rychlostí 15 m/s. Dostanou-li se dva roboty
 * různých barev a různých vlastníků do vzdálenosti 1 metr nebo
 * menší, jeden z nich zanikne podle pravidla:
 *
 *  • červený vítězí nad zeleným,
 *  • zelený vítězí nad modrým a konečně
 *  • modrý vítězí nad červeným.
 *
 * Hra jako celek nechť je zapouzdřená ve třídě ‹game›. Bude mít
 * tyto metody:
 *
 *  • metoda ‹tick› posune čas o 1/60 sekundy, a provede tyto akce:
 *    
 *    a. všechny roboty se posunou na své nové pozice «zároveň»,
 *       tzn. dotáže-li se nějaký robot na aktuální pozici jiného
 *       robotu, dostane souřadnice, které měl tento na konci
 *       předchozího tiku,
 *    b. vzájemné ničení robotů, které proběhne opět zároveň –
 *       sejdou-li se v dostatečné blízkosti roboty všech tří barev,
 *       zaniknou všechny.
 *    
 *  • metoda ‹run› simuluje hru až do jejího konce,
 *    
 *    ◦ tzn. do chvíle, kdy nemůže zaniknout žádný další robot a
 *    ◦ vrátí dvojici (počet tiků, hráči),
 *    ◦ kde „hráči“ je vektor identifikátorů hráčů, seřazený podle
 *      počtu zbývajících robotů; je-li více hráčů se stejným počtem
 *      robotů, první bude ten s větším počtem červených, dále
 *      zelených a nakonec modrých robotů; je-li stále hráčů více,
 *      budou uspořádáni podle svého identifikátoru,
 *      
 *  • metody ‹add_X› pro ‹X› = ‹red›, ‹green› nebo ‹blue›, které
 *    přidají do hry robota odpovídající barvy, a které mají dva
 *    parametry:
 *    
 *    ◦ počáteční pozici, jako trojici hodnot typu ‹double› (zadané
 *      v metrech v kartézské soustavě),
 *    ◦ nenulový celočíselný identifikátor hráče-vlastníka. */
struct robot;
using r_vec = std::vector<robot *>;
struct robot_red;
struct robot_green;
struct robot_blue;
struct robot{
    bool dead = false;
    int owner;
    double speed = 15;
    double x, y, z;
    double dest_x = 0, dest_y = 0, dest_z = 0;
    robot* chasing = nullptr;

    robot(int owner, double x, double y, double z): owner{owner}, x{x}, y{y}, z{z}{}
    virtual void lock_target(r_vec&, r_vec&, r_vec&) = 0;

    double distance(const robot* other) const {return std::hypot(x - other->x, y - other->y, z - other->z);}
    double dest_dist() const {return std::hypot(x - dest_x, y - dest_y, z - dest_z);}
    bool closer(const robot* closest, const robot* g) const {return distance(closest) > distance(g);}
    double angle_to(robot *goal) {return std::atan2(x - goal->x, y - goal->y);}
    void set_dest(robot *des){
        dest_x = des->x;
        dest_y = des->y;
        dest_z = des->z;
    }

    virtual void move(){
        double dist = dest_dist();
        if (!speed || !dist) return;
        x += (dest_x - x) * (speed / 60.0) / dist;
        y += (dest_y - y) * (speed / 60.0) / dist;
        z += (dest_z - z) * (speed / 60.0) / dist;
    }

    void find_closest(robot*& old, std::vector< robot*> &robots){
        for (auto it = robots.begin(); it != robots.end(); ++it){
            if ((*it)->dead){
                std::swap(robots.back(), *it);
                robots.pop_back();
                it--;
            }
            else if ((!old || (old && closer(old, *it))) && ((*it)->owner != owner))
                old = *it;
        }
    }

    virtual void fight_nearby(r_vec&, r_vec&, r_vec&) = 0;

    virtual int pos() = 0;
    virtual ~robot() = default;
};


struct robot_green: public robot{
    robot_green(int o, double x, double y, double z): robot(o, x, y, z) {}
    int pos()override{return 1;}

    void teleport_behind(){
        double dist = dest_dist();
        x = dest_x + (dest_x - x) * 8.0 / dist;
        y = dest_y + (dest_y - y) * 8.0 / dist;
        z = dest_z + (dest_z - z) * 8.0 / dist;
    }
    void move()override{
        if (chasing && distance(chasing) > 10)
            teleport_behind();
        else
            robot::move();
    }

    void lock_target(r_vec&, r_vec&, r_vec& blues) override {
        if (chasing && chasing->dead) chasing = nullptr;
        find_closest(chasing, blues);
        if (!chasing) 
            speed = 0;
        else {
            set_dest(chasing);
            speed = 15;
        }
    }
    void fight_nearby(r_vec&, r_vec&, r_vec& blues) override{
        for (robot *r: blues)
            if(distance(r) <= 1 && r->owner != owner) r->dead = true;
        }
};

struct robot_red : public robot{
    robot_red(int o, double x, double y, double z): robot(o, x, y, z) {}
    int pos()override{return 0;}

    void lock_target(r_vec&, r_vec& greens, r_vec&) override {
        if (chasing && chasing->dead) chasing = nullptr;
        if (!chasing) 
            find_closest(chasing, greens);

        if (!chasing)
            speed = 0;
        else{
            set_dest(chasing);
            speed = 15;
        }
    }
    void fight_nearby(r_vec&, r_vec& greens, r_vec&) override{
        for (robot *r: greens)
            if(distance(r) <= 1 && r->owner != owner) r->dead = true;
        }
};


struct robot_blue: public robot{
    using robot::robot;
    robot_blue(int o, double x, double y, double z): robot(o, x, y, z) {dest_x = 0; dest_y = 0; dest_z = 0;}
    int pos()override{return 2;}

    void lock_target(r_vec& reds, r_vec&, r_vec&) override {        
        if (chasing && chasing->dead) chasing = nullptr;
        find_closest(chasing, reds);
        if (!chasing) 
            speed = 7.5;
        else{
            set_dest(chasing);
            speed = 15;
        }
    }

    void move() override{
        if(!chasing){
            double dist = dest_dist();
            dest_x += (dest_x - x) * (speed / 60.0) / dist;
            dest_y += (dest_y - y) * (speed / 60.0) / dist;
            dest_z += (dest_z - z) * (speed / 60.0) / dist;
        }
        robot::move();
    }

    void fight_nearby(r_vec& reds, r_vec&, r_vec&) override{
        for (robot *r: reds)
            if(distance(r) <= 1 && r->owner != owner) r->dead = true;
        }
};

struct game{
    std::map<int, std::vector<int>> player_stats;
    std::vector<std::unique_ptr<robot>> robots;
    r_vec red_robots, green_robots, blue_robots;

    void tick(){

        for (auto &robot: robots)
                robot->move();

        for(auto &robot: robots)
            robot->fight_nearby(red_robots, green_robots, blue_robots);

        for (auto &robot: robots)
            robot->lock_target(red_robots, green_robots, blue_robots);
        
        for(auto it = robots.begin(); it != robots.end(); ++it){
            if ((*it)->dead){
                robots.back().swap(*it);
                robots.pop_back();
                --it;
            }
        }
    }      

    bool check_moves(){
        for(auto &robot : robots){
            if (robot->chasing)
                return true;
        }
        return false;
    }

    std::tuple<int, std::vector<int>> run(){

        int ticks = 0;

        for(auto &robot: robots)
            robot->lock_target(red_robots, green_robots, blue_robots);
        
        for (;check_moves(); ++ticks){
            tick();
        }

        for (auto &robot : robots){
            player_stats[robot->owner][robot->pos()]++;
        }

        std::vector<std::tuple< int, std::vector<int>>> help;
        for(auto &[id, key] : player_stats)
            help.emplace_back(id, key);
        
        std::sort(help.begin(), help.end(), [](auto &a, auto &z) {
            auto &[id, x] = a;
            auto [r, g, b] = std::tuple<int, int, int>(x[0], x[1], x[2]);
            auto t = r + g + b;
            
            auto [id1, x1] = z;
            auto [r1, g1, b1] = std::tuple<int, int, int>(x1[0], x1[1], x1[2]);
            auto t1 = r1 + g1 + b1;

            return t > t1 || (t == t1 && (r > r1 || (r == r1 && (g > g1 || 
                    (g == g1 && (b > b1 || (b == b1 && id < id1)))))));
            });

        std::vector<int> res;
        for(auto [id, _] : help)
            res.emplace_back(id);
        return {ticks, res};
    }

    void add_red(std::tuple<double, double, double> pos, int owner){
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_red>(owner, x, y, z));
        red_robots.emplace_back(robots.back().get());
        player_stats[owner] = {0,0,0};
    }
    void add_green(std::tuple<double, double, double> pos, int owner){
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_green>(owner, x, y, z));
        green_robots.emplace_back(robots.back().get());
        player_stats[owner] = {0,0,0};
    }
    void add_blue(std::tuple<double, double, double> pos, int owner){
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_blue>(owner, x, y, z));
        blue_robots.emplace_back(robots.back().get());
        player_stats[owner] = {0,0,0};
    }
};


int main()
{
    game g;

    auto [ ticks, players ] = g.run();
    assert( ticks == 0 );
    assert( players.empty() );

    g.add_red( { -5, 0, 0 }, 1 );
    g.add_red( {  5, 0, 0 }, 1 );
    g.add_red( {  0, 0, 0 }, 2 );

    std::tie( ticks, players ) = g.run();
    assert( ticks == 0 );
    assert(( players == std::vector{ 1, 2 } ));

    g.add_green( {  9.6, 0, 0 }, 2 );
    g.add_green( { -9.6, 0, 0 }, 2 );

    std::tie( ticks, players ) = g.run();
    assert(( players == std::vector{ 1, 2 } ));
    assert( ticks == 15 );

    {
    game x;
    x.add_red({0,1,0}, 1);
    x.add_green({2,1,0}, 0);
    auto [a, b] = x.run();
    assert(a == 4);
    assert((b == std::vector{1, 0} ));
    }
    {
    game x;
    x.add_red({0,1,0}, 1);
    x.add_green({0,3,0}, 0);
    auto [a, b] = x.run();
    assert(a == 4);
    assert((b == std::vector{1, 0} ));
    }
    {
    game x;
    x.add_red({0,1,0}, 1);
    x.add_green({0,-1,0}, 0);
    auto [a, b] = x.run();
    assert(a == 4);
    assert((b == std::vector{1, 0} ));
    }
    {
    game x;
    x.add_red({0,1,0}, 1);
    x.add_green({0,1,2}, 0);
    auto [a, b] = x.run();
    assert(a == 4);
    assert((b == std::vector{1, 0} ));
    }

    for (int i = 0; i < 1000; ++i){
        game bots{};
        bots.add_red(   { 15, 0, 0 }, 1 );   // x → 15,  y → 0, z → 0, owner → 1
        bots.add_red(   {-15, 0, 0 }, 2 );   // x → -15, y → 0, z → 0, owner → 2
        bots.add_green( { 15, 0, 0 }, 1 );   // x → 15,  y → 0, z → 0, owner → 1
        bots.add_green( {-15, 0, 0 }, 2 );   // x → -15, y → 0, z → 0, owner → 2
        bots.add_blue(  { 15, 0, 0 }, 1 );   // x → 15,  y → 0, z → 0, owner → 1
        bots.add_blue(  {-15, 0, 0 }, 2 );   // x → -15, y → 0, z → 0, owner → 2
        auto [aa, bb] = bots.run();
        assert(aa == 130);
    }

    {
        game bots{};
        bots.add_red( { 300, 0, 0 }, 3 ); // x → 300, y → 0, z → 0, owner → 3
        bots.add_red( { 300, 0, 0 }, 2 ); // x → -300, y → 0, z → 0, owner → 2
        bots.add_green( { 0, 300, 0 }, 1 ); // x → 0, y → 300, z → 0, owner → 1
        auto [x, y] = bots.run(); // expected   = [ 1694, [ 2, 3, 1 ] ]
        assert(x == 1694);
        assert((y == std::vector{2,3,1}));
    }
    {
        game bots3{};
        bots3.add_green( { 100 , 0, 0 },  0 );
        bots3.add_blue(  { 1,    0,  0 }, 1 );
        auto aaaaa4 = bots3.run();
    }
//     {
//         game bots{}
//   bots.add_red( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 3
//   bots.add_red( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 2
//   bots.add_green( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 3
//   bots.add_green( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 2
//   bots.add_blue( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 1
//   bots.add_blue( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 1
//     }
// game bots{}
//   bots.add_red( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 3
//   bots.add_red( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 2
//   bots.add_green( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 3
//   bots.add_green( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 2
//   bots.add_blue( { x, y, z }, owner ); x → 15, y → 0, z → 0, owner → 1
//   bots.add_blue( { x, y, z }, owner ); x → -15, y → 0, z → 0, owner → 1
{
        game bots{};
        bots.add_red(   { 15, 0, 0 }, 3 );
        bots.add_red(   {-15, 0, 0 }, 2 );
        bots.add_green( { 15, 0, 0 }, 3 );
        bots.add_green( {-15, 0, 0 }, 2 );
        bots.add_blue(  { 15, 0, 0 }, 1 );
        bots.add_blue(  {-15, 0, 0 }, 1 );
        auto [aa, bb] = bots.run();
        assert(aa == 1);
        assert((bb == std::vector{2,3,1}));

}
{
    game bots{};
    bots.add_red( { 1, -1, 1 }, 0 );// x → 1, y → -1, z → 1, owner → 0
    bots.add_red( { 1, -1, 1 }, 0 );// x → 1, y → -1, z → 1, owner → 0
    bots.add_blue( { 1, -1, 0 }, -1 );// x → 1, y → -1, z → 0, owner → -1

    auto [ aa, bb] = bots.run();
    assert(aa == 1);
    assert((bb == std::vector{-1, 0}));// [ 2, [ -1, 0 ] ]
}
{
        game bots;
        bots.add_red( { 1,-1,1 }, 0 );// x → 1, y → -1, z → 1, owner → 0
        bots.add_green( { -119, -1,  -1}, 0 );// x → -119, y → -1, z → -1, owner →0
        bots.add_blue( { 1,-1,0 }, -1 );// x → 1, y → -1, z → 0, owner → -1

        auto [a, b] = bots.run();
        assert(a == 37);
        std::vector<int> k = {0 , -1};
        assert(b == k);
    }

    {
        game bots;
        bots.add_red( { 1,-1,1 }, 0 );// x → 1, y → -1, z → 1, owner → 0
        bots.add_green( { -14, -1,  -1}, 0 );// x → -14, y → -1, z → -1, owner →0
        bots.add_blue( { 1,-1,0 }, -1 );// x → 1, y → -1, z → 0, owner → -1

        auto [a, b] = bots.run();
        assert(a == 36);
        std::vector<int> k = {0 , -1};
        assert(b == k);
    }
    return 0;
}
