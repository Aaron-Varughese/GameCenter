import pygame
import sys
import random
import time


pygame.init()


WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  
CARD_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  
pygame.display.set_caption("Kalikuduka")


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


font_large = pygame.font.Font(None, 80)
font_small = pygame.font.Font(None, 40)
font_timer = pygame.font.Font(None, 36)


def draw_menu():
    screen.fill(WHITE)
    title_text = font_large.render("Select a Game", True, BLACK)
    memory_text = font_small.render("1. Memory Booster", True, BLACK)
    rps_text = font_small.render("2. Stone Paper Scissors", True, BLACK)
    tictactoe_text = font_small.render("3. Tic Tac Toe", True, BLACK)
    quit_text = font_small.render("4. Quit", True, BLACK)

    screen.blit(title_text, (WIDTH // 6, HEIGHT // 6))
    screen.blit(memory_text, (WIDTH // 6, HEIGHT // 3))
    screen.blit(rps_text, (WIDTH // 6, HEIGHT // 3 + 50))
    screen.blit(tictactoe_text, (WIDTH // 6, HEIGHT // 3 + 100))
    screen.blit(quit_text, (WIDTH // 6, HEIGHT // 3 + 150))

    pygame.display.update()


def load_images():
    images = []
    for i in range(1, (GRID_SIZE ** 2) // 2 + 1):
        img = pygame.image.load(f'images/{i}.jpg')  
        img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))
        images.append(img)
    return images


def generate_cards(images):
    card_values = images * 2
    random.shuffle(card_values)
    return card_values


def draw_card(x, y, image, flipped):
    rect = pygame.Rect(x * CARD_SIZE, y * CARD_SIZE, CARD_SIZE, CARD_SIZE)
    pygame.draw.rect(screen, GREEN if flipped else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    
    if flipped:
        screen.blit(image, (x * CARD_SIZE, y * CARD_SIZE))


def draw_grid(cards, flipped):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_card(x, y, cards[y * GRID_SIZE + x], flipped[y][x])


def draw_score_and_time(moves, start_time):
    elapsed_time = round(time.time() - start_time, 2)
    score_text = font_timer.render(f"Moves: {moves}", True, BLACK)
    time_text = font_timer.render(f"Time: {elapsed_time} s", True, BLACK)
    screen.blit(score_text, (20, HEIGHT + 20))
    screen.blit(time_text, (400, HEIGHT + 20))


def memory_booster_game():
    images = load_images()
    cards = generate_cards(images)
    flipped = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    selected = []
    start_time = time.time()
    moves = 0
    matched = 0

    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(cards, flipped)
        draw_score_and_time(moves, start_time)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(selected) == 2:
                    selected = []

                mouse_x, mouse_y = pygame.mouse.get_pos()
                card_x, card_y = mouse_x // CARD_SIZE, mouse_y // CARD_SIZE

                if card_y >= GRID_SIZE:
                    continue

                if not flipped[card_y][card_x]:
                    flipped[card_y][card_x] = True
                    selected.append((card_x, card_y))

                if len(selected) == 2:
                    moves += 1
                    first = selected[0]
                    second = selected[1]
                    first_image = cards[first[1] * GRID_SIZE + first[0]]
                    second_image = cards[second[1] * GRID_SIZE + second[0]]

                    if first_image == second_image:
                        matched += 2
                    else:
                        time.sleep(1)
                        flipped[first[1]][first[0]] = False
                        flipped[second[1]][second[0]] = False

                if matched == GRID_SIZE ** 2:
                    end_time = time.time()
                    total_time = round(end_time - start_time, 2)
                    print(f"You won in {moves} moves and {total_time} seconds!")
                    running = False
                    return_to_menu()

        pygame.display.update()


def stone_paper_scissors_game():
    choices = ["Stone", "Paper", "Scissors"]
    
    def load_images():
        images = {}
        for choice in choices:
            img = pygame.image.load(f'images/{choice.lower()}.jpg')  
            img = pygame.transform.scale(img, (100, 100))
            images[choice] = img
        return images

    def draw_text(text, x, y, color=BLACK):
        render = font_timer.render(text, True, color)
        screen.blit(render, (x, y))

    def draw_choice(image, x, y):
        screen.blit(image, (x, y))

    def determine_winner(player_choice, computer_choice):
        if player_choice == computer_choice:
            return "Draw"
        elif (player_choice == "Stone" and computer_choice == "Scissors") or \
             (player_choice == "Paper" and computer_choice == "Stone") or \
             (player_choice == "Scissors" and computer_choice == "Paper"):
            return "Player Wins"
        else:
            return "Computer Wins"

    images = load_images()
    player_choice = None
    computer_choice = None
    result = ""
    
    player_score = 0
    computer_score = 0
    max_wins = 3
    
    game_over = False

    running = True
    while running:
        screen.fill(WHITE)

        if game_over:
            if player_score > computer_score:
                draw_text("Player Wins the Game!", 100, 150, GREEN)
            else:
                draw_text("Computer Wins the Game!", 100, 150, RED)
            draw_text("Press R to play again!", 120, 200)
        else:
            draw_text("Choose Stone, Paper, or Scissors:", 50, 30)
            draw_choice(images["Stone"], 50, 80)
            draw_choice(images["Paper"], 200, 80)
            draw_choice(images["Scissors"], 350, 80)

            if player_choice and computer_choice:
                draw_text(f"Player: {player_choice}", 50, 250)
                draw_text(f"Computer: {computer_choice}", 250, 250)
                draw_text(result, 150, 300, RED)

            draw_text(f"Player Wins: {player_score}", 50, 350)
            draw_text(f"Computer Wins: {computer_score}", 250, 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player_score = 0
                computer_score = 0
                game_over = False
                player_choice = None
                computer_choice = None
                result = ""

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 50 < mouse_x < 150 and 80 < mouse_y < 180:
                    player_choice = "Stone"
                elif 200 < mouse_x < 300 and 80 < mouse_y < 180:
                    player_choice = "Paper"
                elif 350 < mouse_x < 450 and 80 < mouse_y < 180:
                    player_choice = "Scissors"
                
                if player_choice:
                    computer_choice = random.choice(choices)
                    result = determine_winner(player_choice, computer_choice)

                    if result == "Player Wins":
                        player_score += 1
                    elif result == "Computer Wins":
                        computer_score += 1

                    if player_score == max_wins or computer_score == max_wins:
                        game_over = True

        pygame.display.update()


def tic_tac_toe_game():
    
    LINE_WIDTH = 10
    CELL_SIZE = WIDTH // 3
    screen.fill(WHITE)

    
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)

    
    font = pygame.font.Font(None, 80)

    
    def draw_grid():
        
        pygame.draw.line(screen, BLACK, (0, CELL_SIZE), (WIDTH, CELL_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (0, 2 * CELL_SIZE), (WIDTH, 2 * CELL_SIZE), LINE_WIDTH)
        
        pygame.draw.line(screen, BLACK, (CELL_SIZE, 0), (CELL_SIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, BLACK, (2 * CELL_SIZE, 0), (2 * CELL_SIZE, HEIGHT), LINE_WIDTH)

    
    def draw_markers(board):
        for row in range(3):
            for col in range(3):
                if board[row][col] == 'X':
                    draw_x(col, row)
                elif board[row][col] == 'O':
                    draw_o(col, row)

   
    def draw_x(col, row):
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + 20),
                         (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + CELL_SIZE - 20), LINE_WIDTH)
        pygame.draw.line(screen, RED, (col * CELL_SIZE + 20, row * CELL_SIZE + CELL_SIZE - 20),
                         (col * CELL_SIZE + CELL_SIZE - 20, row * CELL_SIZE + 20), LINE_WIDTH)

    
    def draw_o(col, row):
        pygame.draw.circle(screen, BLUE, (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2),
                           CELL_SIZE // 3, LINE_WIDTH)

    
    def check_winner(board):
        
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

    
    def check_tie(board):
        for row in board:
            if '' in row:
                return False
        return True

   
    def reset_game():
        return [['', '', ''], ['', '', ''], ['', '', '']], 'X', False, None

   
    def computer_move(board):
        empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            board[row][col] = 'O'

   
    board, player_turn, game_over, winner = reset_game()  

    
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid()
        draw_markers(board)

        if game_over:
           
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

           
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over and player_turn == 'X':
                mouse_x, mouse_y = pygame.mouse.get_pos()
                clicked_row = mouse_y // CELL_SIZE
                clicked_col = mouse_x // CELL_SIZE

               
                if board[clicked_row][clicked_col] == '':
                    board[clicked_row][clicked_col] = player_turn

                   
                    winner = check_winner(board)
                    if winner:
                        game_over = True
                    elif check_tie(board):
                        game_over = True
                        winner = None
                    else:
                        # Switch player turn
                        player_turn = 'O'

            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    board, player_turn, game_over, winner = reset_game()

        
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


def return_to_menu():
    draw_menu()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    memory_booster_game()
                elif event.key == pygame.K_2:
                    stone_paper_scissors_game()
                elif event.key == pygame.K_3:
                    tic_tac_toe_game()
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    draw_menu()
    return_to_menu()
