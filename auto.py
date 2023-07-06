import pygame
from config import *


class Auto(pygame.sprite.Sprite): #sprite, son los persponajes
    def __init__(self, path_image:str, size:tuple, midbottom:tuple):
        super().__init__()

        self.image = pygame.image.load(path_image).convert_alpha()  #surface levantada en una imagen
        self.image = pygame.transform.scale(self.image, (size))

        #siempre guardo el tamaño del rectangulo
        self.rect = self.image.get_rect()
        self.rect.midbottom = midbottom
        self.velocidad_x = 0
        self.velocidad_y = 0

        # Posición inicial del sprite
        self.x = 0
        self.y = 300

        # el jugador esta jugando
        self.playing = True

        # Aceleración y desaceleración gradual
        self.aceleracion = 0.2
        self.desaceleracion = 0.1


    def update(self):

        if self.playing:  #si esta jugando, se actualiza el movimiento
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

        if self.rect.left <= DISPLAY_LEFT:   #compruba si la auto no sobrepasa el limite izquierdo. Si sobrepasa se ejecuta la siguiente linea de codigo.
            self.rect.left = DISPLAY_LEFT  #Establece la posición izquierda de la auto en 0, evitando que se desplace más hacia la izquierda y se salga de la pantalla.
        elif self.rect.right >= DISPLAY_RIGHT:  #compruba si la auto no sobrepase el limite derecho. Si sobrepasa se ejecuta la siguiente linea de codigo.
            self.rect.right = DISPLAY_RIGHT  #Establece la posición derecha de la auto en el ancho de la pantalla, evitando que se desplace más hacia la derecha y se salga de la pantalla
        if self.rect.top <= DISPLAY_TOP:   #compruba si la auto no sobrepase el limite de arriba. Si sobrepasa se ejecuta la siguiente linea de codigo.
            self.rect.top = DISPLAY_TOP  #Establece la posición superior de la auto en 0, evitando que se desplace más hacia arriba y se salga de la pantalla.
        elif self.rect.bottom >= DISPLAY_BOTTOM:  #compruba si la auto no sobrepase el limite de abajo. Si sobrepasa se ejecuta la siguiente linea de codigo.
            self.rect.bottom = DISPLAY_BOTTOM  #Establece la posición inferior de la auto en el alto de la pantalla, evitando que se desplace más hacia abajo y se salga de la pantalla.