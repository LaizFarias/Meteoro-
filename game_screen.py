import pygame
from config import*
from assets import*
from sprites import*

def game_screen(window):
    # Variável para o ajuste de velocidade
    clock = pygame.time.Clock()

    assets = load_assets()

    # criando grupo de meteoros normais
    all_sprites = pygame.sprite.Group()
    all_meteors = pygame.sprite.Group()
    # criando grupo de meteoros roxos
    all_meteors_roxo = pygame.sprite.Group()
    # criando as balas
    all_bullets = pygame.sprite.Group()
    # criando o item de vida
    all_lifes_item = pygame.sprite.Group()

    groups = {}
    groups["all_sprites"] = all_sprites
    groups["all_meteors"] = all_meteors
    groups["all_meteors_roxo"] = all_meteors_roxo
    groups["all_bullets"] = all_bullets
    groups["life_img"] = all_lifes_item 

    # criando o jogador
    player = Ship(groups,assets)
    all_sprites.add(player)

    # numero de meteoros normais
    NORMAL = 6
    # numero de meteoros roxos
    MATADOR = 1

    # criando os meteoros normais
    for i in range(NORMAL):
        meteor = Meteor(assets)
        all_sprites.add(meteor)
        all_meteors.add(meteor)

    # criando grupo de meteoros roxos
    all_meteors_roxo = pygame.sprite.Group()
    # criando os meteoros
    for i in range(MATADOR):
        meteor_roxo = Meteor_roxo(assets)
        all_sprites.add(meteor_roxo)
        all_meteors_roxo.add(meteor_roxo)

    DONE = 0
    PLAYING = 1
    EXPLODING = 2
    state = PLAYING

    keys_down = {}
    score = 0
    lives = 3

    # ===== Loop principal =====
    pygame.mixer.music.play(loops = -1)

    while state != DONE:
        clock.tick(FPS)

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            # SÓ VERIFICA O TECLADO SE ESTÁ NO MODO JOGO
            if state == PLAYING:
                # verifica se apertou alguma tecla
                if event.type == pygame.KEYDOWN:
                    # dependendo da tecla, altera a valocidade
                    keys_down[event.key] = True
                    if event.key == pygame.K_LEFT:
                        player.speedx -= 8
                    if event.key == pygame.K_RIGHT:
                        player.speedx += 8
                    if event.key == pygame.K_UP:
                        player.speedy -= 8
                    if event.key == pygame.K_DOWN:
                        player.speedy += 8
                    if event.key == pygame.K_SPACE:
                        player.shoot()
                # verifica se soltou alguma tecla
                if event.type == pygame.KEYUP:
                    # dependendo da tecla, altera a valocidade
                    if event.key in keys_down and keys_down[event.key]:
                        if event.key == pygame.K_LEFT:
                            player.speedx += 8
                        if event.key == pygame.K_RIGHT:
                            player.speedx -= 8
                        if event.key == pygame.K_UP:
                            player.speedy += 8
                        if event.key == pygame.K_DOWN:
                            player.speedy -= 8

        # ----- Atualiza estado do jogo
        # Atualizando a posição dos meteoros
        all_sprites.update()

        if state == PLAYING:
            # verifica se houve colisão entre o tiro e o meteoro comum
            hits = pygame.sprite.groupcollide(all_meteors,all_bullets,True, True)
            for meteor in hits:
                # o meteoro é destuido e precisa ser recriado
                assets["destroy_sound"].play()
                m = Meteor(assets)
                all_sprites.add(m)
                all_meteors.add(m)

                # no lugar do meteoro antigo, adicionar uma explosão
                explosao = Explosion(meteor.rect.center,assets)
                all_sprites.add(explosao)

                # se score for m1000 add meteoro roxo novo e lança item de vida
                # se score for m2500 add meteoro comum

                # ganhou pontos!
                score += 100
                if score % 1000 == 0:
                    m = Meteor_roxo(assets)
                    all_sprites.add(m)
                    all_meteors_roxo.add(m)
                    # parte do item de vida
                    item = Heart(assets)
                    all_sprites.add(item)
                    all_lifes_item.add(item)

                if score % 2500 == 0:
                    m = Meteor(assets)
                    all_sprites.add(m)
                    all_meteors.add(m)
            
            # verifica se houve colisão entre o tiro e o meteoro roxo
            hits_roxo = pygame.sprite.groupcollide(all_meteors_roxo,all_bullets,True, True)
            for meteor in hits_roxo:
                # o meteoro é destuido e precisa ser recriado
                assets["destroy_sound"].play()
                m = Meteor_roxo(assets)
                all_sprites.add(m)
                all_meteors_roxo.add(m)  

                explosao = Explosion(meteor.rect.center,assets)
                all_sprites.add(explosao)

                # ganhou pontos !
                score += 100
                if score % 1000 == 0:
                    m = Meteor_roxo(assets)
                    all_sprites.add(m)
                    all_meteors_roxo.add(m)
                    # parte do item de vida
                    item = Heart(assets)
                    all_sprites.add(item)
                    all_lifes_item.add(item)

                if score % 2500 == 0:
                    m = Meteor(assets)
                    all_sprites.add(m)
                    all_meteors.add(m)

            # verifica se houve colisão entre a nave e o meteoro comum
            hits = pygame.sprite.spritecollide(player,all_meteors, True)
            if len(hits) > 0:
                assets["boom_sound"].play()
                player.kill()
                lives -= 1
                explosao = Explosion(player.rect.center,assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_ticks = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks*len(explosao.explosion_anim) + 400

            # verifica se houve colisão entre a nave e o meteoro roxo, que tira 2 vidas
            hits_roxo = pygame.sprite.spritecollide(player,all_meteors_roxo, True)
            if len(hits_roxo) > 0:
                assets["boom_sound"].play()
                player.kill()
                lives -= 2
                explosao = Explosion(player.rect.center,assets)
                all_sprites.add(explosao)
                state = EXPLODING
                keys_down = {}
                explosion_ticks = pygame.time.get_ticks()
                explosion_duration = explosao.frame_ticks*len(explosao.explosion_anim) + 400

            # vamos verificar a colisão da nave com o item de vida
            life_up = pygame.sprite.spritecollide(player,all_lifes_item,True)
            if len(life_up) > 0:
                lives += 1
                #all_lifes_item.death()
        
        elif state == EXPLODING:
            now = pygame.time.get_ticks()
            if now - explosion_ticks > explosion_duration:
                if lives <= 0:
                    state = DONE
                else:
                    state = PLAYING
                    player = Ship(groups, assets)
                    all_sprites.add(player)

        # ----- Gera saídas
        window.fill((0, 0, 0))  # Preenche com a cor branca
        window.blit(assets["background"], (0, 0))
        # Desenhando meteoros 
        all_sprites.draw(window)

        # Desenhando o score
        text_surface = assets["score_font"].render("{:08d}".format(score), True, (255, 255, 0))
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH / 2,  10)
        window.blit(text_surface, text_rect)

        # Desenhando as vidas
        text_surface = assets["score_font"].render(chr(9829) * lives, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.bottomleft = (10, HEIGHT - 10)
        window.blit(text_surface, text_rect)

        pygame.display.update()  # Mostra o novo frame para o jogador