import pygame
from config import BRANCO, LARGURA_TELA

def desenhar_placar(tela, fonte, pontos_jogador, pontos_ia):
    """Draw the scoreboard at the top of the screen."""
    texto = fonte.render(f"{pontos_jogador}   x   {pontos_ia}", True, BRANCO)
    tela.blit(texto, (LARGURA_TELA // 2 - texto.get_width() // 2, 20))

def render_text_centered(tela, fonte, texto, cor, x_centro, y_centro):
    """Render text centered at a specific position."""
    texto_renderizado = fonte.render(texto, True, cor)
    tela.blit(texto_renderizado, (x_centro - texto_renderizado.get_width() // 2, y_centro - texto_renderizado.get_height() // 2))