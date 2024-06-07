import pygame, sys, time
from settings import *
from sprites import Fondo, Suelo, Aguila, Obstaculo

class Juego:
    def __init__(self):
        
        #Inicialización de Pygame y configuración de la ventana
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Aguila del Desierto')
        self.clock = pygame.time.Clock()
        self.active = True

        # Grupos de Sprites
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Escala y carga de las imagenes
        fondo_height = pygame.image.load('Graficos/escenario/fondo.png').get_height()
        self.scale_factor = WINDOW_HEIGHT / fondo_height

        # Configuracion de Sprites 
        Fondo(self.all_sprites, self.scale_factor)
        Suelo([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.aguila = Aguila(self.all_sprites, self.scale_factor / 1.7)

        # Timer para los obstaculos
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        # Texto Puntuacion
        self.font = pygame.font.Font('Graficos/fuente/BD_Cartoon_Shout.ttf', 30)
        self.score = 0
        self.start_offset = 0

        # Menu para empezar a jugar
        self.menu_surf = pygame.image.load('Graficos/ui/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Musica de fondo
        self.music = pygame.mixer.Sound('Sonidos/music.wav')
        self.music.set_volume(0.2)
        self.music.play(loops=-1)

    def colisiones(self):
        if pygame.sprite.spritecollide(self.aguila, self.collision_sprites, False, pygame.sprite.collide_mask) \
                or self.aguila.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.tipo_sprite == 'obstaculo':
                    sprite.kill()
            self.active = False
            self.aguila.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 1.5)

        score_surf = self.font.render(str(self.score), True, 'black')
        score_rect = score_surf.get_rect(midtop=(WINDOW_WIDTH / 2, y))
        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:

            # Delta time
            dt = time.time() - last_time
            last_time = time.time()

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.aguila.saltar()
                    else:
                        self.aguila = Aguila(self.all_sprites, self.scale_factor / 1.7)
                        self.active = True
                        self.start_offset = pygame.time.get_ticks()

                if event.type == self.obstacle_timer and self.active:
                    Obstaculo([self.all_sprites, self.collision_sprites], self.scale_factor * 1.1)

            # Game logic
            self.display_surface.fill('black')
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()

            if self.active: 
                self.colisiones()
            else:
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    juego = Juego()
    juego.run()
