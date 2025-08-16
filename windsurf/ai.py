import random

def ai_move(board):
    possible_moves = []
    for row in range(3):
        for col in range(3):
            if board[row][col] is None:
                possible_moves.append((row, col))

    move = random.choice(possible_moves)
    return move


def make_decision(board):
    move = ai_move(board)
    return move
