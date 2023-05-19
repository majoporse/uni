#include <string_view>
#include <vector>
#include <map>
#include <string>
#include <cmath>
#include <memory>
#include <charconv>
#include <cctype>
#include <variant>
#include <functional>

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


/* Uvažme hru ‹s2/c_robots› – Vaším úkolem bude nyní naprogramovat
 * jednoduchý interpret, který bude hru řídit. Vstupní program
 * sestává ze tří částí:
 *
 *  1. deklarace, které popisují jak roboty ve hře a jejich
 *     startovní pozice, tak případné pomocné proměnné,
 *  2. příkazy, které se provedou jednou na začátku hry,
 *  3. příkazy, které se provedou každý tik, dokud hra neskončí.
 *
 * Program by mohl vypadat například takto: */

std::string_view example_1 = R"(with
  a  = red   1 @ -5.0 0 0
  b  = red   1 @  5.0 0 0
  c  = red   2 @  0.0 0 0
  g1 = green 2 @ -9.6 0 0
  g2 = green 2 @  9.6 0 0
init
  let g1 chase a
  let g2 chase b
repeat
)";

std::string_view example_2 = R"(with
  r = red   2 @  0.0 0 0
  g = green 2 @  0.0 0 0
  b = blue  1 @ -9.6 0 0
  tick = 0
init
  let r chase g
  let g go_to @ 1.0 0 0
repeat
  if tick > 9
    if g is_alive
       let b chase g
  set tick := tick + 1
)";

/* Následuje gramatika ve formátu EBNF, která popisuje syntakticky
 * platné programy; terminály gramatiky jsou «tokeny», které jsou od
 * sebe vždy odděleny alespoň jednou mezerou, nebo předepsaným
 * koncem řádku.
 *
 *     prog = 'with', { decl },
 *            'init', { stmt },
 *            'repeat', { stmt } ;
 *     decl = ident, '=', init, '\n' ;
 *     init = color, num, coord | coord | num ;
 *
 *     color = 'red' | 'green' | 'blue' ;
 *     coord = '@', num, num, num ;
 *
 *     stmt = cmd, '\n' |
 *            'if', cond, stmt ;
 *     cmd  = 'let', ident, 'chase', ident |
 *            'let', ident, 'go_to', expr |
 *            'set', ident, ':=', expr |
 *            'do', stmt, { stmt }, 'end' ;
 *     cond = atom, '=', atom |
 *            atom, '<', atom |
 *            atom, '>', atom |
 *            ident, 'is_alive' ;
 *     expr = atom |
 *            atom, '+', atom |
 *            atom, '-', atom |
 *            atom, '*', atom |
 *            '[', expr, ']' |
 *            '(', expr, ')' ;
 *     atom = ident | coord | num;
 *
 * Krom terminálních řetězců (‹'red'› a pod.) považujeme za tokeny
 * také symboly ‹num› a ‹ident›, zadané těmito pravidly:
 *
 *     num   = [ '-' ], digit, { digit }, [ '.', { digit } ] ;
 *     ident = letter, { letter | digit }
 *     digit = '0' | '1' | … | '9' ;
 *     letter = 'a' | 'b' | … | 'z' | '_' ;
 *
 * V programu se objevují hodnoty tří typů:
 *
 *  1. čísla (hodnoty typu ‹double›),
 *  2. trojice čísel (reprezentuje pozici nebo směr),
 *  3. odkaz na robota.
 *
 * S hodnotami (a proměnnými, které hodnoty daných typů aktuálně
 * obsahují), lze provádět tyto operace:
 *
 *  1. čísla lze sčítat, odečítat, násobit a srovnávat (neterminály
 *     ‹expr› a ‹cond›),
 *  2. trojice lze sčítat, odečítat a srovnat (ale pouze rovností),
 *  3. roboty lze posílat za jiným robotem nebo na zadané
 *     souřadnice (příkaz ‹let›),
 *  4. operace hranaté závorky hodnotu zjednodušuje:
 *
 *     ◦ ‹[ robot ]› je aktuální pozice robota (trojice),
 *     ◦ ‹[ point ]› je Euklidovská vzdálenost bodu od počátku, resp.
 *        velikost směrového vektoru (‹[ p₁ - p₂ ]› tak spočítá
 *        vzdálenost bodů ‹p₁› a ‹p₂›.
 *
 * Operace, které nejsou výše popsané (např. pokus o sečtení
 * robotů), nemají určené chování. Totéž platí pro pokus o použití
 * nedeklarované proměnné (včetně přiřazení do ní). Podobně není
 * určeno chování, nevyhovuje-li vstupní program zadané gramatice.
 *
 * Robot, kterému bylo uloženo pronásledovat (chase) jiného robota,
 * bude na tohoto robota zamčen, až než mu bude uložen jiný cíl,
 * nebo cílový robot zanikne. Nemá-li robot žádný jiný příkaz, stojí
 * na místě (bez ohledu na barvu).
 *
 * Program je předán metodě ‹run› třídy ‹game› jako hodnota typu
 * ‹std::string_view›, návratová hodnota i zde nezmíněná pravidla
 * zůstavají v platnosti z příkladu v druhé sadě. */
