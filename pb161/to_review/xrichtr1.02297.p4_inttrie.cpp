#include <cassert>
#include <memory>
#include <vector>

/* V tomto cvičení rozšíříme binární trie z ‹p2› – místo
 * posloupnosti bitů budeme za klíče brát posloupnosti celých čísel
 * typu ‹int›. Vylepšíme také rozhraní – místo ruční správy uzlů
 * poskytneme přímo operaci vložení zadaného klíče.
 *
 * Množiny budeme nadále kódovat do binárního stromu:
 *
 *  • levý potomek uzlu rozšiřuje reprezentovaný klíč o jedno celé
 *    číslo (podobně jako tomu bylo u binární trie) – toto číslo je
 *    tedy součástí levé hrany,
 *  • pravý „potomek“ uzlu je ve skutečnosti jeho sourozenec, a
 *    hrana není nijak označená (přechodem doprava se klíč nemění),
 *  • řetěz pravých potomků tvoří de-facto zřetězený seznam, který
 *    budeme udržovat seřazený podle hodnot na odpovídajících
 *    «levých» hranách.
 *
 *
 * Příklad: na obrázku je znázorněná trie s klíči [3, 1], [3, 13,
 * 7], [3, 15], [5, 2], [5, 5], [37]. Levý potomek je pod svým
 * rodičem, pravý je od něj napravo.
 *
 *   ●────────────────▶●─────────────▶●
 *   │                 │              │
 *   │ 3               │ 5            │ 37
 *   ▼                 ▼              ▼
 *   ●────▶●────▶●     ●─────▶●       ●
 *   │     │     │     │      │
 *   │ 1   │ 13  │ 15  │ 2    │ 5
 *   ▼     ▼     ▼     ▼      ▼
 *   ●     ●     ●     ●      ●
 *         │
 *         │ 7
 *         ▼
 *         ●
 *
 * Můžete si představit takto reprezentovanou trie jako ⟦2³²⟧-ární,
 * které by bylo zcela jistě nepraktické přímo implementovat. Proto
 * reprezentujeme virtuální uzly pomyslného ⟦2³²⟧-árního stromu jako
 * zřetězené seznamy pravých potomků ve fyzicky binárním stromě. */

using key = std::vector<int>;
struct trie_node
{
	std::unique_ptr<trie_node> left, right;
	int value; // values are relevant only for left offsprings

	trie_node() = default;

	trie_node(int value) : value(value) {}

	bool is_leaf() const
	{
		return left == nullptr;
	}
};

/* Rozhraní typu ‹trie› je velmi jednoduché: má metodu ‹add›, která
 * přidá klíč a metodu ‹has›, která rozhodne, je-li daný klíč
 * přítomen. Obě jako parametr přijmou hodnotu typu ‹key›. Prefixy
 * vložených klíčů nepovažujeme za přítomné. */

struct trie
{
	trie_node root;
	
	void add(const key& k)
	{
		trie_node* current = &root;
		
		for (int value : k)
		{
			// loop until we find node containing value to traverse down,
			// or until we know that there is none (left is nullptr)
			while (current->left != nullptr && current->left->value != value)
			{
				if (current->right == nullptr)
				{
					current->right = std::make_unique<trie_node>();
				}
				
				current = current->right.get();
			}
			
			// here we know that current->left is either nullptr or contains wanted value
			if (current->left == nullptr) // create the node if there's none
			{
				current->left = std::make_unique<trie_node>(value);
			}
			
			current = current->left.get();
		}
	}
	
	bool has(const key& k) const
	{
		// implicitly returns true for empty keys
		const trie_node* current = &root;
		
		for (int value : k)
		{
			// loop until we find node containing wanted value to traverse down
			// skips over nodes with nullptr left offsprings
			while (current->left == nullptr || current->left->value != value)
			{
				if (current->right == nullptr)
				{
					// we didn't find correct descending node and there's no
					// sibling to traverse to
					return false;
				}
				
				current = current->right.get();
			}
			
			// here we know that current->left isn't nullptr and contains wanted value
			current = current->left.get();
		}
		
		return current->is_leaf();
	}
};

int main()
{
    trie t;
    const trie &ct = t;
    assert( !ct.has( { 1 } ) );

    t.add( { 1 } );
    assert(  t.has( { 1 } ) );
    assert( !t.has( { 1, 1 } ) );

    /* { 1 } disappears from the trie, since it is a prefix of { 1, 1 } */

    t.add( { 1, 1 } );
    assert(  t.has( { 1, 1 } ) );
    assert( !t.has( { 1 } ) );

    /* add a right sibling to a non-root node */

    t.add( { 1, 2 } );
    assert(  t.has( { 1, 1 } ) );
    assert(  t.has( { 1, 2 } ) );
    assert( !t.has( { 2, 2 } ) );
    assert( !t.has( { 2, 1 } ) );

    /* add a right sibling to the root node */

    t.add( { 2, 1 } );
    assert(  t.has( { 1, 1 } ) );
    assert(  t.has( { 2, 1 } ) );
    assert(  t.has( { 1, 2 } ) );
    assert( !t.has( { 2, 2 } ) );

    /* add a left sibling to a non-root node */

    t.add( { 2, 0, 1 } );
    assert(  t.has( { 1, 1 } ) );
    assert(  t.has( { 2, 0, 1 } ) );
    assert(  t.has( { 2, 1 } ) );
    assert(  t.has( { 1, 2 } ) );

    /* add a left sibling to the root node */

    t.add( { 0, 1 } );
    assert(  t.has( { 1, 1 } ) );
    assert(  t.has( { 2, 1 } ) );
    assert(  t.has( { 1, 2 } ) );
    assert(  t.has( { 0, 1 } ) );
    assert(  t.has( { 2, 0, 1 } ) );

    return 0;
}
