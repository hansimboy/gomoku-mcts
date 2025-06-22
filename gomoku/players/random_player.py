from .base import GamePlayerInterface
from ..board import GomokuBoard, CellState, GameResult
from typing import Union

class RandomPlayer(GamePlayerInterface):
    def __init__(self):
        # Initialize the player's side to None
        self.side = None
        super().__init__()

    def move(self, GomokuBoard: GomokuBoard) -> Union[GameResult, bool]:
        # Get a random empty spot on the game board
        location = GomokuBoard.random_empty_spot()

        # Make a move on the game board and capture the result and whether the game is finished
        _, res, finished = GomokuBoard.move(int(location), self.side)

        # Return the move's result and whether the game is finished
        return res, finished

    def new_game(self, side: CellState):
        # Set the player's side at the start of a new game
        self.side = side