import pygame
from random import choice, randint

class Fondo(pygame.sprite.Sprite):
    def __init__(self, grupos, factor_escala):
        super().__init__(grupos)
        imagen_fondo = pygame.image.load('Graficos/escenario/fondo.png').convert()
 
        altura_completa = imagen_fondo.get_height() * factor_escala
        ancho_completo = imagen_fondo.get_width() * factor_escala
        imagen_tamaño_completo = pygame.transform.scale(imagen_fondo, (ancho_completo, altura_completa))
        
        self.image = pygame.Surface((ancho_completo * 2, altura_completa))
        self.image.blit(imagen_tamaño_completo, (0, 0))
        self.image.blit(imagen_tamaño_completo, (ancho_completo, 0))
 
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)
 
    def update(self, dt):
        self.pos.x -= 300 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)

import pygame
from settings import *

class Suelo(pygame.sprite.Sprite):
    def __init__(self, grupos, factor_escala):
        super().__init__(grupos)
        self.tipo_sprite = 'suelo'
        
        # imagen
        superficie_suelo = pygame.image.load('Graficos/escenario/ground.png').convert_alpha()
        self.image = pygame.transform.scale(superficie_suelo, pygame.math.Vector2(superficie_suelo.get_size()) * factor_escala)
        
        # posición
        self.rect = self.image.get_rect(midbottom=(0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)
 
        # máscara
        self.mask = pygame.mask.from_surface(self.image)
 
    def update(self, dt):
        self.pos.x -= 360 * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
 
        self.rect.x = round(self.pos.x)


class Aguila(pygame.sprite.Sprite):
    def __init__(self, grupos, factor_escala):
        super().__init__(grupos)
 
        # imagen 
        self.importar_frames(factor_escala)
        self.indice_frame = 0
        self.image = self.frames[self.indice_frame]
 
        # rect
        self.rect = self.image.get_rect(midleft=(WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
 
        # movimiento
        self.gravedad = 600
        self.direccion = 0
 
        self.mask = pygame.mask.from_surface(self.image)
 
        #Sonido del Salto
        self.sonido_salto = pygame.mixer.Sound('Sonidos/jump.wav')
        self.sonido_salto.set_volume(0.1)
 
    def importar_frames(self, factor_escala):
        self.frames = []
        for i in range(3):
            superficie = pygame.image.load(f'Graficos/Aguila/aguila{i}.png').convert_alpha()
            superficie_escalada = pygame.transform.scale(superficie, pygame.math.Vector2(superficie.get_size()) * factor_escala)
            self.frames.append(superficie_escalada)
 
    def aplicar_gravedad(self, dt):
        self.direccion += self.gravedad * dt
        self.pos.y += self.direccion * dt
        self.rect.y = round(self.pos.y)
 
    def saltar(self):
        self.sonido_salto.play()
        self.direccion = -400
 
    def animar(self, dt):
        self.indice_frame += 10 * dt
        if self.indice_frame >= len(self.frames):
            self.indice_frame = 0
        self.image = self.frames[int(self.indice_frame)]
 
    def rotar(self):
        aguila_rotada = pygame.transform.rotozoom(self.image, -self.direccion * 0.06, 1)
        self.image = aguila_rotada
        self.mask = pygame.mask.from_surface(self.image)
 
    def update(self, dt):
        self.aplicar_gravedad(dt)
        self.animar(dt)
        self.rotar()

class Obstaculo(pygame.sprite.Sprite):
    def __init__(self, grupos, factor_escala):
        super().__init__(grupos)
        self.tipo_sprite = 'obstaculo'
 
        orientacion = choice(('arriba', 'abajo'))
        superficie = pygame.image.load(f'Graficos/Obstaculos/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(superficie, pygame.math.Vector2(superficie.get_size()) * factor_escala)
        
        x = WINDOW_WIDTH + randint(40, 100)
 
        if orientacion == 'arriba':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom=(x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop=(x, y))
 
        self.pos = pygame.math.Vector2(self.rect.topleft)
 
        self.mask = pygame.mask.from_surface(self.image)
 
    def update(self, dt):
        self.pos.x -= 400 * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
