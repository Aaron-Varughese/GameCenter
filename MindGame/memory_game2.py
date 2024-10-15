import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 4  # 4x4 grid of cards
CARD_SIZE = WIDTH // GRID_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT + 100))  # Extra space for score and timer
pygame.display.set_caption("Project Mambazham-Memory Booster Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Font for the timer and score
font = pygame.font.Font(None, 36)

# Load card images
def load_images():
    images = []
    for i in range(1, (GRID_SIZE ** 2) // 2 + 1):
        img = pygame.image.load(f'images/{i}.jpg')  # Ensure your images are named like '1.png', '2.png', etc.
        img = pygame.transform.scale(img, (CARD_SIZE, CARD_SIZE))  # Resize images to fit card size
        images.append(img)
    return images

# Create cards (randomized pairs of images)
def generate_cards(images):
    card_values = images * 2  # Two of each image
    random.shuffle(card_values)
    return card_values

# Draw a single card on the grid
def draw_card(x, y, image, flipped):
    rect = pygame.Rect(x * CARD_SIZE, y * CARD_SIZE, CARD_SIZE, CARD_SIZE)
    pygame.draw.rect(screen, GREEN if flipped else WHITE, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    
    if flipped:
        screen.blit(image, (x * CARD_SIZE, y * CARD_SIZE))

# Draw the entire grid of cards
def draw_grid(cards, flipped):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            draw_card(x, y, cards[y * GRID_SIZE + x], flipped[y][x])

# Draw score and time
def draw_score_and_time(moves, start_time):
    elapsed_time = round(time.time() - start_time, 2)
    score_text = font.render(f"Moves: {moves}", True, BLACK)
    time_text = font.render(f"Time: {elapsed_time} s", True, BLACK)

    screen.blit(score_text, (20, HEIGHT + 20))
    screen.blit(time_text, (400, HEIGHT + 20))

# Main game function
def main():
    # Load images and generate cards
    images = load_images()  # Load the images from the folder
    cards = generate_cards(images)
    flipped = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
    selected = []
    start_time = time.time()
    moves = 0
    matched = 0

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)
        draw_grid(cards, flipped)
        draw_score_and_time(moves, start_time)  # Draw score and time
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if len(selected) == 2:  # Reset after two cards are selected
                    selected = []

                mouse_x, mouse_y = pygame.mouse.get_pos()
                card_x, card_y = mouse_x // CARD_SIZE, mouse_y // CARD_SIZE

                if card_y >= GRID_SIZE:  # Ignore clicks below the grid (where score/timer are displayed)
                    continue

                if not flipped[card_y][card_x]:  # Flip the card if not already flipped
                    flipped[card_y][card_x] = True
                    selected.append((card_x, card_y))

                if len(selected) == 2:
                    moves += 1
                    first = selected[0]
                    second = selected[1]
                    first_image = cards[first[1] * GRID_SIZE + first[0]]
                    second_image = cards[second[1] * GRID_SIZE + second[0]]

                    if first_image == second_image:  # Cards match
                        matched += 2
                    else:
                        time.sleep(1)  # Brief delay before flipping back
                        flipped[first[1]][first[0]] = False
                        flipped[second[1]][second[0]] = False

                if matched == GRID_SIZE ** 2:  # All cards are matched
                    end_time = time.time()
                    total_time = round(end_time - start_time, 2)
                    print(f"You won in {moves} moves and {total_time} seconds!")
                    running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
