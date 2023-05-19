#include <iostream>
#include <cassert>
#include "b_chess.cpp" // replace with the name of your source file
#include <iostream>
void print(const chess& c) {
    std::cout << "\n  @-------------------------------@\n"; ;
    for(int rank = 8 ; rank >= 1; --rank){
        std::cout << rank << " |";
        for(int file = 1 ; file <= 8; ++file){
            auto p = c.at({file, rank});
            if (!p) { std::cout << "   |"; continue; }

            if (p->owner == player::white) { 
                std::cout << " ";
                if(p->type == piece_type::pawn) std::cout << "♙ ";
                if(p->type == piece_type::rook) std::cout << "♖ ";
                if(p->type == piece_type::knight) std::cout << "♘ ";
                if(p->type == piece_type::bishop) std::cout << "♗ ";
                if(p->type == piece_type::king) std::cout << "♔ ";
                if(p->type == piece_type::queen) std::cout << "♕ ";
            }
            else {
                std::cout << " ";
                if(p->type == piece_type::pawn) std::cout << "♟︎ ";
                if(p->type == piece_type::rook) std::cout << "♜ ";
                if(p->type == piece_type::knight) std::cout << "♞ ";
                if(p->type == piece_type::bishop) std::cout << "♝ ";
                if(p->type == piece_type::king) std::cout << "♚ ";
                if(p->type == piece_type::queen) std::cout << "♛ ";
            }

            std::cout << "|";
            
        }
        std::cout  << "\n";
        std::cout  << (rank > 1 ? "  |---+---+---+---+---+---+---+---|\n" : "  @---+---+---+---+---+---+---+---@\n");
    }
    std::cout << "    1   2   3   4   5   6   7   8  \n\n\n";
}

