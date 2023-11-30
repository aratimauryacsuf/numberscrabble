from games import *


class Number_Scrabble(Game):
    """Play TicTacToe on an h x v board, with Max (first player) playing 'X'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a dict of {(x, y): Player} entries, where Player is 'X' or 'O'."""

    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        moves = [
            (x, y, z)
            for x in range(1, h + 1)
            for y in range(1, v + 1)
            for z in range(1, 10)
        ]
        self.initial = GameState(to_move="X", utility=0, board={}, moves=moves)

    def actions(self, state):
        """Legal moves are any square not yet taken."""
        return state.moves

    def result(self, state, move):
        if move not in state.moves:
            return state  # Illegal move has no effect
        board = state.board.copy()
        [x1, y1, num1] = move
        board[(x1, y1)] = num1
        moves = []
        for new_move in state.moves:
            [x2, y2, num2] = new_move
            # remove all moves that take up the spot on the board.
            if x1 == x2 and y1 == y2:
                continue
            # remove all moves that have the number placed on the board.
            if num1 == num2:
                continue
            moves.append(new_move)
        return GameState(
            to_move=("O" if state.to_move == "X" else "X"),
            utility=self.compute_utility(board, move, state.to_move),
            board=board,
            moves=moves,
        )

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == "X" else -state.utility

    def terminal_test(self, state):
        """A state is terminal if it is won or there are no empty squares."""
        return state.utility != 0 or len(state.moves) == 0

    def display(self, state):
        board = state.board
        for x in range(1, self.h + 1):
            for y in range(1, self.v + 1):
                print(board.get((x, y), "."), end=" ")
            print()

    def compute_utility(self, board, move, player):
        """If 'X' wins with this move, return 1; if 'O' wins return -1; else return 0."""
        if (
            self.k_in_row(board, move, player, (0, 1))
            or self.k_in_row(board, move, player, (1, 0))
            or self.k_in_row(board, move, player, (1, -1))
            or self.k_in_row(board, move, player, (1, 1))
        ):
            return +1 if player == "X" else -1
        else:
            return 0

    def k_in_row(self, board, move, player, delta_x_y):
        """Return true if there is a line through move on board for player."""
        (delta_x, delta_y) = delta_x_y
        x, y, num1 = move
        n = 0  # n is number of moves in row
        total = 0
        # check forward from move
        while board.get((x, y)):
            n += 1
            total += board[(x, y)]
            x, y = x + delta_x, y + delta_y
        x, y, num1 = move
        # check backwards from move
        while board.get((x, y)):
            n += 1
            total += board[(x, y)]
            x, y = x - delta_x, y - delta_y
        n -= 1  # Because we counted move itself twice
        x, y , num1= move
        total -= board.get((x, y))
        return n >= self.k and total == 15


if __name__ == "__main__":
    scrabble = Number_Scrabble()  # Creating the game instance
    # nim = GameOfNim(board=[7, 5, 3, 1]) # a much larger tree to search
    # print(nim.initial.board) # must be [0, 5, 3, 1]
    # print(nim.initial.moves) # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    # print(nim.result(nim.initial, (1,3) ))
    utility = scrabble.play_game(alpha_beta_player, query_player)  # computer moves first
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
