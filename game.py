import pygame
from config import *
from utils import desenhar_placar
from vision import atualizar_webcam

def handle_ai_movement(y_ia, y_bola, ai_speed):
    """Move the AI paddle based on the ball's position."""
    if y_ia + ALTURA_RAQUETE // 2 < y_bola:
        y_ia += ai_speed
    elif y_ia + ALTURA_RAQUETE // 2 > y_bola:
        y_ia -= ai_speed
    return max(0, min(ALTURA_TELA - ALTURA_RAQUETE, y_ia))

def handle_ball_movement(x_bola, y_bola, velocidade_bola_x, velocidade_bola_y):
    """Move the ball and handle collisions with the top and bottom walls."""
    x_bola += velocidade_bola_x
    y_bola += velocidade_bola_y

    # Collision with top and bottom
    if y_bola <= 0 or y_bola >= ALTURA_TELA:
        velocidade_bola_y *= -1

    return x_bola, y_bola, velocidade_bola_x, velocidade_bola_y

def check_paddle_collision(x_bola, y_bola, x_paddle, y_paddle):
    """Check if the ball collides with a paddle."""
    return (x_paddle <= x_bola <= x_paddle + LARGURA_RAQUETE and
            y_paddle < y_bola < y_paddle + ALTURA_RAQUETE)

def reset_ball():
    """Reset the ball to the center of the game area."""
    return LARGURA_TELA // 3 + (2 * LARGURA_TELA // 3) // 2, ALTURA_TELA // 2

def game_loop(tela, clock, fonte, difficulty):
    # Set AI speed based on difficulty
    ai_speed = {"easy": 4, "medium": 5, "hard": 6}.get(difficulty, 5)

    # Initial positions
    y_jogador = ALTURA_TELA // 2 - ALTURA_RAQUETE // 2
    y_ia = ALTURA_TELA // 2 - ALTURA_RAQUETE // 2
    x_jogador = LARGURA_TELA // 3 + 30
    x_ia = LARGURA_TELA - 30 - LARGURA_RAQUETE
    x_bola, y_bola = reset_ball()
    velocidade_bola_x = 5
    velocidade_bola_y = 5

    pontos_jogador = 0
    pontos_ia = 0

    rodando = True
    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        tela.fill(PRETO)

        # Update hand position and draw webcam feed
        nova_pos_y = atualizar_webcam(tela)
        if nova_pos_y is not None:
            y_jogador = max(0, min(ALTURA_TELA - ALTURA_RAQUETE, nova_pos_y - ALTURA_RAQUETE // 2))

        # AI movement
        y_ia = handle_ai_movement(y_ia, y_bola, ai_speed)

        # Ball movement
        x_bola, y_bola, velocidade_bola_x, velocidade_bola_y = handle_ball_movement(
            x_bola, y_bola, velocidade_bola_x, velocidade_bola_y
        )

        # Collision with player's paddle
        if check_paddle_collision(x_bola - RAIO_BOLA, y_bola, x_jogador, y_jogador):
            velocidade_bola_x *= -1

        # Collision with AI's paddle
        if check_paddle_collision(x_bola + RAIO_BOLA, y_bola, x_ia, y_ia):
            velocidade_bola_x *= -1

        # Scoring
        if x_bola < LARGURA_TELA // 3:  # Player missed
            pontos_ia += 1
            x_bola, y_bola = reset_ball()
        if x_bola > LARGURA_TELA:  # AI missed
            pontos_jogador += 1
            x_bola, y_bola = reset_ball()

        # Draw game elements
        pygame.draw.rect(tela, BRANCO, (x_jogador, y_jogador, LARGURA_RAQUETE, ALTURA_RAQUETE))
        pygame.draw.rect(tela, BRANCO, (x_ia, y_ia, LARGURA_RAQUETE, ALTURA_RAQUETE))
        pygame.draw.circle(tela, VERDE, (x_bola, y_bola), RAIO_BOLA)

        desenhar_placar(tela, fonte, pontos_jogador, pontos_ia)

        pygame.display.flip()
        clock.tick(60)