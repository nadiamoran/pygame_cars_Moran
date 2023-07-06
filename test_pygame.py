import pygame
import sqlite3
from config import *
from auto import Auto
import sys, random, math
from button import *
from enemigo_juego import Enemigo
from coin import *
import json


pygame.init()

# Tamaño de pantalla
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

fondo = pygame.image.load(path_ruta).convert()
fondo = pygame.transform.scale(fondo, screen_size)
fondo_alto = fondo.get_height()


#sonidos
sound_choque = pygame.mixer.Sound(path_sonido_colision)
sound_coin = pygame.mixer.Sound(path_sonido_coin)
sound_inicio = pygame.mixer.Sound(path_sonido_inicio)
sound_acelerar = pygame.mixer.Sound(path_sonido_acelerar)


auto = Auto(path_auto, SIZE_AUTO,(screen.get_width()//2, screen.get_height()-20))
clock = pygame.time.Clock() #controlar la velocidad


menu_principal = pygame.image.load(image_folder + "menuCar.jpg").convert()

def get_font(size):
    return pygame.font.Font(path_fuente, size)

def guardar_ranking(path_ranking_json, player, score):
    ranking = {
        "player": player,
        "score": str(score)
    }
    with open(path_ranking_json, "a") as archivo:
        json.dump(ranking, archivo)
        archivo.write("\n")


def mostrar_puntaje():
    font = pygame.font.Font(path_fuente, 20)
    text = font.render("SCORE: " + str(score), True, (255, 255, 255))
    screen.blit(text, (10, 40))

def mostrar_vidas():
    font = pygame.font.Font(path_fuente, 25)
    text = font.render("Vidas: " + str(vidas), True, (255, 255, 255))
    screen.blit(text, (10, 10))

def mostrar_game_over():
    gameover_imagen = pygame.image.load(image_folder + "gameover.png").convert_alpha()
    screen.blit(gameover_imagen, (0, 0))
    pygame.display.flip()
    pygame.time.delay(1000)  # Pausa el juego durante 3 segundos
    font = pygame.font.Font(path_fuente,40)

    player_name = ""

    # Bucle principal para ingresar el nombre
    entering_name = True
    while entering_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entering_name = False
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

        # Limpiar la ventana
        screen.fill((0, 0, 0))

        text = font.render("GAME OVER: " + "Score:" + str(score), True, (255, 255, 255))
        screen.blit(text, (120, 280))
        # Mostrar el nombre ingresado dentro del rectángulo
        name_text = font.render("Player Name: " + player_name, True, (255, 255, 255))
        screen.blit(name_text, (120 + 10, 360 + 10))

        pygame.display.flip()

    guardar_ranking(path_ranking_json, player_name, score)

    pygame.display.flip()

    main_menu()

enemigos_group = pygame.sprite.Group()

def ranking():
    while True:
        sound_inicio.play()
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        
        screen.fill("white")

        RANKING_TEXT = get_font(60).render("- - - TOP RANKING - - -" , True,"Black") 

        titulo_text = get_font(30).render(f"   TOP       PLAYER       SCORE", True, "Black")
        titulo_rect = titulo_text.get_rect(center=(400, 130))

        OPTIONS_RECT =  RANKING_TEXT.get_rect(center=(400, 50))
        
        screen.blit(RANKING_TEXT, OPTIONS_RECT)
        screen.blit(titulo_text, titulo_rect)

        OPTIONS_BACK = Button(image=None, pos=(690, 560),
                              text_input="BACK", font=get_font(60), base_color="Black", hovering_color="Pink")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    sound_inicio.stop()
                    main_menu()


        lista_score_ordenado = []
        with open(path_ranking_json, "r") as archivo: #modo lectura
        #ordeno los datos por score en orden descendente
            #Mostrar los datos en forma descendente
            cadena = ""
            for i in archivo:
                cadena += i
            # Separar los elementos utilizando "{"
            elementos = cadena.split("{")
            # Filtrar los elementos que contienen "}"
            elementos = [elemento for elemento in elementos if "}" in elemento]
            # Ordenar los elementos por score en orden descendente
            elementos_ordenados = sorted(elementos, key=lambda x: int(x.split('"score": "')[1].split('"')[0]), reverse=True)
            # Imprimir los elementos ordenados
            for elemento in elementos_ordenados:
                elemento = "{" + elemento.strip()
                lista_score_ordenado.append(elemento)

            y=180
            top = 1
            for dato in lista_score_ordenado:
                diccionario = json.loads(dato)
                player = diccionario["player"]
                score = diccionario["score"]

                if top <= 10:
                    top_text = get_font(25).render(f"{top}", True, "Black")
                    top_rect = top_text.get_rect(center=(260, y))
                    player_text = get_font(25).render(f"{player}", True, "Black")
                    player_rect = player_text.get_rect(center=(400, y))
                    score_text = get_font(25).render(f"{score}", True, "Black")
                    score_rect = score_text.get_rect(center=(530, y))
                    top+=1

                screen.blit(top_text, top_rect)
                screen.blit(score_text, score_rect)
                screen.blit(player_text, player_rect)
                y+=30


        pygame.display.update()

def crear_enemigo():
    global timer

    if len(enemigos_group) < MAX_ENEMIGOS:  # Verificar la cantidad actual de enemigos
        timer += 1  # Incrementar el temporizador en cada iteración

        if timer >= FRECUENCIA_ENEMIGO:  # Controlar la frecuencia de aparición de los enemigos
            x = random.randint(auto.rect.left, auto.rect.right)  # Posición X aleatoria dentro del área del auto
            y = random.randint(-200, -50)  # Posición Y aleatoria arriba de la pantalla

            # Crear un enemigo con una imagen aleatoria
            if random.random() < 0.5:
                enemigo = Enemigo(image_folder + "taxi.png", SIZE_ENEMIGO, (x, y))
            else:
                enemigo = Enemigo(image_folder + "policia.png", SIZE_ENEMIGO, (x, y))

            enemigos_group.add(enemigo)

            timer = 0  # Reiniciar el temporizador después de crear un nuevo enemigo

            # Establecer posición Y negativa para que aparezcan arriba
            enemigo.rect.y = y

def enemigo_colision():
    global vidas
    global score

    colisiones = pygame.sprite.spritecollide(auto, enemigos_group, True)
    colisiones_coins = pygame.sprite.spritecollide(auto, coins_group, True)

    if colisiones:
        sound_acelerar.stop()
        sound_choque.play()
        vidas -= 10  # Descuenta un 10% de vida por colisión con un enemigo
        explosion_imagen = pygame.image.load(image_folder + "explosion.png").convert_alpha()
        explosion_rect = explosion_imagen.get_rect()
        explosion_rect.center = colisiones[0].rect.center  # Posición de la primera colisión
        screen.blit(explosion_imagen, explosion_rect)

    if colisiones_coins:
        sound_coin.play()
        score += 10


def start_game():
    global pos_fondo, timer, vidas, score
    pos_fondo = 0
    timer = 0
    vidas = 50
    score = 0

    while True:

        clock.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    auto.velocidad_x = -SPEED_AUTO
                    print(auto.velocidad_x)
                    sound_acelerar.play()
                    auto.image = pygame.image.load(path_auto_mov_izq).convert_alpha()
                    auto.image = pygame.transform.scale(auto.image, (auto.rect.width, auto.rect.height))
                elif evento.key == pygame.K_RIGHT:
                    auto.velocidad_x = SPEED_AUTO
                    print(auto.velocidad_x)
                    sound_acelerar.play()
                    auto.image = pygame.image.load(path_auto_mov_der).convert_alpha()
                    auto.image = pygame.transform.scale(auto.image, (auto.rect.width, auto.rect.height))

                elif evento.key == pygame.K_UP:
                    auto.velocidad_y = -SPEED_AUTO
                    print(auto.velocidad_y)
                    sound_acelerar.play()
                    auto.image = pygame.image.load(path_auto_acel).convert_alpha()
                    auto.image = pygame.transform.scale(auto.image, (auto.rect.width, auto.rect.height))
                elif evento.key == pygame.K_DOWN:
                    auto.velocidad_y = SPEED_AUTO
                    print(auto.velocidad_y)
                    sound_acelerar.play()
                elif evento.key == pygame.K_SPACE:
                        sound_acelerar.stop()
                        print("tocaste pausa")
                        flag_pausa = True
                        while flag_pausa:
                            sound_inicio.play()
                            for evento_pausa in pygame.event.get():
                                if evento_pausa.type == pygame.KEYDOWN:
                                    if evento_pausa.key == pygame.K_SPACE:
                                        flag_pausa = False
                                        sound_inicio.stop()
                            
                            TEXT_PAUSA = get_font(80).render("----PAUSA----" , True,"White") 
                            PAUSA_RECT = TEXT_PAUSA.get_rect(center=(400, 300))
                            screen.blit(TEXT_PAUSA, PAUSA_RECT)
                            pygame.display.update()
                            print("El juego esta pausado")

            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT:
                    auto.velocidad_x = 0
                    print(auto.velocidad_x)
                elif evento.key == pygame.K_RIGHT:
                    auto.velocidad_x = 0
                    print(auto.velocidad_x)

                elif evento.key == pygame.K_UP:
                    auto.velocidad_y = 0
                    print(auto.velocidad_y)
                elif evento.key == pygame.K_DOWN:
                    auto.velocidad_y = 0
                    print(auto.velocidad_y)

        pos_fondo += 5

        if auto.rect.left <= 0:
            auto.rect.left = 0
        elif auto.rect.right > screen.get_width():
            auto.rect.right = screen.get_width()
        elif auto.rect.bottom > screen.get_height():
            auto.rect.bottom = screen.get_height()

        crear_enemigo()
        enemigos_group.update()

        crear_coin()
        coins_group.update()

        screen.blit(fondo, (0, pos_fondo))
        screen.blit(fondo, (0, pos_fondo - fondo_alto))

        mostrar_vidas()
        mostrar_puntaje()

        screen.blit(auto.image, auto.rect)
        auto.update()

        for enemigo in enemigos_group:
            enemigo.update()

        enemigos_group.draw(screen)
        auto.update()

        enemigo_colision()

        # Verificar si se necesita reiniciar la posición del fondo
        if pos_fondo >= fondo_alto:
            pos_fondo = 0

        if vidas <= 0:
            # Acción a realizar cuando las vidas llegan a cero (por ejemplo, reiniciar el juego o mostrar "Game Over")
            # Reiniciar el juego
            pos_fondo = 0
            timer = 0
            mostrar_game_over()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_RETURN:  # Si se presiona la tecla Enter
                main_menu()  # Regresar al menú principal

        colisiones_coins = pygame.sprite.spritecollide(auto, coins_group, True)

        if colisiones_coins:
            score += 10

        coins_group.update()
        coins_group.draw(screen)

        pygame.display.flip()
        clock.tick(50)



def options():
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        screen.fill("white")

        OPTIONS_TEXT = get_font(25).render("Para mover el auto tiene que utilizar las fechas del teclado.", True,
                                           "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(100, 150))
        screen.blit(OPTIONS_TEXT, OPTIONS_RECT)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="BACK", font=get_font(60), base_color="Black", hovering_color="Pink")

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        sound_inicio.play()
        screen.blit(menu_principal, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load(image_folder + "OptionsRect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(30), base_color="#3b3b3b", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load(image_folder + "OptionsRect.png"), pos=(640, 340),
                                text_input="Instrucciones", font=get_font(30), base_color="#3b3b3b",
                                hovering_color="White")
        RANKING_BUTTON = Button(image=pygame.image.load(image_folder + "OptionsRect.png"), pos=(640, 410),
                        text_input="Ranking Player", font=get_font(30), base_color="#3b3b3b",
                        hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load(image_folder + "OptionsRect.png"), pos=(640, 480),
                             text_input="QUIT", font=get_font(30), base_color="#3b3b3b", hovering_color="White")

        PLAY_BUTTON.changeColor(MENU_MOUSE_POS)
        OPTIONS_BUTTON.changeColor(MENU_MOUSE_POS)
        RANKING_BUTTON.changeColor(MENU_MOUSE_POS)
        QUIT_BUTTON.changeColor(MENU_MOUSE_POS)

        PLAY_BUTTON.update(screen)
        OPTIONS_BUTTON.update(screen)
        RANKING_BUTTON.update(screen)
        QUIT_BUTTON.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.time.wait(500)
                    sound_inicio.stop()
                    start_game()  # Llamar a la función "start_game()" para iniciar el juego
                elif OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_inicio.stop()
                    options()  # Llamar a la función "options()" para mostrar las instrucciones
                elif RANKING_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_inicio.stop()
                    ranking()  # Llamar a la función "ranking()" para mostrar el top de players
                elif QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_inicio.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()


