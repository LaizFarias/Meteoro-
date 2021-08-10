# ===== Inicialização =====
# ----- Importa e inicia pacotes
import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
WIDTH = 480
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Navinha')

# ----- Inicia assets
METEOR_WIDTH = 50
METEOR_HEIGHT = 38
SHIP_WIDTH = 50
SHIP_HEIGHT = 38
assets = {}
assets["background"] = pygame.image.load("assets/img/starfield.png").convert()
assets["meteor_img"] = pygame.image.load("assets/img/meteorBrown_med1.png").convert_alpha()
assets["meteor_img"] = pygame.transform.scale(assets["meteor_img"], (METEOR_WIDTH, METEOR_HEIGHT))
assets["meteor_roxo_img"] = pygame.image.load("assets/img/asteroid_roxo.png").convert_alpha()
assets["meteor_roxo_img"] = pygame.transform.scale(assets["meteor_roxo_img"], (METEOR_WIDTH, METEOR_HEIGHT))
assets["ship_img"] = pygame.image.load("assets/img/playerShip1_orange.png").convert_alpha()
assets["ship_img"] = pygame.transform.scale(assets["ship_img"], (SHIP_WIDTH, SHIP_HEIGHT))
assets["bullet_img"] = pygame.image.load("assets/img/laserRed16.png").convert_alpha()

# carrega os sons do jogo
pygame.mixer.music.load("assets/snd/tgfcoder-FrozenJam-SeamlessLoop.ogg")
pygame.mixer.music.set_volume(0.4)
boom_sound = pygame.mixer.Sound("assets/snd/expl3.wav")
destroy_sound = pygame.mixer.Sound("assets/snd/expl6.wav")
assets["pew_sound"] = pygame.mixer.Sound("assets/snd/pew.wav")

# ----- Inicia estruturas de dados
# Definindo os novos tipos
class Ship(pygame.sprite.Sprite):
    def __init__(self,groups,assets):
        # construtor da classe mãe (Sprite)
        pygame.sprite.Sprite.__init__(self)

        self.image = assets["ship_img"]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0
        self.groups = groups
        self.assets = assets

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

game = True
# Variável para o ajuste de velocidade
clock = pygame.time.Clock()
FPS = 30

# criando grupo de meteoros normais
all_sprites = pygame.sprite.Group()
all_meteors = pygame.sprite.Group()
# criando grupo de meteoros roxos
all_meteors_roxo = pygame.sprite.Group()
# criando as balas
all_bullets = pygame.sprite.Group()
groups = {}
groups["all_sprites"] = all_sprites
groups["all_meteors"] = all_meteors
groups["all_meteors_roxo"] = all_meteors_roxo
groups["all_bullets"] = all_bullets

# criando o jogador
player = Ship(groups,assets)
all_sprites.add(player)

# criando os meteoros normais
for i in range(6):
    meteor = Meteor(assets)
    all_sprites.add(meteor)
    all_meteors.add(meteor)

# criando grupo de meteoros roxos
all_meteors_roxo = pygame.sprite.Group()
# criando os meteoros
for i in range(3):
    meteor_roxo = Meteor_roxo(assets)
    all_sprites.add(meteor_roxo)
    all_meteors_roxo.add(meteor_roxo)

# ===== Loop principal =====
pygame.mixer.music.play(loops = -1)

while game:
    clock.tick(FPS)

    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False
        # verifica se apertou alguma tecla
        if event.type == pygame.KEYDOWN:
            # dependendo da tecla, altera a valocidade
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

    # verifica se houve colisão entre o tiro e o meteoro comum
    hits = pygame.sprite.groupcollide(all_meteors,all_bullets,True, True)
    for meteor in hits:
        # o meteoro é destuido e precisa ser recriado
        m = Meteor(assets)
        all_sprites.add(m)
        all_meteors.add(m)
    
    # verifica se houve colisão entre o tiro e o meteoro roxo
    hits_roxo = pygame.sprite.groupcollide(all_meteors_roxo,all_bullets,True, True)
    for meteor in hits_roxo:
        # o meteoro é destuido e precisa ser recriado
        m = Meteor_roxo(assets)
        all_sprites.add(m)
        all_meteors_roxo.add(m)  

    # verifica se houve colisão entre a nave e o meteoro comum
    hits = pygame.sprite.spritecollide(player,all_meteors, True)
    if len(hits) > 0:
        boom_sound.play()
        time.sleep(1) # precisa esperar se não fecha
        game = False

    # verifica se houve colisão entre a nave e o meteoro roxo
    hits_roxo = pygame.sprite.spritecollide(player,all_meteors_roxo, True)
    if len(hits_roxo) > 0:
        boom_sound.play()
        time.sleep(1)
        game = False

    # ----- Gera saídas
    window.fill((0, 0, 0))  # Preenche com a cor branca
    window.blit(assets["background"], (0, 0))
    # Desenhando meteoros 
    all_sprites.draw(window)

    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados