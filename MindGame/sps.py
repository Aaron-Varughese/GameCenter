import pygame
import random

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 500, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stone Paper Scissors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Font for displaying text
font = pygame.font.Font(None, 36)

# Choices
choices = ["Stone", "Paper", "Scissors"]

# Load images for stone, paper, scissors
def load_images():
    images = {}
    for choice in choices:
        img = pygame.image.load(f'images/{choice.lower()}.jpg')  # Ensure you have 'stone.png', 'paper.png', 'scissors.png'
        img = pygame.transform.scale(img, (100, 100))
        images[choice] = img
    return images

# Function to display text on screen
def draw_text(text, x, y, color=BLACK):
    render = font.render(text, True, color)
    screen.blit(render, (x, y))

# Function to display images of choices
def draw_choice(image, x, y):
    screen.blit(image, (x, y))

# Function to determine the winner
def determine_winner(player_choice, computer_choice):
    if player_choice == computer_choice:
        return "Draw"
    elif (player_choice == "Stone" and computer_choice == "Scissors") or \
         (player_choice == "Paper" and computer_choice == "Stone") or \
         (player_choice == "Scissors" and computer_choice == "Paper"):
        return "Player Wins"
    else:
        return "Computer Wins"

# Main game function
def main():
    images = load_images()  # Load images for Stone, Paper, Scissors
    player_choice = None
    computer_choice = None
    result = ""
    
    player_score = 0
    computer_score = 0
    max_wins = 3  # Best of 3 (you can change to 5 or 7)
    
    game_over = False

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)

        if game_over:
            # Display final result
            if player_score > computer_score:
                draw_text("Player Wins the Game!", 100, 150, GREEN)
            else:
                draw_text("Computer Wins the Game!", 100, 150, RED)
            draw_text("Press R to play again!", 120, 200)
        else:
            # Display choices
            draw_text("Choose Stone, Paper, or Scissors:", 50, 30)
            draw_choice(images["Stone"], 50, 80)
            draw_choice(images["Paper"], 200, 80)
            draw_choice(images["Scissors"], 350, 80)

            # Display the result
            if player_choice and computer_choice:
                draw_text(f"Player: {player_choice}", 50, 250)
                draw_text(f"Computer: {computer_choice}", 250, 250)
                draw_text(result, 150, 300, RED)

            # Display score
            draw_text(f"Player Wins: {player_score}", 50, 350)
            draw_text(f"Computer Wins: {computer_score}", 250, 350)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                # Reset game if "R" is pressed after game over
                player_score = 0
                computer_score = 0
                game_over = False
                player_choice = None
                computer_choice = None
                result = ""

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Detect player choice
                if 50 < mouse_x < 150 and 80 < mouse_y < 180:
                    player_choice = "Stone"
                elif 200 < mouse_x < 300 and 80 < mouse_y < 180:
                    player_choice = "Paper"
                elif 350 < mouse_x < 450 and 80 < mouse_y < 180:
                    player_choice = "Scissors"
                
                if player_choice:
                    computer_choice = random.choice(choices)  # Computer randomly selects
                    result = determine_winner(player_choice, computer_choice)

                    # Update score
                    if result == "Player Wins":
                        player_score += 1
                    elif result == "Computer Wins":
                        computer_score += 1

                    # Check if the game is over
                    if player_score == max_wins or computer_score == max_wins:
                        game_over = True

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