int main() {


    // test initialization of the chess board
    chess c{};
    // assert(c.board.size() == 32);
    // assert((c.board.find(position{1, 1})->second->type == piece_type::rook));
    // // assert(c.board.find(position{2, 5})->second == std::nullopt);
    // print(c);

    // test a valid pawn move
    auto res = c.play({2, 2}, {2, 4});
    assert(res == result::ok);
    // assert(c.board.find(position{2, 4})->second->type == piece_type::pawn);
    // assert(c.turn_player == player::black);
    print(c);

    // test an invalid move (no piece at the starting position)
    res = c.play({2, 3}, {2, 4});
    assert(res == result::no_piece);
    // assert(c.turn_player == player::black);
    print(c);

    // test an invalid move (wrong player tries to move)
    res = c.play({2, 4}, {2, 5});
    assert(res == result::bad_piece);
    // assert(c.turn_player == player::black);
    print(c);

    // test a valid capture move
    res = c.play({3, 7}, {3, 5});
    print(c);
    assert(res == result::ok);
    res = c.play({2, 4}, {3, 5});
    print(c);
    assert(res == result::capture);
    // assert(c.board.find(position{3, 5})->second->type == piece_type::pawn);
    // assert(c.turn_player == player::black);
    print(c);

    res = c.play({2, 8}, {3, 6});
    assert(res == result::ok);
    // assert(c.turn_player == player::white);
    print(c);


    // test an invalid move (piece cannot move that way)
    res = c.play({3, 2}, {3, 5});
    assert(res == result::bad_move);
    // assert(c.turn_player == player::white);
    print(c);

    // test an invalid move 
    res = c.play({1, 1}, {1, 5});
    assert(res == result::blocked);
    // assert(c.turn_player == player::white);

    // test an invalid move (cant capture own piece)
    res = c.play({2, 1}, {4, 2});
    assert(res == result::blocked);
    // assert(c.turn_player == player::white);

    // test an invalid move (pawn cannot capture forward)
    res = c.play({3, 5}, {3, 6});
    assert(res == result::blocked);
    // assert(c.turn_player == player::white);
    
    assert(c.play({5, 2}, {5, 4}) == result::ok); print(c);
    assert(c.play({4, 7}, {4, 5}) == result::ok); print(c);
    assert(c.play({3, 5}, {4, 6}) == result::capture); print(c);
    assert(c.play({6, 7}, {6, 5}) == result::ok); print(c);
    assert(c.play({4, 6}, {4, 7}) == result::ok); print(c);
    assert(c.play({6, 5}, {6, 4}) == result::in_check); print(c);
    assert(c.play({5, 8}, {6,8}) == result::blocked); print(c);
    assert(c.play({5, 8}, {6, 7}) == result::ok); print(c);
    assert(c.play({4, 7}, {4, 8}) == result::blocked); print(c);
    assert(c.play({4, 7}, {5, 8}) == result::bad_move); print(c);
    assert(c.play({4, 7}, {3, 8}) == result::bad_promote); print(c);
    assert(c.play({4, 7}, {3, 8}, piece_type::queen) == result::capture); print(c);
    assert(c.play({6, 7}, {5, 6}) == result::would_check); print(c);
    assert(c.play({6, 5}, {6, 4}) == result::ok); print(c);
    assert(c.play({3, 8}, {4, 8}) == result::capture); print(c);
    assert(c.play({6, 4}, {5, 3}) == result::lapsed); print(c);
    assert(c.play({7, 8}, {6, 6}) == result::ok); print(c);
    assert(c.play({7, 2}, {7, 4}) == result::ok); print(c);
    assert(c.play({6, 4}, {7, 3}) == result::capture); print(c);
    assert(c.play({6, 2}, {6, 3}) == result::ok); print(c);
    assert(c.play({6, 6}, {5, 4}) == result::capture); print(c);
    assert(c.play({6, 3}, {5, 4}) == result::capture); print(c);
    assert(c.play({5, 1}, {5, 4}) == result::bad_piece); print(c);
    assert(c.play({1, 7}, {1, 6}) == result::ok); print(c);
    assert(c.play({5, 1}, {5, 4}) == result::bad_move); print(c);
    assert(c.play({5, 1}, {4, 1}) == result::blocked); print(c);
    assert(c.play({5, 1}, {6, 2}) == result::would_check); print(c);
    assert(c.play({5, 1}, {5, 2}) == result::ok); print(c);
    
    {
        chess c{};
        // assert a2 == position( 1, 2 )
        assert (c.play( {1, 2}, {1,4} ) == result::ok)  ;
        assert (c.play( {4, 7}, {4, 5} ) == result::ok) ;
        assert (c.play( {1, 1}, {1,3} ) == result::ok)  ;
        assert (c.play( {3,8}, {8,3} ) == result::ok)   ;
        // eval/b_blocked.t.cpp:17: c.play( c8, h3 ) == result::ok
        // c.play( c8, h3 ) = blocked
        // result::ok       = ok 
    }

    {
        chess c{};
        assert(c.play( {7,2}, {7,3} ) == result::ok); print(c);
        assert(c.play( {1,7}, {1,6} ) == result::ok); print(c);
        assert(c.play( {6,1}, {8,3} ) == result::ok); print(c);
        assert(c.play( {2,7}, {2,6} ) == result::ok); print(c);
        assert(c.play( {5,1}, {7,1} ) == result::blocked); print(c);
        assert(c.play( {5,1}, {8,1} ) == result::bad_move); print(c);
        assert(c.play( {7,1}, {6,3} ) == result::ok); print(c);
        assert(c.play( {3,7}, {3,6} ) == result::ok); print(c);
        assert(c.play( {5,1}, {7,1} ) == result::ok); print(c);
        // assert(c.play( {4,7}, {4,6} ) == result::ok); print(c);
        // assert(c.play( {7,7}, {7,6} ) == result::ok); print(c);
    }


    {
        chess c{};
        assert( c.play( { 1, 2 }, { 1, 4} ) == result::ok); print(c);
        assert( c.play( { 4, 7 }, { 4, 5} ) == result::ok); print(c);
        assert( c.play( { 1, 1 }, { 1, 3} ) == result::ok); print(c);
        assert( c.play( { 3, 8 }, { 8, 3} ) == result::ok); print(c);
        assert( c.play( { 7, 1 }, { 6, 3} ) == result::ok); print(c);
        assert( c.play( { 4, 8 }, { 4, 6} ) == result::ok); print(c);
        assert( c.play( { 1, 3 }, { 4, 3} ) == result::ok); print(c);
        assert( c.play( { 5, 8 }, { 4, 8} ) == result::ok); print(c);
        assert( c.play( { 4, 3 }, { 5, 4} ) == result::bad_move); print(c);
        assert( c.play( { 4, 3 }, { 5, 5} ) == result::bad_move); print(c);
        assert( c.play( { 1, 4 }, { 1, 6} ) == result::bad_move); print(c);
    }

    {
        chess c{};
        assert( c.play( {7,2}, {7,3} ) == result::ok ); print(c);
        assert( c.play( {7,7}, {7,6} ) == result::ok ); print(c);
        assert( c.play( {6,1}, {8,3} ) == result::ok ); print(c);
        assert( c.play( {7,8}, {6,6} ) == result::ok ); print(c);
        assert( c.play( {7,1}, {6,3} ) == result::ok ); print(c);
        assert( c.play( {6,8}, {8,6} ) == result::ok ); print(c);
        assert( c.play( {8,1}, {7,1} ) == result::ok ); print(c);
        assert( c.play( {5,7}, {5,6} ) == result::ok ); print(c);
        assert( c.play( {7,1}, {8,1} ) == result::ok ); print(c);
        assert( c.play( {6,6}, {8,5} ) == result::ok ); print(c);
        assert( c.play( {5,1}, {7,1} ) == result::has_moved ); print(c);
    }
    std::cout << "All tests passed!\n";

    return 0;
}