import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 450, 450  # 50% bigger
LINE_WIDTH = 8
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 14
CROSS_WIDTH = 20
SPACE = SQUARE_SIZE // 5

# Colors
BG_COLOR = (40, 44, 52)  # Dark background
LINE_COLOR = (80, 200, 220)  # Bright cyan lines
CIRCLE_COLOR = (255, 214, 10)  # Gold circle
CROSS_COLOR = (255, 85, 85)  # Red cross

# Screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
screen.fill(BG_COLOR)

# Board
board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Functions
def draw_lines():
    # Horizontal
    for i in range(1, BOARD_ROWS):
        pygame.draw.line(screen, LINE_COLOR, (0, i * SQUARE_SIZE), (WIDTH, i * SQUARE_SIZE), LINE_WIDTH)
    # Vertical
    for i in range(1, BOARD_COLS):
        pygame.draw.line(screen, LINE_COLOR, (i * SQUARE_SIZE, 0), (i * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == 'O':
                pygame.draw.circle(screen, CIRCLE_COLOR, (int(col * SQUARE_SIZE + SQUARE_SIZE // 2), int(row * SQUARE_SIZE + SQUARE_SIZE // 2)), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == 'X':
                start_desc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE)
                end_desc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)
                start_asc = (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE)
                end_asc = (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE)
                pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

def mark_square(row, col, player):
    board[row][col] = player

def available_square(row, col):
    return board[row][col] is None

def is_board_full():
    for row in board:
        for cell in row:
            if cell is None:
                return False
    return True

def check_win(player):
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # Check columns
    for col in range(BOARD_COLS):
        if all([board[row][col] == player for row in range(BOARD_ROWS)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(BOARD_ROWS)]):
        return True
    if all([board[i][BOARD_ROWS - i - 1] == player for i in range(BOARD_ROWS)]):
        return True
    return False

def minimax(board, depth, is_maximizing):
    if check_win('O'):
        return 1
    if check_win('X'):
        return -1
    if is_board_full():
        return 0
    if is_maximizing:
        best_score = -float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] is None:
                    board[r][c] = 'O'
                    score = minimax(board, depth + 1, False)
                    board[r][c] = None
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                if board[r][c] is None:
                    board[r][c] = 'X'
                    score = minimax(board, depth + 1, True)
                    board[r][c] = None
                    best_score = min(score, best_score)
        return best_score

def ai_move():
    best_score = -float('inf')
    move = None
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            if board[r][c] is None:
                board[r][c] = 'O'
                score = minimax(board, 0, False)
                board[r][c] = None
                if score > best_score:
                    best_score = score
                    move = (r, c)
    if move:
        mark_square(move[0], move[1], 'O')
        return move
    return None, None

font = pygame.font.SysFont('arial', 64, bold=True)
def draw_message(message):
    # Blur effect: draw a semi-transparent surface over the board
    blur_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    blur_surface.fill((30, 30, 30, 180))  # More opaque for stronger blur
    screen.blit(blur_surface, (0, 0))
    # Message background
    text = font.render(message, True, (40, 44, 52))
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    bg_rect = text_rect.inflate(60, 30)
    pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=18)
    # Add a subtle shadow
    shadow_rect = bg_rect.move(4, 4)
    pygame.draw.rect(screen, (200, 200, 200), shadow_rect, border_radius=18)
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(1500)

def restart():
    global board
    board = [[None for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    screen.fill(BG_COLOR)
    draw_lines()

draw_lines()

player = 'X'  # Human is X, AI is O
game_over = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX = event.pos[0]
            mouseY = event.pos[1]
            clicked_row = mouseY // SQUARE_SIZE
            clicked_col = mouseX // SQUARE_SIZE
            if available_square(clicked_row, clicked_col):
                mark_square(clicked_row, clicked_col, player)
                if check_win(player):
                    draw_figures()
                    draw_message('You win!')
                    restart()
                    game_over = False
                    continue
                elif is_board_full():
                    draw_figures()
                    draw_message('Tie!')
                    restart()
                    game_over = False
                    continue
                else:
                    # AI turn
                    ai_row, ai_col = ai_move()
                    if ai_row is not None and check_win('O'):
                        draw_figures()
                        draw_message('AI wins!')
                        restart()
                        game_over = False
                        continue
                    elif is_board_full():
                        draw_figures()
                        draw_message('Tie!')
                        restart()
                        game_over = False
                        continue
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                game_over = False
    draw_figures()
    pygame.display.update()
