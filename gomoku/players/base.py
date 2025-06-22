from abc import ABC, abstractmethod
from typing import Tuple
from ..board import GomokuBoard, CellState, GameResult

class GamePlayerInterface(ABC):
    """
    Interface for Gomoku player
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    def move(self, board: GomokuBoard) -> Tuple[GameResult, bool]:
        pass

    @abstractmethod
    def new_game(self, side: CellState):
        pass