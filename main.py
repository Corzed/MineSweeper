import random
import pygame
import sys

# Constants for game settings
BOARD_SIZE = 10  # 10x10 board
MINES_COUNT = 15  # Total number of mines
CELL_SIZE = 40  # Pixel size of each cell
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
WINDOW_HEIGHT = WINDOW_SIZE + 50  # Additional space for the mine count display

# Colors
OPEN_CELL_COLOR = (229, 229, 229)
CLOSED_CELL_COLOR = (189, 189, 189)
FLAG_COLOR = (255, 69, 0)
MINE_COLOR = (128, 128, 128)
NUMBER_COLORS = [
    None,
    (25, 118, 210),
    (56, 142, 60),
    (211, 47, 47),
    (123, 31, 162),
    (255, 143, 0),
    (0, 77, 64),
    (84, 84, 84),
    (0, 0, 0),
]
BORDER_COLOR = (60, 60, 60)
COUNTDOWN_POS = (5, WINDOW_SIZE + 5)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper")
font = pygame.font.SysFont('arial', 25, bold=True)

# Game states
UNOPENED = "unopened"
FLAGGED = "flagged"
OPENED = "opened"


def init_board(mines_count):
    board = [[{'state': UNOPENED, 'value': 0, 'is_mine': False} for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mines_placed = 0
    while mines_placed < mines_count:
        x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
        if not board[y][x]['is_mine']:
            board[y][x]['is_mine'] = True
            mines_placed += 1
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                        board[ny][nx]['value'] += 1
    return board


def draw_board(board, game_over, mines_left, highlight_cells):
    screen.fill((255, 255, 255))  # Clear screen for drawing
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            cell = board[y][x]
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            # Determine cell color
            if cell['state'] == UNOPENED or (game_over and cell['is_mine'] and cell['state'] != FLAGGED):
                cell_color = CLOSED_CELL_COLOR
                if (x, y) in highlight_cells:
                    cell_color = (255, 255, 0)  # Yellow highlight for potential moves
            elif cell['state'] == FLAGGED:
                cell_color = CLOSED_CELL_COLOR
            else:
                cell_color = OPEN_CELL_COLOR

            pygame.draw.rect(screen, cell_color, rect.inflate(-2, -2))

            if cell['state'] == FLAGGED:
                pygame.draw.polygon(screen, FLAG_COLOR, [(rect.left + 10, rect.top + 10),
                                                         (rect.left + 10, rect.bottom - 10),
                                                         (rect.right - 10, rect.centery)])
            elif cell['state'] == OPENED and cell['value'] > 0 and not cell['is_mine']:
                text = font.render(str(cell['value']), True, NUMBER_COLORS[cell['value']])
                screen.blit(text, text.get_rect(center=rect.center))
            if game_over and cell['is_mine']:
                if cell['state'] != FLAGGED:  # Only draw mines if not flagged or incorrectly flagged
                    pygame.draw.circle(screen, MINE_COLOR, rect.center, CELL_SIZE // 4)

    # Draw mines left count
    countdown_text = font.render(f"Mines Left: {mines_left}", True, (0, 0, 0))
    screen.blit(countdown_text, COUNTDOWN_POS)

    pygame.display.flip()


def open_cell(board, x, y):
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x]['state'] == UNOPENED:
        board[y][x]['state'] = OPENED
        if board[y][x]['is_mine']:
            return True  # Game over
        if board[y][x]['value'] == 0:
            for nx, ny in get_adjacent_cells(x, y):
                if board[ny][nx]['state'] == UNOPENED:
                    open_cell(board, nx, ny)
    return False


def get_adjacent_cells(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == 0 and dy == 0:
                continue  # Skip the cell itself
            nx, ny = x + dx, y + dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                yield nx, ny


def chord_cell(board, x, y):
    if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x]['state'] == OPENED:
        cell = board[y][x]
        if 0 < cell['value'] <= 8:  # Ensure it's a numbered cell
            flags_count = sum(board[ny][nx]['state'] == FLAGGED for nx, ny in get_adjacent_cells(x, y))
            if flags_count == cell['value']:
                for nx, ny in get_adjacent_cells(x, y):
                    if board[ny][nx]['state'] == UNOPENED:
                        open_cell(board, nx, ny)


def toggle_flag(board, x, y):
    cell = board[y][x]
    if cell['state'] == UNOPENED:
        cell['state'] = FLAGGED
    elif cell['state'] == FLAGGED:
        cell['state'] = UNOPENED


def calculate_mines_left(board):
    flags_placed = sum(cell['state'] == FLAGGED for row in board for cell in row)
    return MINES_COUNT - flags_placed


def main():
    board = init_board(MINES_COUNT)
    running = True
    game_over = False
    highlight_cells = []  # List to keep track of cells to highlight

    while running:
        mines_left = calculate_mines_left(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                if event.button == 1:  # Left click
                    game_over = open_cell(board, x, y)
                elif event.button == 3:  # Right click
                    toggle_flag(board, x, y)
                elif event.button == 2:  # Middle click for chording and highlighting
                    highlight_cells = list(get_adjacent_cells(x, y))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:  # Middle button release
                highlight_cells = []  # Clear highlight cells list
                x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
                chord_cell(board, x, y)

        draw_board(board, game_over, mines_left, highlight_cells)

    pygame.quit()



if __name__ == "__main__":
    main()
