import random
import pygame
from config import LIFE_HEIGHGT, LIFE_WIDTH, WIDTH, HEIGHT, METEOR_WIDTH, METEOR_HEIGHT, SHIP_WIDTH, SHIP_HEIGHT
from assets import SHIP_IMG, PEW_SOUND, METEOR_IMG, BULLET_IMG, EXPLOSION_ANIM

class Ship(pygame.sprite.Sprite):
    def __init__(self,groups,assets):
        # construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["ship_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.assets = assets

        # só será possóvel atirar uma vez a cada 500 ms
        self.last_shot = pygame.time.get_ticks()
        self.shoot_ticks = 500

    def update(self):
        # Atualização da posição da nave
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        # mantem dentro da tela
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        ## mantendo dentro da tela no fundo e em cima
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def shoot(self):
        # verifica se pode atirar
        now = pygame.time.get_ticks()
        # verifica quantos ticks se passaram desde o último tiro
        elapsed_ticks = now - self.last_shot

        if elapsed_ticks > self.shoot_ticks:
            # marca o tick da nova imagem
            self.last_shot = now 
            # a nova bala vai ser criada logo acima e no centro horizontal da nave
            new_bullet = Bullet(self.assets, self.rect.top, self.rect.centerx)
            self.groups["all_sprites"].add(new_bullet)
            self.groups["all_bullets"].add(new_bullet)
            self.assets["pew_sound"].play()

class Meteor(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["meteor_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
        self.rect.y = random.randint(-100, -METEOR_HEIGHT)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
            self.rect.y = random.randint(-100, -METEOR_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

class Meteor_roxo(pygame.sprite.Sprite):
    def __init__(self, assets):
        # Construtor da classe mãe (Sprite).
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["meteor_roxo_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
        self.rect.y = random.randint(-100, -METEOR_HEIGHT)
        self.speedx = random.randint(-3, 3)
        self.speedy = random.randint(2, 9)

    def update(self):
        # Atualizando a posição do meteoro
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # Se o meteoro passar do final da tela, volta para cima e sorteia
        # novas posições e velocidades
        if self.rect.top > HEIGHT or self.rect.right < 0 or self.rect.left > WIDTH:
            self.rect.x = random.randint(0, WIDTH-METEOR_WIDTH)
            self.rect.y = random.randint(-100, -METEOR_HEIGHT)
            self.speedx = random.randint(-3, 3)
            self.speedy = random.randint(2, 9)

# classe bullet que representa os tiros
class Bullet(pygame.sprite.Sprite):
    # construtor da classe
    def __init__(self,assets,bottom,centerx):
        # contrutor da classe mãe (sprite)
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["bullet_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

        # coloca no lugar inicial definido em x,y do contrutor
        self.rect.centerx = centerx
        self.rect.bottom = bottom
        self.speedy = -10 # velocidade fixa para cima

    def update(self):
        # a bala só se move no eixo y
        self.rect.y += self.speedy

        # se o tiro passar do inicio da tela, morre
        if self.rect.bottom < 0:
            self.kill()

# classe que representa uma explosão do meteoro
class Explosion(pygame.sprite.Sprite):
    # construtor da classe
    def __init__(self,center,assets):
        # contrutor da classe mãe
        pygame.sprite.Sprite.__init__(self)

        # armazena a animação de explosão
        self.explosion_anim = assets["explosion_anim"]

        # inicia o processo de animação colocando a primeira imagem na tela
        self.frame = 0
        self.image = self.explosion_anim[self.frame] # pega a primeira imagem
        self.rect = self.image.get_rect()
        self.rect.center = center # posiciona o centro da imagem

        # guarda o tick da primeira imagem, ou seja, o momento em que a primeira imagem foi mostrada
        self.last_update = pygame.time.get_ticks()

        # controle de ticks de anomação: troca da imagem a cada self.frame_ticks milissegundos
        # quando pygame.time.get_ticks() - self.last_update > self.frame_ticks a
        # próxima imagem da animação será mostrada 
        self.frame_ticks = 50

    def update(self):
        # verifica o tick atual
        now = pygame.time.get_ticks()
        # verifica quantos ticks se passaram desde a altima mudança de frame
        elapsed_ticks = now - self.last_update

        # se já está na hora de mudar a imagem, então ...
        if elapsed_ticks > self.frame_ticks:
            # marca o tick da nova imagem
            self.last_update = now
            # avança um quadr0
            self.frame += 1

            # verifica se já chegou no final da animação
            if self.frame == len(self.explosion_anim):
                # se sim, acabou a explosão
                self.kill()
            else:
                # se não chegou no fim da explosão, troca de imagem
                center = self.rect.center
                self.image = self.explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Heart(pygame.sprite.Sprite):
    def __init__(self,assets):
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["life_img"]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0,30)
        self.rect.y = 0
        self.speedx = random.randint(-3,3)
        self.speedy = random.randint(2, 5)

    def update(self):
        # atualiza a posição do item 
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        # item não sair da tela pela lateral
        if self.rect.x <= 0 or self.rect.x >= WIDTH:
            self.speedx *= -1