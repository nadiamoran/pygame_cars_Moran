# Define la clase Enemigo
import pygame
import random
from config import *

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, image_path, size, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = random.randint(2, 5)  # Velocidad aleatoria de movimiento vertical


    def update(self):
        self.rect.y += self.speed  # Mover el enemigo hacia abajo
        if self.rect.y > screen.get_height():  # Si el enemigo se sale de la pantalla
            self.kill()  # Eliminar el enemigo


