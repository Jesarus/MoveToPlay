import pygame
from config import LARGURA_TELA, ALTURA_TELA, BRANCO, PRETO
from game import game_loop
from vision import release_resources, wait_for_hand_detection
from utils import render_text_centered

def splash_screen(tela, clock):
    """Display the splash screen with options to start or exit the game."""
    fonte_titulo = pygame.font.SysFont(None, 72)
    fonte_opcoes = pygame.font.SysFont(None, 48)

    rodando = True
    while rodando:
        tela.fill(PRETO)

        # Render title
        titulo = fonte_titulo.render("Pong com a Mão 🖐️", True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 4))

        # Render options
        opcao_novo_jogo = fonte_opcoes.render("1. Novo Jogo", True, BRANCO)
        opcao_sair = fonte_opcoes.render("2. Sair", True, BRANCO)
        tela.blit(opcao_novo_jogo, (LARGURA_TELA // 2 - opcao_novo_jogo.get_width() // 2, ALTURA_TELA // 2))
        tela.blit(opcao_sair, (LARGURA_TELA // 2 - opcao_sair.get_width() // 2, ALTURA_TELA // 2 + 60))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Start new game
                    return True
                if event.key == pygame.K_2:  # Exit game
                    rodando = False
                    return None

        clock.tick(60)

def select_difficulty(tela, clock):
    """Display a screen to select the AI difficulty level."""
    fonte_titulo = pygame.font.SysFont(None, 72)
    fonte_opcoes = pygame.font.SysFont(None, 48)

    rodando = True
    while rodando:
        tela.fill(PRETO)

        # Render title
        titulo = fonte_titulo.render("Selecione a Dificuldade", True, BRANCO)
        tela.blit(titulo, (LARGURA_TELA // 2 - titulo.get_width() // 2, ALTURA_TELA // 4))

        # Render difficulty options
        opcao_facil = fonte_opcoes.render("1. Fácil", True, BRANCO)
        opcao_medio = fonte_opcoes.render("2. Médio", True, BRANCO)
        opcao_dificil = fonte_opcoes.render("3. Difícil", True, BRANCO)
        tela.blit(opcao_facil, (LARGURA_TELA // 2 - opcao_facil.get_width() // 2, ALTURA_TELA // 2))
        tela.blit(opcao_medio, (LARGURA_TELA // 2 - opcao_medio.get_width() // 2, ALTURA_TELA // 2 + 60))
        tela.blit(opcao_dificil, (LARGURA_TELA // 2 - opcao_dificil.get_width() // 2, ALTURA_TELA // 2 + 120))

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
    """Main function to run the game."""
    pygame.init()
    tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    pygame.display.set_caption("Pong com a Mão 🖐️")
    clock = pygame.time.Clock()

    # Show splash screen
    if splash_screen(tela, clock):
        # Select difficulty
        difficulty = select_difficulty(tela, clock)
        if difficulty is None:
            return  # Exit if the user quits during difficulty selection

        # Wait for hand detection
        if wait_for_hand_detection(tela, clock):
            fonte = pygame.font.SysFont(None, 48)
            game_loop(tela, clock, fonte, difficulty)

    pygame.quit()
    release_resources()

if __name__ == "__main__":
    main()