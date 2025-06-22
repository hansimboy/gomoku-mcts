from gomoku.board import GomokuBoard
from gomoku.players.random_player import RandomPlayer
from gomoku.utils import draw_go_board
from gomoku.board import GomokuBoard, CellState, GameResult
from gomoku.players.base import GamePlayerInterface

# from gomoku.players.mcts_player import MCTSAlgorithm
from gomoku.players import mcts_2023150428

def play_game(board: GomokuBoard, player1: GamePlayerInterface, player2: GamePlayerInterface, drawing_board: bool = True):
    player1.new_game(CellState.CROSS)
    player2.new_game(CellState.NAUGHT)
    board.reset()

    finished = False
    while not finished:
        result, finished = player1.move(board)
        if drawing_board:
            draw_go_board(board)
        if finished:
            continue
        else:
            result, finished = player2.move(board)
            if drawing_board:
                draw_go_board(board)
    return result

def battle(player1: GamePlayerInterface, player2: GamePlayerInterface, num_games: int = 1000, silent: bool = False):
    board = GomokuBoard()
    draw_count = 0
    cross_count = 0
    naught_count = 0
    for _ in range(num_games):
        result = play_game(board, player1, player2,drawing_board=False)
        if result == GameResult.CROSS_WIN:
            cross_count += 1
        elif result == GameResult.NAUGHT_WIN:
            naught_count += 1
        else:
            draw_count += 1

    if not silent:
        print("After {} game we have draws: {}, GamePlayerInterface 1 wins: {}, and GamePlayerInterface 2 wins: {}.".format(num_games, draw_count,
                                                                                                  cross_count,
                                                                                                  naught_count))

        print("Which gives percentages of draws: {:.2%}, GamePlayerInterface 1 wins: {:.2%}, and GamePlayerInterface 2 wins:  {:.2%}".format(
            draw_count / num_games, cross_count / num_games, naught_count / num_games))

    return cross_count, naught_count, draw_count

if __name__ == "__main__":
    player1 = mcts_2023150428.MCTSAlgorithm()
    player2 = RandomPlayer()
    # play_game(GomokuBoard(), player1, player2, drawing_board=True)
    battle(player1, player2, num_games=40) # about 3 miniutes time-consuming when iteration=400