from .base import GamePlayerInterface
from ..board import GomokuBoard, CellState, GameResult
from typing import Union
import networkx as nx
import numpy as np
import copy
import random

from ..constants import BOARD_DIM, BOARD_SIZE, NUM_WIN
    
class MCTSAlgorithm(GamePlayerInterface):

    iteration = 600

    WIN_VALUE = 1
    DRAW_VALUE = 0
    LOSS_VALUE = -1

    def __init__(self):
        self.side = None
        self.tree = nx.DiGraph()
        super().__init__()

    def new_game(self, side: CellState):
        self.side = side
        self.tree.clear()

    def ucb_score(self, parent_visits, child_value, child_visits, c=1.41):
      if child_visits == 0:
        return float('inf')

      exploit = child_value / child_visits
      explore = c * np.sqrt(np.log(parent_visits) / child_visits)

      return exploit + explore

    def is_fully_expanded(self, board: GomokuBoard) -> bool:
      node = board.hash_value()
      legal_moves = [pos for pos in range(BOARD_SIZE) if board.is_legal(pos)]
      child_nodes = list(self.tree.successors(node))

      expanded_hashes = set(child_nodes)

      for move in legal_moves:
        temp_board = copy.deepcopy(board)
        temp_board.move(move, self.current_player(board))
        child_hash = temp_board.hash_value()

        if child_hash not in expanded_hashes:
          return False

      return True

    def current_player(self, board: GomokuBoard) -> CellState:
      num_cross = sum(1 for cell in board.state if cell == CellState.CROSS)
      num_naught = sum(1 for cell in board.state if cell == CellState.NAUGHT)

      return CellState.CROSS if num_cross == num_naught else CellState.NAUGHT

    def selection(self, board: GomokuBoard, path=None): # 여기 board는 copy된 board가 들어옴
      if path is None:
        path = []

      state = board.hash_value()
      path.append(state)

      if board.who_won is not None:
         winner = board.who_won
         if winner == CellState.CROSS:
            result = GameResult.CROSS_WIN
         elif winner == CellState.NAUGHT:
            result = GameResult.NAUGHT_WIN
         else:
            result = GameResult.DRAW

         return board, path, result, True

      if state not in self.tree.nodes:
        self.tree.add_node(state, visit=0, value=0.0)

      if self.is_fully_expanded(board):
        best_score = float('-inf')
        best_actions = []

        parent_visits = self.tree.nodes[state]['visit']
        for child in self.tree.successors(state):
          visits = self.tree.nodes[child]['visit']
          value = self.tree.nodes[child]['value']
          score = self.ucb_score(parent_visits, value, visits)

          if score > best_score:
            best_score = score
            best_actions = [self.tree[state][child]['action']]
          elif score == best_score:
             best_actions.append(self.tree[state][child]['action'])

        best_action = random.choice(best_actions)
        board.move(best_action, self.current_player(board))

        return self.selection(board, path)

      else:
        return board, path, GameResult.NOT_FINISHED, False

    def expansion(self, board: GomokuBoard, path: list): # 여기 board는 copy된 board가 들어옴
        parent = board.hash_value()

        path.append(parent)

        if not self.is_fully_expanded(board):
            legal_moves = [pos for pos in range(BOARD_SIZE) if board.is_legal(pos)]

            expanded_moves = {
                self.tree.edges[parent, child]['action']
                for child in self.tree.successors(parent)
            }
            unexpanded_moves = [m for m in legal_moves if m not in expanded_moves]

            if not unexpanded_moves:
                raise ValueError("No unexpanded moves left, but is_fully_expanded returned False")

            move = random.choice(unexpanded_moves)
            _, result, finished = board.move(move, self.current_player(board))
            child = board.hash_value()

            if child not in self.tree.nodes:
                self.tree.add_node(child, visit=0, value=0.0)

            if not self.tree.has_edge(parent, child):
                self.tree.add_edge(parent, child, action=move)

            path.append(child)  # 여기서 path에 추가

            if finished:
              return board, path, result, True

            return board, path, result, False
        else:
            raise ValueError("expansion error: node is already fully expanded")

    def simulation(self, board: GomokuBoard, path: list): # 여기 board는 copy된 board가 들어옴
        if board.num_empty() == 0:
          return GameResult.DRAW, path

        finished = False
        while not finished:
          parent = board.hash_value()

          legal_moves = [pos for pos in range(BOARD_SIZE) if board.is_legal(pos)]
          move = random.choice(legal_moves)

          _, result, finished = board.move(move, self.current_player(board))
          child = board.hash_value()
          path.append(child)

          if child not in self.tree.nodes:
            self.tree.add_node(child, visit=0, value=0.0)

          if not self.tree.has_edge(parent, child):
            self.tree.add_edge(parent, child, action=move)

          if finished:
            break

        return result, path

    def backpropagation(self, path: list, result: GameResult):
        root_player = self.side

        # Convert GameResult to scalar value
        if result == GameResult.DRAW:
            scalar_result = self.DRAW_VALUE
        elif result == GameResult.CROSS_WIN:
            scalar_result = self.WIN_VALUE if root_player == CellState.CROSS else self.LOSS_VALUE
        elif result == GameResult.NAUGHT_WIN:
            scalar_result = self.WIN_VALUE if root_player == CellState.NAUGHT else self.LOSS_VALUE
        else:
            raise ValueError(f"Unknown GameResult: {result}")

        # Now propagate the result

        for idx, node in enumerate(reversed(path)):
            self.tree.nodes[node]['visit'] += 1
            self.tree.nodes[node]['value'] += scalar_result
            scalar_result = -scalar_result

    def find_optimal_move(self, board: GomokuBoard):
        current_node = board.hash_value()
        successors = list(self.tree.successors(current_node))
        if not successors:
          return -1  # fallback for terminal node

        max_visit = -1
        best_children = []

        for child in successors:
            visits = self.tree.nodes[child]['visit']
            if visits > max_visit:
                max_visit = visits
                best_children = [child]
            elif visits == max_visit:
                best_children.append(child)

        best_child = random.choice(best_children)
        action = self.tree[current_node][best_child]['action']
        return action

    def move(self, board: GomokuBoard) -> Union[GameResult, bool]:
      for _ in range(self.iteration):
        temp_board = copy.deepcopy(board)
        temp_board, path, result, finished = self.selection(temp_board)

        if finished:
          self.backpropagation(path, result)
          continue

        temp_board, path, result, finished = self.expansion(temp_board, path)

        if finished:
          self.backpropagation(path, result)
          continue

        result, path = self.simulation(temp_board, path)
        self.backpropagation(path, result)

      best_move = self.find_optimal_move(board)
      if best_move == -1:
         raise ValueError("not found best move")
      
      _, res, finished = board.move(best_move, self.side)
      return res, finished