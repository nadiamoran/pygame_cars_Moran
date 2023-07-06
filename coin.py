import pygame, random
from config import *

coins_group = pygame.sprite.Group()

class Coin(pygame.sprite.Sprite):
    def __init__(self, image_path, size, posicion):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = posicion
        self.speed = random.randint(2,3)

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > screen.get_width():
            self.kill()

    
def crear_coin():
    global coin_creation_timer
    global num_monedas_creadas


    # Código para crear y agregar monedas
    
    image_path = path_coin  # Ruta de la imagen de la moneda
    coin_size = (30, 30)  # Tamaño de la moneda (ancho y alto en píxeles)

    if num_monedas_creadas < num_monedas_total:
        current_time = pygame.time.get_ticks()
        if current_time - coin_creation_timer >= coin_intervalos:
            # Asignar una posición aleatoria a la moneda dentro del área permitida
            coin_position = (random.randint(200, screen.get_width() - coin_size[0] - 200),
                            random.randint(-400, -30))  # Posición inicial arriba de la pantalla

            # Crear una instancia de la clase Coin con la imagen cargada, tamaño y posición
            coin = Coin(image_path, coin_size, coin_position)

            # Agregar la moneda al grupo coins_group
            coins_group.add(coin)

            num_monedas_creadas += 1
            coin_creation_timer = current_time