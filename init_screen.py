from assets import*
import pygame
import random
from config import*

def init_screen(screen):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    # definindo o indice
    i = 0

    # fps da tela inicial
    FPS_sc = 1
    running = True

    assets = load_assets()

    while running:

        # Ajusta a velocidade do jogo.
        clock.tick(FPS_sc)

        # alterando imagem
        screen.blit(assets[STARTSC_ANIM][i%2],(0,0))
        # Processa os eventos (mouse, teclado, botão, etc).
        for event in pygame.event.get():
            # Verifica se foi fechado.
            if event.type == pygame.QUIT:
                state = QUIT
                running = False
            if event.type == pygame.KEYUP:
                state = GAME
                running = False
            
        pygame.display.update()
        i += 1

        # Depois de desenhar tudo, inverte o display.
        pygame.display.flip()

    return state