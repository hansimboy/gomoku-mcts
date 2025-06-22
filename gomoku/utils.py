import matplotlib.pyplot as plt
import time
from IPython.display import clear_output
from .board import GomokuBoard, BOARD_DIM

def draw_go_board(board: GomokuBoard):
    clear_output(wait=True)
    fig, ax = plt.subplots(figsize=(BOARD_DIM, BOARD_DIM))
    ax.set_xlim(0, BOARD_DIM)
    ax.set_ylim(0, BOARD_DIM)

    cell_size = 0.97
    rect_offset = (1.-cell_size) / 2  # Offset to center the cells
    offset = 1 / 2

    # Draw black board
    ax.add_patch(plt.Rectangle((0, 0), BOARD_DIM, BOARD_DIM, color='black', fill=True))

    # Draw white cells
    for x in range(BOARD_DIM):
        for y in range(BOARD_DIM):
            ax.add_patch(plt.Rectangle((x + rect_offset, y + rect_offset), cell_size, cell_size, color='white', fill=True))

    # Place markers
    for x in range(BOARD_DIM):
        for y in range(BOARD_DIM):
            pos = x * BOARD_DIM + y
            marker = board.state_to_char(pos)
            ax.text(x + offset, y + offset, marker, ha='center', va='center', fontsize=20)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    plt.show()
    time.sleep(0.5)

# board = GomokuBoard()
# draw_go_board(board)