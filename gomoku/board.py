from enum import Enum
import numpy as np
from typing import Tuple, Union

from .constants import BOARD_DIM, BOARD_SIZE, NUM_WIN

class CellState(Enum):
  EMPTY = 0  # type: int
  NAUGHT = 1  # type: int
  CROSS = 2  # type: int

class GameResult(Enum):
  """
  Enum to encode different states of the game. A game can be in progress (NOT_FINISHED), lost, won, or draw
  """
  NOT_FINISHED = 0
  NAUGHT_WIN = 1
  CROSS_WIN = 2
  DRAW = 3

class GomokuBoard:
    """
    The class to encode a gomoku board, including its current state of pieces.
    Also contains various utility methods.
    """

    WIN_CHECK_DIRS = [[(-1, 0), (1, 0)],
                      [(0, -1), (0, 1)],
                      [(-1, 1), (1, -1)],
                      [(-1, -1), (1, 1)]]

    def hash_value(self) -> int:
        """
        Encode the current state of the game (board positions) as an integer. Will be used for caching evaluations
        :return: A collision free hash value representing the current board state
        """
        res = 0
        for i in range(BOARD_SIZE):
            res *= BOARD_DIM
            res += self.state[i].value

        return res

    @staticmethod
    def other_side(side: CellState) -> CellState:
        """
        Utility method to return the value of the other player than the one passed as input
        :param side: The side we want to know the opposite of
        :return: The opposite side to the one passed as input
        """
        if side == CellState.EMPTY:
            raise ValueError("EMPTY has no 'other side'")

        if side == CellState.CROSS:
            return CellState.NAUGHT

        if side == CellState.NAUGHT:
            return CellState.CROSS

        raise ValueError("{} is not a valid side".format(side))

    def __init__(self):
        """
        Create a new Board. If a state is passed in, we use that otherwise we initialize with an empty board
        :param s: Optional board state to initialise the board with
        """
        self.state = np.ndarray(shape=(BOARD_SIZE,), dtype=CellState)
        self.reset()

    def coord_to_pos(self, coord: Tuple[int, int]) -> int:
        """
        Converts a 2D board position to a 1D board position.
        Various parts of code prefer one over the other.
        :param coord: A board position in 2D coordinates
        :return: The same board position in 1D coordinates
        """
        return coord[0] * BOARD_DIM + coord[1]

    def pos_to_coord(self, pos: int) -> Tuple[int, int]:
        """
        Converts a 1D board position to a 2D board position.
        Various parts of code prefer one over the other.
        :param pos: A board position in 1D coordinates
        :return: The same board position in 2D coordinates
        """
        return pos // BOARD_DIM, pos % BOARD_DIM

    def reset(self):
        """
        Resets the game board. All fields are set to be EMPTY.
        """
        self.state.fill(CellState.EMPTY)
        self.who_won = None

    def num_empty(self) -> int:
        """
        Counts and returns the number of empty fields on the board.
        :return: The number of empty fields on the board
        """
        return np.count_nonzero(self.state == CellState.EMPTY)

    def random_empty_spot(self) -> int:
        """
        Returns a random empty spot on the board in 1D coordinates
        :return: A random empty spot on the board in 1D coordinates
        """
        index = np.random.randint(self.num_empty()) # Count all empty spot and random selection among them
        for i in range(BOARD_SIZE):
            if self.state[i] == CellState.EMPTY:
                if index == 0: # if index is zero, then, it means this spot is selected
                    return i
                else:
                    index = index - 1 # if index is not zero, then, it means we have to move next emtpy spot

    def is_legal(self, pos: int) -> bool:
        """
        Tests whether a board position can be played, i.e. is currently empty
        :param pos: The board position in 1D that is to be checked
        :return: Whether the position can be played
        """
        return (0 <= pos < BOARD_SIZE) and (self.state[pos] == CellState.EMPTY)

    def move(self, position: int, side: CellState) -> Union[np.ndarray, GameResult, bool]:
        """
        Places a piece of side "side" at position "position". The position is to be provided as 1D.
        Throws a ValueError if the position is not EMPTY
        returns the new state of the board, the game result after this move, and whether this move has finished the game

        :param position: The position where we want to put a piece
        :param side: What piece we want to play (NAUGHT, or CROSS)
        :return: The game state after the move, The game result after the move, Whether the move finished the game
        """
        if self.state[position] != CellState.EMPTY:
            print('Illegal move')
            raise ValueError("Invalid move")

        self.state[position] = side

        if self.check_win(position, side):
            self.who_won = side
            return self.state, GameResult.CROSS_WIN if side == CellState.CROSS else GameResult.NAUGHT_WIN, True

        if self.num_empty() == 0:
            self.who_won = CellState.EMPTY
            return self.state, GameResult.DRAW, True

        return self.state, GameResult.NOT_FINISHED, False

    def check_win(self, pos: int, side: CellState):
        row = pos // BOARD_DIM
        col = pos % BOARD_DIM

        def check_direction(_dr, _dc):
            count = 0
            r, c = row + _dr, col + _dc
            p = r * BOARD_DIM + c
            while 0 <= r < BOARD_DIM and 0 <= c < BOARD_DIM and self.state[p] == side:
                count += 1
                r += _dr
                c += _dc
                p = r * BOARD_DIM + c
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for dr, dc in directions:
            total_count = 1  # Count the current stone
            total_count += check_direction(-dr, -dc)  # Count stones in the opposite direction
            total_count += check_direction(dr, dc)    # Count stones in the original direction

            if total_count >= NUM_WIN:
                return True

        return False

    def state_to_char(self, pos):
        """
        Return 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' ' to enforce a white space in the case of HTML output
        :param pos: The position in 1D for which we want a character representation
        :param html: Flag indicating whether we want an ASCII (False) or HTML (True) character
        :return: 'x', 'o', or ' ' depending on what piece is on 1D position pos. Ig `html` is True,
        return '&ensp' instead of ' '
        """
        if (self.state[pos]) == CellState.NAUGHT:
            return 'O'
        elif (self.state[pos]) == CellState.CROSS:
            return 'X'