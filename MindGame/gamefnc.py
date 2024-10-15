import pygame
import random
import time

# Initialize Pygame
pygame.init()  # Initializes all the Pygame modules

# Set window dimensions
WIDTH, HEIGHT = 600, 600  # Window dimensions
GRID_SIZE = 4  # 4x4 grid of cards
CARD_SIZE = WIDTH // GRID_SIZE  # Calculate card size based on grid size
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Create a Pygame window with extra space at the bottom for score and timer
pygame.display.set_caption("Project Mambazham-Memory Booster Game")  # Set window title

# Colors
WHITE = (255, 255, 255)  # RGB value for white color (background)
BLACK = (0, 0, 0)  # RGB value for black color (text and borders)
GREEN = (0, 255, 0)  # RGB value for green color (flipped card background)

# Font for the timer and score
font = pygame.font.Font(None, 36)  # Load default font with size 36 for displaying score and time

# Load card images
def load_images():
    images = []  # Empty list to store the images
    for i in range(1, (GRID_SIZE ** 2) // 2 + 1):  # Loop over the number of images needed (half of the total cards)
        img = pygame.image.load(f'images/{i}.jpg')  # Load each image (ensure images are named like '1.jpg', '2.jpg', etc.)
        img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))  # Resize images to fit card size
        images.append(img)  # Add the resized image to the list
    return images  # Return the list of images

# Create cards (randomized pairs of images)
def generate_cards(images):
    card_values = images * 2  # Duplicate the list of images to have pairs
    random.shuffle(card_values)  # Shuffle the cards to randomize their positions
    return card_values  # Return the shuffled card list

# Draw a single card on the grid
def draw_card(x, y, image, flipped):
    rect = pygame.Rect(x * CARD_SIZE, y * CARD_SIZE, CARD_SIZE, CARD_SIZE)  # Create a rectangle representing the card
    pygame.draw.rect(screen, GREEN if flipped else WHITE, rect)  # Draw the card with green background if flipped, white otherwise
    pygame.draw.rect(screen, BLACK, rect, 2)  # Draw a black border around the card

    if flipped:  # If the card is flipped, display the image
        screen.blit(image, (x * CARD_SIZE, y * CARD_SIZE))  # Draw the image on the card

# Draw the entire grid of cards
def draw_grid(cards, flipped):
    for y in range(GRID_SIZE):  # Loop through the rows of the grid
        for x in range(GRID_SIZE):  # Loop through the columns of the grid
            draw_card(x, y, cards[y * GRID_SIZE + x], flipped[y][x])  # Draw each card based on its position and flip state

# Draw score and time
def draw_score_and_time(moves, start_time):
    elapsed_time = round(time.time() - start_time, 2)  # Calculate the elapsed time since the game started
    score_text = font.render(f"Moves: {moves}", True, BLACK)  # Render the moves text
    time_text = font.render(f"Time: {elapsed_time} s", True, BLACK)  # Render the elapsed time text

    screen.blit(score_text, (20, HEIGHT + 20))  # Draw the moves text on the screen
    screen.blit(time_text, (400, HEIGHT + 20))  # Draw the time text on the screen

# Main game function
def main():
    # Load images and generate cards
    images = load_images()  # Load the card images from the folder
    cards = generate_cards(images)  # Generate the shuffled card pairs
    flipped = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]  # Create a 2D list to keep track of flipped cards
    selected = []  # List to store the currently selected cards
    start_time = time.time()  # Record the start time of the game
    moves = 0  # Counter for the number of moves
    matched = 0  # Counter for the number of matched cards

    # Game loop
    running = True  # Flag to control the game loop
    while running:
        screen.fill(WHITE)  # Fill the screen with white background
        draw_grid(cards, flipped)  # Draw the card grid on the screen
        draw_score_and_time(moves, start_time)  # Draw the score and time on the screen
        pygame.display.flip()  # Update the display

        for event in pygame.event.get():  # Handle events
            if event.type == pygame.QUIT:  # If the window is closed
                running = False  # Exit the game loop

            if event.type == pygame.MOUSEBUTTONDOWN:  # If the player clicks the mouse
                if len(selected) == 2:  # If two cards are already selected
                    selected = []  # Reset the selected list

                mouse_x, mouse_y = pygame.mouse.get_pos()  # Get the mouse position
                card_x, card_y = mouse_x // CARD_SIZE, mouse_y // CARD_SIZE  # Convert mouse position to grid coordinates

                if card_y >= GRID_SIZE:  # Ignore clicks below the grid (where score/timer are displayed)
                    continue  # Skip to the next iteration

                if not flipped[card_y][card_x]:  # If the clicked card is not flipped yet
                    flipped[card_y][card_x] = True  # Flip the card
                    selected.append((card_x, card_y))  # Add the card to the selected list

                if len(selected) == 2:  # If two cards are now selected
                    moves += 1  # Increment the move counter
                    first = selected[0]  # Get the first selected card
                    second = selected[1]  # Get the second selected card
                    first_image = cards[first[1] * GRID_SIZE + first[0]]  # Get the image of the first card
                    second_image = cards[second[1] * GRID_SIZE + second[0]]  # Get the image of the second card

                    if first_image == second_image:  # If the two selected cards match
                        matched += 2  # Increment the matched counter
                    else:
                        time.sleep(1)  # Brief delay before flipping back the cards
                        flipped[first[1]][first[0]] = False  # Unflip the first card
                        flipped[second[1]][second[0]] = False  # Unflip the second card

                if matched == GRID_SIZE ** 2:  # If all cards are matched
                    end_time = time.time()  # Record the end time
                    total_time = round(end_time - start_time, 2)  # Calculate the total time
                    print(f"You won in {moves} moves and {total_time} seconds!")  # Print the winning message
                    running = False  # Exit the game loop

        pygame.display.update()  # Update the display

    pygame.quit()  # Quit the Pygame module

# Run the game
if __name__ == "__main__":
    main()  # Start the game by calling the main function
