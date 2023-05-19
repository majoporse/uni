#include <cassert>
#include <algorithm>
#include <memory>
#include <vector>

/* Implementujte množinu libovolných celých čísel, s těmito
 * operacemi:
 *
 *  • sjednocení operátorem ‹|›,
 *  • průnik operátorem ‹&›,
 *  • rozdíl operátorem ‹-›,
 *  • uspořádání inkluzí relačními operátory.
 *
 * Všechny výše uvedené operace musí být nejvýše lineární v součtu
 * velikostí vstupních množin. Typ ‹set› doplňte metodami ‹add›
 * (přidá prvek) a ‹has› (ověří přítomnost prvku), které mají
 * nejvýše logaritmickou složitost. */

struct set_node
{
public:
	int value;
	std::unique_ptr<set_node> left, right;
	
	set_node(int value) : value(value) {}
	
	set_node(const set_node& other) : value(other.value)
	{
		if (other.left)
		{
			left = std::make_unique<set_node>(*other.left);
		}
		
		if (other.right)
		{
			right = std::make_unique<set_node>(*other.right);
		}
	}
	
	set_node(std::vector<int>& subtree, std::size_t size)
	{
		assert(!subtree.empty());
		
		// this constructor constructs subtree from values in given vector,
		// it takes last 'size' amount of elements
		std::size_t left_size = size / 2,
					right_size = size - left_size - 1; //-1 counts for value in this node
		
		if (right_size > 0) // recursively make the right subtree
		{
			right = std::make_unique<set_node>(subtree, right_size);
		}
		
		assert(!subtree.empty());
		// making of current node
		value = subtree.back();
		subtree.pop_back();
		
		if (left_size > 0) // recursively make the left subtree
		{
			left = std::make_unique<set_node>(subtree, left_size);
		}
	}
	
	~set_node() = default;
	
	void make_left(int left_value)
	{
		assert(left == nullptr);
		left = std::make_unique<set_node>(left_value);
	}
	
	void make_right(int right_value)
	{
		assert(right == nullptr);
		right = std::make_unique<set_node>(right_value);
	}

	void recursive_copy(std::vector<int>& v) const
	{
		// infix recursive copy values of this subtree into given vector
		if (left)
		{
			left->recursive_copy(v);
		}
		
		v.push_back(value);
		
		if (right)
		{
			right->recursive_copy(v);
		}
	}
};

struct set
{
	std::unique_ptr<set_node> root;
	
	std::vector<int> contents() const
	{
		// returns vector of all keys stored in ascending order
		std::vector<int> result;
		
		if (!empty())
		{
			root->recursive_copy(result);
		}
		
		return result;
	}
	
public:
	set() = default;
	
	set(const set& other)
	{
		if (other.empty())
		{
			return;
		}
		
		root = std::make_unique<set_node>(*other.root);
	}
	
	set(std::vector<int>& elements)
	{
		// creates set from given vector of keys, assumes that it is sorted
		// works in linear time
		if (elements.empty())
		{
			return;
		}
		
		root = std::make_unique<set_node>(elements, elements.size());
	}
	
	~set() = default;

	bool empty() const { return root == nullptr; }

	void add(int value)
	{
		//typical binary search inserting
		set_node *current = root.get(), *prev = nullptr;
		
		while (current)
		{
			prev = current;
			
			if (value < current->value)
			{
				current = current->left.get();
			}
			else if (value > current->value)
			{
				current = current->right.get();
			}
			else
			{
				// the inserted value is already in the tree
				return;
			}
		}
		
		if (!prev) // tree is empty
		{
			root = std::make_unique<set_node>(value);
			return;
		}
		
		if (value < prev->value)
		{
			prev->make_left(value);
		}
		else
		{
			prev->make_right(value);
		}
	}
	
	bool has(int value) const
	{
		// typical binary search find
		const set_node *current = root.get();
		
		while (current)
		{
			if (value < current->value)
			{
				current = current->left.get();
			}
			else if (value > current->value)
			{
				current = current->right.get();
			}
			else
			{
				return true;
			}
		}
		
		return false;
	}

	friend set operator|(const set& s1, const set& s2)
	{
		std::vector<int> s1_content = s1.contents(), s2_content = s2.contents();
		std::vector<int> result;
		
		std::set_union(s1_content.begin(), s1_content.end(),
					   s2_content.begin(), s2_content.end(),
					   std::back_inserter(result));
		
		return { result };
	}
	
	friend set operator&(const set& s1, const set& s2)
	{
		std::vector<int> s1_content = s1.contents(), s2_content = s2.contents();
		std::vector<int> result;
		
		std::set_intersection(s1_content.begin(), s1_content.end(),
							  s2_content.begin(), s2_content.end(),
							  std::back_inserter(result));

		return { result };
	}
	
	friend set operator-(const set& s1, const set& s2)
	{
		std::vector<int> s1_content = s1.contents(), s2_content = s2.contents();
		std::vector<int> result;
		
		std::set_difference(s1_content.begin(), s1_content.end(),
							s2_content.begin(), s2_content.end(),
							std::back_inserter(result));
		
		return { result };
	}
	
	friend bool operator==(const set& s1, const set& s2)
	{
		return s1.contents() == s2.contents();
	}
	
	friend bool operator<(const set& s1, const set& s2)
	{
		return (s1 - s2).empty() && s1 != s2;
	}
	
	friend bool operator<=(const set& s1, const set& s2)
	{
		return (s1 - s2).empty();
	}
	
	friend bool operator>(const set& s1, const set& s2)
	{
		return s2 < s1;
	}
	
	friend bool operator>=(const set& s1, const set& s2)
	{
		return s2 <= s1;
	}
};


int main()
{
    set a, b;
    a.add( 1 ), a.add( 2 ), a.add( 5 ), a.add( -3 );
    b.add( 1 ), b.add( -3 ), b.add( -1000 ), b.add( 1 << 20 );

    const set x = a, y = b;

    const set u = x | y;
    const set i = x & y;
    const set d = x - y;
    
    assert(  u.has( 1 ) );
    assert(  i.has( 1 ) );
    assert( !d.has( 1 ) );

    assert(  u.has( 2 ) );
    assert( !i.has( 2 ) );
    assert(  d.has( 2 ) );
    assert( !i.has( -1000 ) );
    assert(  u.has( -1000 ) );
    assert( !d.has( -1000 ) );
    assert(  u.has( 1 << 20 ) );
    assert( !i.has( 1 << 20 ) );

    assert( !( a <= b ) );
    assert( !( b <= a ) );
    assert( a <= u );
    assert( u >  a );
    assert( b <= u );
    assert( i <= u );
    assert( i <  u );
    assert( i <= a );
    assert( i <= b );
    assert( u <= u );
    assert( u == u );
    assert( d <= u );
    assert( d <= a );
    assert( !( d <= b ) );

    return 0;
}