struct brackets{
    expr e;
};
enum class cond_type{ equals, less, greater};
struct binary_cond{
    cond_type type;
    atom a;
    atom b;
};

enum class op_type{ plus, minus, times };
struct binary_op{
    op_type type;
    atom a;
    atom b;
};

struct is_alive{
    std::string id;
};

using atom = std::variant<std::string, std::tuple<double, double, double>, int>;
using expr = std::variant<atom, binary_op, std::tuple<double, double, double>, brackets>;
using cond = std::variant<binary_cond, is_alive>;
struct if_st;

struct let_chase{
    std::string id1;
    std::string id2;
};

struct let_goto{
    std::string id;
    expr e;
};

struct set{
    std::string id;
    expr e;
};

struct do_stmt{
    std::vector<stmnt> s;
};

using cmd = std::variant<let_chase, let_goto, set, do_stmt>;
using stmnt = std::variant<cmd, if_st>;

struct if_st{
    cond condition;
    stmnt statement;
};

using variable = std::variant<robot*, std::tuple<double, double, double>, int>;
struct data{
    std::map<std::string, variable> variables;
    bool operator()(is_alive i) { return !std::get<robot*>(variables[i.id])->dead; }
    bool operator()(binary_cond cond) {
        auto a = cond.a;
        auto b = cond.b;
        if (std::holds_alternative<std::string>(cond.a)){
            a = variables[std::get<std::string>(cond.a)];
        }
        if (std::holds_alternative<std::string>(cond.b)){
            b = variables[std::get<std::string>(cond.b)];
        }


    }
    int operator()(binary_op b) {
        if (b.a.index() == 2){
    }
};

struct game{
    std::map<int, std::vector<int>> player_stats;
    std::vector<std::unique_ptr<robot>> robots;
    std::map<std::string, atom> variables;
    std::map<std::string, r_vec> colours;
    stmnt program;

    struct expr_visitor{
        
    } visitor;

    bool eval(if_st i){
        if (std::visit(database, i.condition))
            eval(i.statement);
    }

    bool eval(let_chase l){
    }
    bool eval(do_stmt d){
        for (auto &s : d.s){
            eval(s);
        }
    }
    bool eval(set s) { variables[s.id] = get_expr(s.e); }
    bool eval(let_goto l) { std::get<robot*>(variables[l.id]); }
    bool eval(let_chase l) { std::get<robot*>(variables[l.id1])->chasing = std::get<robot*>(variables[l.id2]); }

    void tick()
    {

        for (auto &robot : robots)
            robot->move();

        for (auto &robot : robots)
            robot->fight_nearby(colours["red"], colours["green"], colours["blue"]);

        for (auto &robot : robots)
            robot->lock_target(colours["red"], colours["green"], colours["blue"]);

        for (auto it = robots.begin(); it != robots.end(); ++it)
        {
            if ((*it)->dead)
            {
                robots.back().swap(*it);
                robots.pop_back();
                --it;
            }
        }
    }

    bool check_moves()
    {
        for (auto &robot : robots)
        {
            if (robot->chasing)
                return true;
        }
        return false;
    }
    std::tuple<double, double, double> get_coords(std::string_view &sv){
        std::vector<double> coords(3);
        for(int i = 0; i < 3; i++){
            sv.remove_prefix(sv.find_first_not_of(' \n')); //remove space
            auto end = sv.find_first_of(' \n');
            coords[i] = stoi(std::string{sv.substr(0, end)});
            sv.remove_prefix(end);
        }
        return {coords[0], coords[1], coords[2]};
    }

