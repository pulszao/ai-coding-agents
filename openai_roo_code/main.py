# Entry point for the Pygame Tic-Tac-Toe game

import pygame
import sys
from ai_agent import get_ai_move  # Assumes this function exists and returns (row, col)

# --- Game Constants ---
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 5
CIRCLE_RADIUS = CELL_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 10
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (28, 170, 156)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (84, 84, 84)
TEXT_COLOR = (20, 20, 20)
TURN_COLOR = (50, 50, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe: Human vs AI")
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 32)

# --- Game Logic ---

def create_board():
    print("[create_board] Creating a new empty board.")
    return [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def is_board_full(board):
    full = all(all(cell is not None for cell in row) for row in board)
    print(f"[is_board_full] Board full: {full}")
    return full

def check_winner(board):
    # Rows, columns, diagonals
    for i in range(GRID_SIZE):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            print(f"[check_winner] Winner found in row {i}: {board[i][0]}")
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            print(f"[check_winner] Winner found in column {i}: {board[0][i]}")
            return board[0][i]
    # Diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        print(f"[check_winner] Winner found in main diagonal: {board[0][0]}")
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        print(f"[check_winner] Winner found in anti-diagonal: {board[0][2]}")
        return board[0][2]
    print("[check_winner] No winner found.")
    return None

def get_empty_cells(board):
    empty = [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE) if board[r][c] is None]
    print(f"[get_empty_cells] Empty cells: {empty}")
    return empty

# --- Rendering ---

def draw_board(board):
    screen.fill(BG_COLOR)
    # Draw grid lines
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, WIDTH), LINE_WIDTH)
    # Draw marks
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            center_x = c * CELL_SIZE + CELL_SIZE // 2
            center_y = r * CELL_SIZE + CELL_SIZE // 2
            if board[r][c] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (center_x, center_y), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[r][c] == "X":
                start1 = (c * CELL_SIZE + SPACE, r * CELL_SIZE + SPACE)
                end1 = (c * CELL_SIZE + CELL_SIZE - SPACE, r * CELL_SIZE + CELL_SIZE - SPACE)
                start2 = (c * CELL_SIZE + SPACE, r * CELL_SIZE + CELL_SIZE - SPACE)
                end2 = (c * CELL_SIZE + CELL_SIZE - SPACE, r * CELL_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start1, end1, CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, start2, end2, CROSS_WIDTH)

def draw_status(turn, winner, draw):
    status_rect = pygame.Rect(0, WIDTH, WIDTH, HEIGHT - WIDTH)
    pygame.draw.rect(screen, BG_COLOR, status_rect)
    if winner:
        text = f"{winner} wins!"
        color = TURN_COLOR
    elif draw:
        text = "Draw!"
        color = TURN_COLOR
    else:
        text = f"{turn}'s turn"
        color = TURN_COLOR if turn == "O" else CROSS_COLOR
    label = font.render(text, True, color)
    label_rect = label.get_rect(center=(WIDTH // 2, WIDTH + (HEIGHT - WIDTH) // 2))
    screen.blit(label, label_rect)
    # Draw reset instruction
    reset_label = small_font.render("Press R to reset", True, TEXT_COLOR)
    reset_rect = reset_label.get_rect(center=(WIDTH // 2, HEIGHT - 30))
    screen.blit(reset_label, reset_rect)

# --- Main Game Loop ---

def main():
    print("[main] Starting main game loop.")
    board = create_board()
    human = "X"
    ai = "O"
    turn = human  # Human always starts
    running = True
    winner = None
    draw = False
    ai_thinking = False

    while running:
        draw_board(board)
        draw_status(turn, winner, draw)
        pygame.display.flip()

        if winner or draw:
            print(f"[main] Game ended. Winner: {winner}, Draw: {draw}")
            # Wait for reset
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("[main] Quit event received. Exiting game loop.")
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    print("[main] Reset key pressed. Resetting game.")
                    board = create_board()
                    turn = human
                    winner = None
                    draw = False
                    ai_thinking = False
            continue

        if turn == ai and not ai_thinking:
            print("[main] AI's turn. Setting ai_thinking to True and starting timer.")
            # AI's turn: call get_ai_move(board)
            ai_thinking = True
            pygame.time.set_timer(pygame.USEREVENT, 300)  # Small delay for UX

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("[main] Quit event received. Exiting game loop.")
                running = False

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                print("[main] Reset key pressed. Resetting game.")
                board = create_board()
                turn = human
                winner = None
                draw = False
                ai_thinking = False

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn == human:
                x, y = event.pos
                print(f"[main] Mouse click at ({x}, {y}) by human.")
                if y < WIDTH:  # Only allow clicks in grid area
                    row = y // CELL_SIZE
                    col = x // CELL_SIZE
                    print(f"[main] Human attempting move at ({row}, {col}).")
                    if board[row][col] is None and not winner:
                        board[row][col] = human
                        print(f"[main] Human placed at ({row}, {col}). Board now: {board}")
                        winner = check_winner(board)
                        if not winner and is_board_full(board):
                            print("[main] Board is full after human move. Declaring draw.")
                            draw = True
                        else:
                            print("[main] Switching turn to AI.")
                            turn = ai
                    else:
                        print(f"[main] Invalid move by human at ({row}, {col}). Cell occupied or game over.")

            elif event.type == pygame.USEREVENT and turn == ai and ai_thinking:
                print("[main] USEREVENT: AI's move about to be made.")
                # AI move
                # Convert board to AI-compatible format ('' for empty)
                ai_board = [[cell if cell is not None else '' for cell in row] for row in board]
                print(f"[main] Calling get_ai_move with board: {ai_board}")
                move = get_ai_move(ai_board)
                print(f"[main] AI selected move: {move}")
                if move and board[move[0]][move[1]] is None:
                    board[move[0]][move[1]] = ai
                    print(f"[main] AI placed at ({move[0]}, {move[1]}). Board now: {board}")
                    winner = check_winner(board)
                    if not winner and is_board_full(board):
                        print("[main] Board is full after AI move. Declaring draw.")
                        draw = True
                    else:
                        print("[main] Switching turn to human.")
                        turn = human
                else:
                    print(f"[main] AI move invalid or cell occupied: {move}")
                ai_thinking = False
                pygame.time.set_timer(pygame.USEREVENT, 0)

    print("[main] Exiting game. Quitting pygame.")
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()