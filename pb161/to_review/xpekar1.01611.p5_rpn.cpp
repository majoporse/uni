#include <cassert>
#include <cmath>
#include <stack>

/* Naprogramujte jednoduchý zásobníkový evaluátor aritmetických
 * výrazů zapsaných v RPN (postfixové notaci). Operace:
 *
 *  • ‹push› vloží na vrch pracovního zásobníku konstantu,
 *  • ‹apply› přijme hodnotu jednoho ze tří níže definovaných typů,
 *    které reprezentují operace a příslušnou operaci provede,
 *  • metoda ‹top› poskytne přístup k aktuálnímu vrcholu pracovního
 *    zásobníku, včetně možnosti změnit jeho hodnotu,
 *  • ‹pop› odstraní jednu hodnotu z vrcholu zásobníku a vrátí ji,
 *  • ‹empty› vrátí ‹true› je-li pracovní zásobník prázdný.
 *
 * Podobně jako v příkladu ‹distance› zařiďte, aby bylo možné metody
 * ‹push› a ‹apply› libovolně řetězit. Všechny tři operace uvažujeme
 * jako binární. */

struct add
{
    int operator()(int x, int y) const
    {
        return x + y;
    }
}; /* addition */
struct mul
{
    int operator()(int x, int y) const
    {
        return x * y;
    }
}; /* multiplication */
struct dist
{
    int operator()(int x, int y) const
    {
        return std::abs(x - y);
    }
}; /* absolute value of difference */

struct eval
{
    std::stack<int> stack;

    eval &push(int x)
    {
        stack.push(x);
        return *this;
    }

    eval &apply(const auto &operation)
    {
        if (stack.size() < 2) {
            return *this;
        }
        push(operation(pop(), pop()));
        return *this;
    }

    int top() const
    {
        return stack.top();
    }

    int &top()
    {
        return stack.top();
    }

    int pop()
    {
        int x = top();
        stack.pop();
        return x;
    }

    bool empty() const
    {
        return stack.empty();
    }
};

int main()
{
    eval e;
    const eval &f = e;

    e.push(7).push(3).apply(add());
    assert(f.top() == 10);
    assert(e.push(1).apply(mul()).top() == 10);
    assert(e.pop() == 10);
    assert(f.empty());
    e.push(10);
    e.top() = 11;
    assert(f.top() == 11);
    e.push(10).apply(dist());
    assert(f.top() == 1);
    assert(!f.empty());
    assert(e.pop() == 1);
    assert(f.empty());

    return 0;
}
