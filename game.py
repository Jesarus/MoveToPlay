import pygame
from config import *
from utils import draw_score
from vision import update_webcam
import random

def handle_ai_movement(y_ai, y_ball, ai_speed):
    """Move the AI paddle based on the ball's position."""
    if y_ai + PADDLE_HEIGHT // 2 < y_ball:
        y_ai += ai_speed
    elif y_ai + PADDLE_HEIGHT // 2 > y_ball:
        y_ai -= ai_speed
    return max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, y_ai))

def handle_ball_movement(x_ball, y_ball, ball_speed_x, ball_speed_y):
    """Move the ball and handle collisions with the top and bottom walls."""
    x_ball += ball_speed_x
    y_ball += ball_speed_y

    # Collision with top and bottom
    if y_ball <= 0 or y_ball >= SCREEN_HEIGHT:
        ball_speed_y *= -1

    return x_ball, y_ball, ball_speed_x, ball_speed_y

def check_paddle_collision(x_ball, y_ball, x_paddle, y_paddle):
    """Check if the ball collides with a paddle."""
    return (x_paddle <= x_ball <= x_paddle + PADDLE_WIDTH and
            y_paddle < y_ball < y_paddle + PADDLE_HEIGHT)

def reset_ball(difficulty):
    """Reset the ball to the initial position and give it a random direction based on difficulty."""
    x_ball = SCREEN_WIDTH // 3 + (2 * SCREEN_WIDTH // 3) // 2  # Initial horizontal position
    y_ball = SCREEN_HEIGHT // 2  # Center vertically

    # Set ball speed based on difficulty
    speed = {"easy": 5, "medium": 6, "hard": 7}.get(difficulty, 4)

    ball_speed_x = random.choice([-speed, speed])  # Randomly choose left or right
    ball_speed_y = random.choice([-speed, speed])  # Randomly choose up or down
    return x_ball, y_ball, ball_speed_x, ball_speed_y

def game_loop(screen, clock, font, difficulty):
    # Set AI speed based on difficulty
    ai_speed = {"easy": 4, "medium": 5, "hard": 6}.get(difficulty, 5)

    # Initial positions
    y_player = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    y_ai = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
    x_player = SCREEN_WIDTH // 3 + 30
    x_ai = SCREEN_WIDTH - 30 - PADDLE_WIDTH
    x_ball, y_ball, ball_speed_x, ball_speed_y = reset_ball(difficulty)

    player_points = 0
    ai_points = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Check if ESC is pressed
                    return True  # Return to the menu

        screen.fill(BLACK)

        # Update hand position and draw webcam feed
        new_pos_y = update_webcam(screen)
        if new_pos_y is not None:
            y_player = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, new_pos_y - PADDLE_HEIGHT // 2))

        # AI movement
        y_ai = handle_ai_movement(y_ai, y_ball, ai_speed)

        # Ball movement
        x_ball, y_ball, ball_speed_x, ball_speed_y = handle_ball_movement(
            x_ball, y_ball, ball_speed_x, ball_speed_y
        )

        # Collision with player's paddle
        if check_paddle_collision(x_ball - BALL_RADIUS, y_ball, x_player, y_player):
            ball_speed_x *= -1
            x_ball = x_player + PADDLE_WIDTH + BALL_RADIUS  # Move ball outside the paddle

        # Collision with AI's paddle
        if check_paddle_collision(x_ball + BALL_RADIUS, y_ball, x_ai, y_ai):
            ball_speed_x *= -1
            x_ball = x_ai - BALL_RADIUS  # Move ball outside the paddle

        # Scoring
        if x_ball < SCREEN_WIDTH // 3:  # Player missed
            ai_points += 1
            x_ball, y_ball, ball_speed_x, ball_speed_y = reset_ball(difficulty)
            y_player = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2  # Reset player position
            y_ai = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2  # Reset AI position

        if x_ball > SCREEN_WIDTH:  # AI missed
            player_points += 1
            x_ball, y_ball, ball_speed_x, ball_speed_y = reset_ball(difficulty)
            y_player = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2  # Reset player position
            y_ai = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2  # Reset AI position

        # Check if either player or AI has scored 5 points
        if player_points == 5 or ai_points == 5:
            return True  # Return to the menu

        # Draw game elements
        pygame.draw.rect(screen, WHITE, (x_player, y_player, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.rect(screen, WHITE, (x_ai, y_ai, PADDLE_WIDTH, PADDLE_HEIGHT))
        pygame.draw.circle(screen, GREEN, (x_ball, y_ball), BALL_RADIUS)

        draw_score(screen, font, player_points, ai_points)

        pygame.display.flip()
        clock.tick(60)