import copy
# Local AI opponent logic for Tic-Tac-Toe

def get_ai_move(board):
    print("[ai_agent.py] get_ai_move called")
    print("[get_ai_move] Called with board:")
    for row in board:
        print("  ", row)
    """
    Determines the AI's move using the minimax algorithm for unbeatable play.

    Args:
        board (list of list): 3x3 list of lists representing the current board state.
            Each cell contains 'X', 'O', or '' (empty string) to indicate the state.

    Returns:
        tuple: (row, col) indicating the AI's chosen move (0-based indices).

    The AI assumes it is playing as 'O' and the human is 'X'.
    The function ensures the returned move is valid (the cell is empty).
    """

    AI = 'O'
    HUMAN = 'X'
    EMPTY = None
    EMPTY_ALT = ''  # Accept empty string as empty for compatibility

    def is_moves_left(b):
        for row in b:
            if EMPTY in row or EMPTY_ALT in row:
                return True
        return False

    def evaluate(b):
        # Check rows and columns
        for i in range(3):
            if (
                b[i][0] == b[i][1] == b[i][2]
                and b[i][0] != EMPTY
                and b[i][0] != EMPTY_ALT
            ):
                if b[i][0] == AI:
                    print(f"[evaluate] Row {i} win for AI")
                    return +10
                elif b[i][0] == HUMAN:
                    print(f"[evaluate] Row {i} win for HUMAN")
                    return -10
            if (
                b[0][i] == b[1][i] == b[2][i]
                and b[0][i] != EMPTY
                and b[0][i] != EMPTY_ALT
            ):
                if b[0][i] == AI:
                    print(f"[evaluate] Col {i} win for AI")
                    return +10
                elif b[0][i] == HUMAN:
                    print(f"[evaluate] Col {i} win for HUMAN")
                    return -10
        # Check diagonals
        if (
            b[0][0] == b[1][1] == b[2][2]
            and b[0][0] != EMPTY
            and b[0][0] != EMPTY_ALT
        ):
            if b[0][0] == AI:
                print("[evaluate] Main diagonal win for AI")
                return +10
            elif b[0][0] == HUMAN:
                print("[evaluate] Main diagonal win for HUMAN")
                return -10
        if (
            b[0][2] == b[1][1] == b[2][0]
            and b[0][2] != EMPTY
            and b[0][2] != EMPTY_ALT
        ):
            if b[0][2] == AI:
                print("[evaluate] Anti-diagonal win for AI")
                return +10
            elif b[0][2] == HUMAN:
                print("[evaluate] Anti-diagonal win for HUMAN")
                return -10
        print(f"[evaluate] Returning 0")
        return 0

import time

minimax_call_count = 0

def minimax(b, depth, is_max):
    global minimax_call_count
    minimax_call_count += 1
    start_time = time.time()
    score = evaluate(b)
    if score == 10 or score == -10:
        end_time = time.time()
        print(f"[minimax] Terminal node at depth {depth}, time: {end_time - start_time:.4f}s, call count: {minimax_call_count}")
        return score
    if not is_moves_left(b):
        end_time = time.time()
        print(f"[minimax] No moves left at depth {depth}, time: {end_time - start_time:.4f}s, call count: {minimax_call_count}")
        return 0

        if is_max:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if b[i][j] == EMPTY or b[i][j] == EMPTY_ALT:
                        original = b[i][j]
                        b[i][j] = AI
                        val = minimax(b, depth + 1, not is_max)
                        best = max(best, val)
                        b[i][j] = original
            end_time = time.time()
            print(f"[minimax] (is_max) Best value at depth {depth}: {best}, time: {end_time - start_time:.4f}s, call count: {minimax_call_count}")
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if b[i][j] == EMPTY or b[i][j] == EMPTY_ALT:
                        original = b[i][j]
                        b[i][j] = HUMAN
                        val = minimax(b, depth + 1, not is_max)
                        best = min(best, val)
                        b[i][j] = original
            end_time = time.time()
            print(f"[minimax] (is_min) Best value at depth {depth}: {best}, time: {end_time - start_time:.4f}s, call count: {minimax_call_count}")
            return best

    best_val = -1000
    best_move = (-1, -1)
    print("[get_ai_move] Searching for best move for AI...")
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY or board[i][j] == EMPTY_ALT:
                print(f"[get_ai_move] Trying move at ({i},{j})")
                original = board[i][j]
                board[i][j] = AI
                start_time = time.time()
                move_val = minimax(copy.deepcopy(board), 0, False)
                end_time = time.time()
                print(f"[get_ai_move] Move at ({i},{j}) has value {move_val}, time: {end_time - start_time:.4f}s, call count: {minimax_call_count}")
                board[i][j] = original
                print(f"[get_ai_move] Current best_val: {best_val}, move_val: {move_val}")
                if move_val > best_val:
                    print(f"[get_ai_move] New best move found at ({i},{j}) with value {move_val}")
                    best_val = move_val
                    best_move = (i, j)
                print(f"[get_ai_move] best_val after comparison: {best_val}")

    # Fallback: if no move found (should not happen), pick first empty cell
    if best_move == (-1, -1):
        print("[get_ai_move] No best move found, using fallback to first empty cell.")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY or board[i][j] == EMPTY_ALT:
                    print(f"[get_ai_move] Fallback move: ({i},{j})")
                    return (i, j)
        print("[get_ai_move] No moves available, returning (-1, -1)")
        return best_move if best_move != (-1, -1) else None
    print(f"[get_ai_move] Returning best move: {best_move} with value {best_val}")
    return best_move