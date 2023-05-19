#include <vector>
#include <string>
#include <cassert>
#include <sstream>
#include <iostream>
#include <string>
#include <map>
#include <charconv>

/* Write a simple parser for an assembly-like language with one
 * instruction per line (each taking 2 operands, separated by
 * spaces, where the first is always a register and the second is
 * either a register or an ‘immediate’ number).
 *
 * The opcodes (instructions) are: ‹add›, ‹mul›, ‹jnz›, the
 * registers are ‹rax›, ‹rbx› and ‹rcx›. The result is a vector of
 * ‹instruction› instances (see below). Set ‹r_2› to
 * ‹reg::immediate› if the second operand is a number.
 *
 * If the input does not conform to the expected format, throw
 * ‹no_parse›, which includes a line number with the first erroneous
 * instruction and the kind of error (see ‹enum error›), as public
 * attributes ‹line› and ‹type›, respectively. If multiple errors
 * appear on the same line, give the one that comes first in the
 * definition of ‹error›. You can add attributes or methods to the
 * structures below, but do not change the enumerations. */

enum class opcode { add, mul, jnz };
enum class reg { rax, rbx, rcx, immediate };
enum class error { bad_opcode, bad_register, bad_immediate,
                   bad_structure };

struct instruction
{
    opcode op;
    reg r_1, r_2;
    int32_t immediate;
};

struct no_parse
{
    int line;
    error type;
};
std::map<std::string, opcode> opcodes = { {"add", opcode::add},
                                          {"mul", opcode::mul},
                                          {"jnz", opcode::jnz} };

std::map<std::string, reg> registers = { {"rax", reg::rax},
                                         {"rbx", reg::rbx},
                                         {"rcx", reg::rcx} };

std::vector< instruction > parse( const std::string &s){
    std::stringstream ss(s);
    std::string line;
    std::vector<instruction> res;
    for (int i = 1; std::getline(ss, line); ++i){
        std::string a, b, c;
        std::stringstream l(line);
        l >> a >> b >> c;

        auto &ins = res.emplace_back();
        if (!opcodes.contains(a))
            throw no_parse{ i, error::bad_opcode };

        ins.op = opcodes[a];
        if (!registers.contains(b))
            throw no_parse{ i, error::bad_register };

        ins.r_1 = registers[b];
        if (isdigit(c[0])){
            if (int dummy = 0; std::from_chars(c.data(), c.data() + c.size(), dummy).ptr == c.data() + c.size())
                ins.r_2 = reg::immediate;
            else
                throw no_parse{ i, error::bad_immediate };

        } else if (registers.contains(c))
            ins.r_2 = registers[c];
        else
            throw  no_parse{ i, error::bad_register };

        if (l.peek() != EOF)
            throw no_parse{ i, error::bad_structure };
    }
     
    return res;
}

#include <iostream>

int main()
{
    auto p_1 = parse( "add rax 7\n"
                      "mul rax  rbx\n" );
    assert( p_1[ 0 ].op  == opcode::add );
    assert( p_1[ 0 ].r_1 == reg::rax );
    assert( p_1[ 0 ].r_2 == reg::immediate );
    assert( p_1[ 1 ].op  == opcode::mul );
    assert( p_1[ 1 ].r_2 == reg::rbx );

    try
    {
        parse( "add rax 7\n"
               "mul rax  rbx\n"
               "mul rax rrx\n" );
        assert( false );
    }
    catch ( const no_parse &np )
    {
        assert( np.line == 3 );
        assert( np.type == error::bad_register );
    }

    try
    {
        parse( "add rax 7\n"
               "mul rax rax rbx\n"
               "mul rax rrx\n" );
        assert( false );
    }
    catch ( const no_parse &np )
    {
        assert( np.line == 2 );
        assert( np.type == error::bad_structure );
    }

    try
    {
        parse( "add rax 7z\n" );
        assert( false );
    }
    catch ( const no_parse &np )
    {
        assert( np.line == 1 );
        assert( np.type == error::bad_immediate );
    }

    try
    {
        parse( "add rax 7\n"
               "hlt rax 7z\n"
               "add rax rox\n" );
        assert( false );
    }
    catch ( const no_parse &np )
    {
        assert( np.line == 2 );
        assert( np.type == error::bad_opcode );
    }

    try
    {
        parse( "add 7 rax\n" );
        assert( false );
    }
    catch ( const no_parse &np )
    {
        assert( np.line == 1 );
        assert( np.type == error::bad_register );
    }

    return 0;
}
