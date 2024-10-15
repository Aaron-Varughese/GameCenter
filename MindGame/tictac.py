import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 10
CELL_SIZE = WIDTH // 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Fonts for text
font = pygame.font.Font(None, 80)

# Draw grid lines
def draw_grid():
    # Horizontal lines
    pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
    # Vertical lines
    pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)

# Function to display X and O
def draw_markers(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == 'X':
                draw_x(col, row)
            elif board[row][col] == 'O':
                draw_o(col, row)

# Draw X marker
def draw_x(col, row):
    pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                     (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE - 20), LINE_WIDTH)
    pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20),
                     (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + 20), LINE_WIDTH)

# Draw O marker
def draw_o(col, row):
    pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                       CELL_SIZE // 3, LINE_WIDTH)

# Check for winner
def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != '':
            return row[0]
    
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        return board[0][2]

    # No winner yet
    return None

# Check for a tie (all cells filled)
def check_tie(board):
    for row in board:
        if '' in row:
            return False
    return True

# Reset the game state
def reset_game():
    return [['', '', ''], ['', '', ''], ['', '', '']], 'X', False, None

# Computer move (simple random move)
def computer_move(board):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == '']
    if empty_cells:
        row, col = random.choice(empty_cells)
        board[row][col] = 'O'

# Main game function
def main():
    board, player_turn, game_over, winner = reset_game()  # Initialize game state

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_markers(board)

        if game_over:
            # Display winner
            if winner:
                text = font.render(f'{winner} wins!', True, BLACK)
            else:
                text = font.render('Tie!', True, BLACK)
            screen.blit(text, (WIDTH // 6, HEIGHT // 3))
            restart_text = font.render('Press R to Restart', True, BLACK)
            screen.blit(restart_text, (WIDTH // 6 - 50, HEIGHT // 3 + 80))
        
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            # Handle mouse click for placing markers
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn == 'X':
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE

                # Make sure the cell is empty
                if board[clicked_row][clicked_col] == '':
                    board[clicked_row][clicked_col] = player_turn

                    # Check if there's a winner
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif check_tie(board):
                        game_over = True
                        winner = None
                    else:
                        # Switch player turn
                        player_turn = 'O'

            # Handle 'R' key press to restart the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    board, player_turn, game_over, winner = reset_game()

        # Computer move
        if player_turn == 'O' and not game_over:
            computer_move(board)
            winner = check_winner(board)
            if winner:
                game_over = True
            elif check_tie(board):
                game_over = True
                winner = None
            else:
                player_turn = 'X'

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
