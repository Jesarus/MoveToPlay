import pygame
from config import WHITE, SCREEN_WIDTH

def draw_score(screen, font, player_points, ai_points):
    """Draw the scoreboard at the top of the screen."""
    text = font.render(f"{player_points}   x   {ai_points}", True, WHITE)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

def render_text_centered(screen, font, text, color, x_center, y_center):
    """Render text centered at a specific position."""
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x_center - rendered_text.get_width() // 2, y_center - rendered_text.get_height() // 2))