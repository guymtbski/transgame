import pygame
import random
import os
import time
import sys

# Initialize Pygame
pygame.init()

# Game Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TREE_WIDTH = 60  # Adjusted tree width to match image
TREE_HEIGHT = 60  # Adjusted tree height to match image
BACKGROUND_COLOR = (135, 206, 235)  # Sky blue

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Skiing Adventure')

# --- Resource Path Function ---
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, "trans", relative_path)  # Add "trans" here

# Load tree image 
tree_image_path = resource_path("trump_tree.png")  # Using resource_path

# Check if the image files exist
if not os.path.isfile(tree_image_path):
    print(f"Error: The image file '{tree_image_path}' was not found.")
    pygame.quit()
    sys.exit()

# Load the tree image
tree_image = pygame.image.load(tree_image_path)

# Optionally scale the image if it is too large or too small
TREE_WIDTH = 60
TREE_HEIGHT = 60
tree_image = pygame.transform.scale(tree_image, (TREE_WIDTH, TREE_HEIGHT))

# Game variables
skier_image_path = resource_path("skier.png")  # Using resource_path
if not os.path.isfile(skier_image_path):
    print(f"Error: The image file '{skier_image_path}' was not found.")
    pygame.quit()
    sys.exit()

# Load the skier image
skier_image = pygame.image.load(skier_image_path)

# Increase the size of the skier
skier_width = 100  # Increased width
skier_height = 100  # Increased height
skier_image = pygame.transform.scale(skier_image, (skier_width, skier_height))
skier_rect = skier_image.get_rect()

# Initial positions and speeds
skier_x = SCREEN_WIDTH // 2 - skier_width // 2
skier_y = SCREEN_HEIGHT - skier_rect.height - 10
skier_velocity = 5
trees = []
score = 0
game_over = False

# Define font for score and game over text
font = pygame.font.SysFont('Arial', 36)

# Load trans.png 
trans_image_path = resource_path("trans.png")  # Using resource_path
if not os.path.isfile(trans_image_path):
    print(f"Error: The image file '{trans_image_path}' was not found.")
    pygame.quit()
    sys.exit()

# Load the trans.png image
trans_image = pygame.image.load(trans_image_path)
trans_image = pygame.transform.scale(trans_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Load noo.mp3
sound_file_path = resource_path("noo.mp3")  # Using resource_path
if not os.path.isfile(sound_file_path):
    print(f"Error: The sound file '{sound_file_path}' was not found.")
    pygame.quit()
    sys.exit()

# Load and play the background music (YMCA)
background_music_path = resource_path("ymca.mp3")
if not os.path.isfile(background_music_path):
    print(f"Error: The music file '{background_music_path}' was not found.")
    pygame.quit()
    sys.exit()

pygame.mixer.init()
# Load the 'noo.mp3' for game over
pygame.mixer.music.load(sound_file_path)
# Load the 'ymca.mp3' for background music
background_music = pygame.mixer.Sound(background_music_path)

# Start playing background music in a loop
background_music.play(-1)  # -1 means play indefinitely

# Functions to draw skier and trees
def draw_skier(x, y):
    screen.blit(skier_image, (x, y))

def draw_tree(x, y):
    screen.blit(tree_image, (x, y))

def draw_trees(trees):
    for tree in trees:
        draw_tree(tree[0], tree[1])

def check_collision(skier_x, skier_y, trees):
    for tree in trees:
        if (skier_x < tree[0] + TREE_WIDTH and
                skier_x + skier_rect.width > tree[0] and
                skier_y < tree[1] + TREE_HEIGHT and
                skier_y + skier_rect.height > tree[1]):
            return True
    return False

def display_score(score):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

def display_game_over():
    game_over_text = font.render("Game Over", True, (255, 0, 0))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))

# Main game loop
clock = pygame.time.Clock()
while True:
    screen.fill(BACKGROUND_COLOR)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and skier_x > 0:
            skier_x -= skier_velocity
        if keys[pygame.K_RIGHT] and skier_x < SCREEN_WIDTH - skier_rect.width:
            skier_x += skier_velocity

        # Move trees
        for tree in trees:
            tree[1] += 5

        # Add new trees
        if random.random() < 0.02:
            new_tree_x = random.randint(0, SCREEN_WIDTH - TREE_WIDTH)
            trees.append([new_tree_x, -TREE_HEIGHT])

        # Remove off-screen trees
        trees = [tree for tree in trees if tree[1] < SCREEN_HEIGHT]

        # Check for collision with trees
        if check_collision(skier_x, skier_y, trees):
            game_over = True

        # Update score
        score += 1

        # Draw everything
        draw_skier(skier_x, skier_y)
        draw_trees(trees)
        display_score(score)

    else:  # Game over condition
        screen.blit(trans_image, (0, 0))
        pygame.mixer.music.play()  # Play noo.mp3 for game over
        pygame.display.update()
        time.sleep(3)
        pygame.quit()
        sys.exit()

    pygame.display.update()

    # Set the frame rate
    clock.tick(60)