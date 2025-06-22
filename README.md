# Playing Gomoku using MCTSAlgorithm

This project implements an AI agent that plays the game of Gomoku using the Monte Carlo Tree Search (MCTS) algorithm.  

Against a random player, the MCTS agent achieves over **95% win rate as the first player**,  
and over **85% win rate as the second player**

## Configuration

By default, the game is played on a **5×5 board** with a win condition of **three in a row**.  
These settings can be customized by modifying the following constants in `constants.py`:

- `BOARD_DIM`: Size of the board (e.g., 5 → 5×5 board)
- `NUM_WIN`: Number of stones in a row needed to win (e.g., 3 for "three in a row")
---

이 프로젝트는 MCTS 알고리즘을 사용하여 오목(Gomoku)을 플레이하는 AI 에이전트를 구현합니다.

random player와 게임할 때, 선공일 경우 **95%이상의 승률**, 후공일 경우 **85%이상의 승률**을 보여줍니다.

기본 설정에서는 **5×5 크기의 보드**에서 **3목**을 먼저 만드는 플레이어가 승리합니다.  
이 설정은 `constants.py` 파일의 다음 상수를 수정하여 자유롭게 변경할 수 있습니다:

- `BOARD_DIM`: 보드의 크기 (예: 5 → 5x5 보드)
- `NUM_WIN`: 승리 조건이 되는 연속 돌의 개수 (예: 3 → 3목)
