import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK
from game import game_loop
from vision import release_resources, wait_for_hand_detection
from utils import render_text_centered

def splash_screen(screen, clock):
    """Display the splash screen with options to start or exit the game."""
    title_font = pygame.font.SysFont(None, 72)
    options_font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        screen.fill(BLACK)

        # Render title
        title = title_font.render("Pong with Hand", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))

        # Render options
        option_new_game = options_font.render("1. New Game", True, WHITE)
        option_exit = options_font.render("2. Exit", True, WHITE)
        screen.blit(option_new_game, (SCREEN_WIDTH // 2 - option_new_game.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(option_exit, (SCREEN_WIDTH // 2 - option_exit.get_width() // 2, SCREEN_HEIGHT // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start new game
                    return True
                if event.key == pygame.K_2:  # Exit game
                    running = False
                    return None

        clock.tick(60)

def select_difficulty(screen, clock):
    """Display a screen to select the AI difficulty level."""
    title_font = pygame.font.SysFont(None, 72)
    options_font = pygame.font.SysFont(None, 48)

    running = True
    while running:
        screen.fill(BLACK)

        # Render title
        title = title_font.render("Select Difficulty", True, WHITE)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))

        # Render difficulty options
        option_easy = options_font.render("1. Easy", True, WHITE)
        option_medium = options_font.render("2. Medium", True, WHITE)
        option_hard = options_font.render("3. Hard", True, WHITE)
        screen.blit(option_easy, (SCREEN_WIDTH // 2 - option_easy.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(option_medium, (SCREEN_WIDTH // 2 - option_medium.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
        screen.blit(option_hard, (SCREEN_WIDTH // 2 - option_hard.get_width() // 2, SCREEN_HEIGHT // 2 + 120))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Easy
                    return "easy"
                if event.key == pygame.K_2:  # Medium
                    return "medium"
                if event.key == pygame.K_3:  # Hard
                    return "hard"

        clock.tick(60)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    while True:
        # Show the splash screen
        if splash_screen(screen, clock) is None:
            break  # Exit the program

        # Select difficulty
        difficulty = select_difficulty(screen, clock)
        if difficulty is None:
            break  # Exit the program

        # Wait for hand detection
        if not wait_for_hand_detection(screen, clock):
            break  # Exit the program

        # Start the game loop
        if not game_loop(screen, clock, font, difficulty):
            break  # Exit the program

    pygame.quit()
    release_resources()

if __name__ == "__main__":
    main()