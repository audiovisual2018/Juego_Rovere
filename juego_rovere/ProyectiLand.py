
import pygame
import random
from pygame.locals import *
from random import randint
import os
import sys
import time

# ------------------------------
# Defino colores y extras
# ------------------------------

 
NEGRO    = (   0,   0,   0)
BLANCO   = ( 255, 255, 255)
ROJO     = ( 255,   0,   0)
AZUL     = (   0,   0, 255)


IMG_DIR = "imagenes"
SONIDO_DIR = "sonidos"

# ------------------------------
# Funciones
# ------------------------------


def cargar_imagen(nombre, dir_imagen, alpha=False):
    #Ruta de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    image = pygame.image.load(ruta)
   
    if alpha is True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image


def cargar_sonido(nombre, dir_sonido):
    ruta = os.path.join(dir_sonido, nombre)
    # Cargar el sonido
    sonido = pygame.mixer.Sound(ruta)

    return sonido


# ------------------------------
# Clases
# ------------------------------

 
class Enemigo(pygame.sprite.Sprite):
    #Aviones enemigos
    def __init__(self):
        # Llama al constructor de la clase padre (Sprite)
        super().__init__() 
        self.image = cargar_imagen("avion3.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
 
class Protagonista(pygame.sprite.Sprite):
    #Avion protagonista    
    def __init__(self):
        # Llama al constructor de la clase padre (Sprite)
        super().__init__() 
        self.image = cargar_imagen("avion.png", IMG_DIR, alpha=True)
        self.rect = self.image.get_rect()
         
    def update(self):
        #Actualiza la ubicación del protagonista.
        # Obtiene la posición actual del ratón. La devuelve como una lista de dos números.
        pos = pygame.mouse.get_pos()
     
        # Sitúa la posición x del protagonista en la posición x del ratón
        self.rect.x = pos[0] 
         
class Proyectil(pygame.sprite.Sprite):
    # Creo al proyectil del protagonista
    def __init__(self):
        #  Llama al constructor de la clase padre (Sprite)
        super().__init__() 
 
        self.image = pygame.Surface([4, 6])
        self.image.fill(BLANCO)
 
        self.rect = self.image.get_rect()
         
    def update(self):
        # Desplaza al proyectil
        self.rect.y -= 15



class Proyectilenemigo(pygame.sprite.Sprite):
    # Proyectil del enemigo
    def __init__(self):
        #  Llama al constructor de la clase padre (Sprite)
        super().__init__() 
        self.image = pygame.Surface([4, 6])
        self.image.fill(ROJO)
        self.rect = self.image.get_rect()
         
    def update(self):
        # Desplaza al proyectil
        self.rect.y += 25
                         

# ------------------------------
# Ventana
# ------------------------------

pygame.init()
 
# Dimensiones de la pantalla
largo_pantalla = 900
alto_pantalla = 600
pantalla = pygame.display.set_mode([largo_pantalla, alto_pantalla])
pygame.display.set_caption("PROYECTILAND                               By   MATEO ROVERE")
  
# Lista de cada sprite, así como de todos los enemigos y del protagonista.
lista_de_todos_los_sprites = pygame.sprite.Group()
 
# Lista de cada enemigo en el juego
lista_enemigos = pygame.sprite.Group()
 
# Lista de cada proyectil
lista_proyectiles = pygame.sprite.Group()
lista_proyectiles_enemigos = pygame.sprite.Group()


# ------------------------------
# Creo los sprites
# ------------------------------
 
for i in range(3):
# 3 Filas
    for j in range (10):
#10 Columnas    
        # Esto representa un enemigo
        enemigo = Enemigo()
     
        # Configuro una ubicación aleatoria para el enemigo
        enemigo.rect.x = 100 + j*70  #Desde el pixel 100, de 70 en 70, hacia abajo
        enemigo.rect.y = 270 - i*120 #Desde el pixel 270, de 120 en 120, hacia arriba
         
        # Añado al enemigo a la lista de objetos
        lista_enemigos.add(enemigo)
        lista_de_todos_los_sprites.add(enemigo)
 
# Creo al protagonista
protagonista = Protagonista()
lista_de_todos_los_sprites.add(protagonista)
 
# Itinerancia hasta que el usuario presione el botón de salir. (Booleano,variable que es True o False)
hecho = False
 
# Tasa de refresco de la pantalla
reloj = pygame.time.Clock()
puntuacion = 0
protagonista.rect.y = 500




# ------------------------------
# Bucle Principal
# ------------------------------

fondo = cargar_imagen("fondo.jpg", IMG_DIR, alpha=False)

contador = 0
enemigos_vivos = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

lista_protagonistas = pygame.sprite.Group()
lista_protagonistas.add(protagonista)
vidas = 3

while not hecho:
    # Procesamiento de Eventos
    for evento in pygame.event.get(): 
        if evento.type == pygame.QUIT: 
            hecho = True
             
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            # Dispara un proyectil si el usuario presiona el botón del mouse
            proyectil = Proyectil()
            # Configuro el proyectil de forma que esté en la punta del protagonista
            proyectil.rect.x = protagonista.rect.x+25
            proyectil.rect.y = protagonista.rect.y
            # Añado el proyectil a la lista
            lista_de_todos_los_sprites.add(proyectil)
            lista_proyectiles.add(proyectil)
            contador += 1
            if contador == 1:          
                proyectil_enemigo = Proyectilenemigo()
                posX = randint(1,10)
                posY = randint (1,3)
                proyectil_enemigo.rect.x = 100 + posX * 70
                proyectil_enemigo.rect.y = 270 - posY * 120
                lista_proyectiles_enemigos.add(proyectil_enemigo)
                lista_de_todos_los_sprites.add(proyectil_enemigo)
                contador = 0
 
# ------------------------------
# Lógica del Juego
# ------------------------------

     
    # Llamo al método update() en todos los sprites
    lista_de_todos_los_sprites.update()
     
    # Calculo la mecánica para cada proyectil
    for proyectil in lista_proyectiles:
 
        # Veo si alcanza a un enemigo
        lista_enemigos_alcanzados = pygame.sprite.spritecollide(proyectil, lista_enemigos, True)
         
        # Por cada enemigo eliminado, elimino el proyectil y aumentamos la puntuación
        for enemigo in lista_enemigos_alcanzados:
            lista_proyectiles.remove(proyectil)
            lista_de_todos_los_sprites.remove(proyectil)
            puntuacion += 1
            print( puntuacion )
             
        # Eliminamos el proyectil si vuela fuera de la pantalla
        if proyectil.rect.y < -10:
            lista_proyectiles.remove(proyectil)
            lista_de_todos_los_sprites.remove(proyectil)

    # Veo si un proyectil enemigo alcanza al protagonista 
    for bala in lista_proyectiles_enemigos:
        lista_protagonista_alcanzado = pygame.sprite.spritecollide(bala, lista_protagonistas, False)
        if len(lista_protagonista_alcanzado) > 0:
            vidas-=1
            lista_proyectiles_enemigos.remove(bala)
            lista_de_todos_los_sprites.remove(bala)
            print ("Tus vidas son: " + (str(vidas)))
            
        elif vidas == 0:
                pygame.quit()

                pygame.init()
                largo_pantalla = 900
                alto_pantalla = 600
                pantalla = pygame.display.set_mode([largo_pantalla, alto_pantalla])                                            
                pygame.display.set_caption("Proyectiland GAME OVER")                 
                reloj = pygame.time.Clock()
                puntaje = puntuacion
                
                fuente = pygame.font.Font(None, 100)                
                texto1 = fuente.render("GAME OVER " , 50, (0, 0, 255))            
                fondo = cargar_imagen("fondo.jpg", IMG_DIR, alpha=True)
                                  
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                    reloj.tick(5)
                    pantalla.blit(texto1, (240,250))
                    pygame.display.update()


                fuente = pygame.font.Font(None, 100)                
                texto1 = fuente.render("Tu puntaje fue: " + (str(puntaje)), 10, (0, 0, 255))

                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            exit()
                    reloj.tick(5)
                    pantalla.blit(texto1, (240,400))
                    pygame.display.update()
             
                             
        if bala.rect.y > 600:
            #saca la bala de la pantalla
            lista_proyectiles_enemigos.remove(bala)
            lista_de_todos_los_sprites.remove(bala)
            


# ------------------------------
# Dibujamos un marco
# ------------------------------
         
    # Fondo de la pantalla
    pantalla.blit(fondo, (0, 0))
                                             
    # Dibujamos todos los sprites
    lista_de_todos_los_sprites.draw(pantalla)
                                     
    # Actualizo la pantalla con todo lo que hemos dibujado.
    pygame.display.flip()
                                         
    # Limitamos a 20 fps
    reloj.tick(20)  


 
pygame.quit()