    void parse_declaration(std::string_view &sv){
        sv.remove_prefix(4); //with
        sv.remove_prefix(sv.find_first_not_of(' \n')); //space

        while(!sv.starts_with("init")){


            auto pos = sv.find_first_of(' \n');
            auto ident = std::string{sv.substr(0, pos)}; //post ident
            sv.remove_prefix(sv.find_first_not_of(' \n=', pos)); //on next word

            if (sv[0] == '@'){ //coord only

                auto [x, y, z] = get_coords(sv);
                sv.remove_prefix(sv.find_first_not_of(' \n'));

            } else if (std::isdigit(sv[0])){ //num onlhy

                int num = 0;
                auto num_end = sv.find_first_of(' \n');
                std::from_chars(sv.data(), sv.data() + num_end, num);
                sv.remove_prefix(sv.find_first_of('@', num_end));

            } else{ //color, num, coord

                auto end_color = sv.find_first_of(' \n');
                std::string color = std::string{sv.substr(0, end_color)};
                auto num_pos = sv.find_first_not_of(" \n", end_color);
                sv.remove_prefix(num_pos);
                
                int num = 0;
                auto num_end = sv.find_first_of(' \n');
                std::from_chars(sv.data(), sv.data() + num_end, num);
                sv.remove_prefix(sv.find_first_of('@', num_end));
                
                auto [x, y, z] = get_coords(sv);
                sv.remove_prefix(sv.find_first_not_of(' \n'));//go to next
            }
        }
    }

    void parse_init(std::string_view &sv){

    }

    void parse_game(std::string_view &sv){
        parse_declaration(sv);
        parse_init(sv);
        parse_program(sv);
    }

    std::tuple<int, std::vector<int>> run(std::string_view sv)
    {
        parse_game(sv);
        int ticks = 0;

        for (auto &robot : robots)
            robot->lock_target(colours["red"], colours["green"], colours["blue"]);

        for (; check_moves(); ++ticks)
        {
            tick();
        }

        for (auto &robot : robots)
        {
            player_stats[robot->owner][robot->pos()]++;
        }

        std::vector<std::tuple<int, std::vector<int>>> help;
        for (auto &[id, key] : player_stats)
            help.emplace_back(id, key);

        std::sort(help.begin(), help.end(), [](auto &a, auto &z)
                  {
          auto &[id, x] = a;
          auto [r, g, b] = std::tuple<int, int, int>(x[0], x[1], x[2]);
          auto t = r + g + b;
          
          auto [id1, x1] = z;
          auto [r1, g1, b1] = std::tuple<int, int, int>(x1[0], x1[1], x1[2]);
          auto t1 = r1 + g1 + b1;

          return t > t1 || (t == t1 && (r > r1 || (r == r1 && (g > g1 || 
                  (g == g1 && (b > b1 || (b == b1 && id < id1))))))); });

        std::vector<int> res;
        for (auto [id, _] : help)
            res.emplace_back(id);
        return {ticks, res};
    }

    void add_red(std::tuple<double, double, double> pos, int owner)
    {
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_red>(owner, x, y, z));
        colours["red"].emplace_back(robots.back().get());
        player_stats[owner] = {0, 0, 0};
    }
    void add_green(std::tuple<double, double, double> pos, int owner)
    {
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_green>(owner, x, y, z));
        colours["green"].emplace_back(robots.back().get());
        player_stats[owner] = {0, 0, 0};
    }
    void add_blue(std::tuple<double, double, double> pos, int owner)
    {
        auto [x, y, z] = pos;
        robots.emplace_back(std::make_unique<robot_blue>(owner, x, y, z));
        colours["red"].emplace_back(robots.back().get());
        player_stats[owner] = {0, 0, 0};
    }
};

int main()
{
    game g, h;

    auto [ticks, players] = g.run(example_1);
    assert(ticks == 15);
    assert((players == std::vector{1, 2}));

    std::tie(ticks, players) = h.run(example_2);
    assert(ticks == 49);
    assert((players == std::vector{2, 1}));

    return 0;
}
