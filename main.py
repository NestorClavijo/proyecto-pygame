import math
from pygame import Rect, draw, mouse, MOUSEBUTTONDOWN
import pygame
import random

#Primero se dede inicializar pygame
pygame.init()

#Crear primera ventana con pygame
screen = pygame.display.set_mode((1200,800))
background = pygame.image.load('espacio.jpg')
background = pygame.transform.scale(background, (1200,800))

#Modificamos el titulo e icono de la ventana
pygame.display.set_caption("Simulacion de Galaga")
try:
    icono = pygame.image.load('astronave.png')
    pygame.display.set_icon(icono)
except pygame.error as e:
    print(f"Error al cargar la imagen: {e}")

#=========================================================================#
#Definicion de la imagen del jugador y su posicion inicial en el juego
imagenJugador = pygame.image.load("nave-espacial.png")
jugadorX = 570
jugadorY = 650
movimientoJugador = 0

def jugador(x,y):
    screen.blit(imagenJugador, (x,y))

#Definicion del enemigo del mismo modo que se creo el jugador
imagenEnemigo = []
enemigoX = []
enemigoY = []
desplazarEnemigoX = []
desplazarEnemigoY = []
numero_enemigos = 2

def crearEnemigos(num):
    for i in range(num):
        imagenEnemigo.append(pygame.image.load("alienigena-aterrador.png"))
        enemigoX.append(random.randint(60,1050))
        enemigoY.append(random.randint(70,300))
        desplazarEnemigoX.append(random.randint(2,6)/10)
        desplazarEnemigoY.append(random.randint(4,8)/10)

def eliminarEnemigos():
    imagenEnemigo.clear()
    enemigoX.clear()
    enemigoY.clear()
    desplazarEnemigoX.clear()
    desplazarEnemigoY.clear()

crearEnemigos(2)

def enemigo(x,y,i):
    screen.blit(imagenEnemigo[i], (x,y))

#Definicion de la bala que usara la nave
imagenBala = pygame.image.load("bala.png")
balaX = 570
balaY = 650
desplazarBala = 3
estadoBala = "preparado"

def disparar_bala(x,y):
    global estadoBala
    estadoBala = "ataque"
    screen.blit(imagenBala, (x + 10,y + 10))

def colisiona(enemigoX,enemigoY,balaX,balaY,x):
    enemigoX = enemigoX
    enemigoY = enemigoY
    distancia = math.sqrt((math.pow(enemigoX-balaX,2))+(math.pow(enemigoY-balaY,2)))
    if distancia < x:
        return True
    else:
        return False

#Parametros para mostrar el puntaje y el nivel
valor_nivel = 1
valor_puntaje = 0

font = pygame.font.Font('freesansbold.ttf',32)
puntajeX = 10
puntajeY = 10

def mostrarPuntaje(x,y):
    puntaje = font.render("Puntaje: "+ str(valor_puntaje), True, (255,255,255))
    screen.blit(puntaje,(x,y))
def mostrarNivel(x,y):
    nivel = font.render("Nivel: " + str(valor_nivel), True, (255, 255, 255))
    screen.blit(nivel, (1050-x,y))

#Parametros para terminar el nivel
perdida_font = pygame.font.Font('freesansbold.ttf',256)

def juegoTerminado():
    texto_final = font.render("WASTED",True,(255,0,0))
    screen.blit(texto_final,(550,350))
#=========================================================================#

#Definiendo botones del final del jeugo
reintentar = Rect(250,150,200,50)
salir = Rect(700,150,200,50)

#=========================================================================#

corriendo = True
estoyVivo = True
#Este while define en que momento seleccinamos el boton de cerrar ventana (Game Loop)
while corriendo:
    screen.fill((255, 255, 255))
    screen.blit(background,(0,0))
    if estoyVivo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            #Condicional para definir si las flechas del teclado estan presionadas
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    movimientoJugador = -0.6
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    movimientoJugador = 0.6
                if event.key == pygame.K_SPACE:
                    if estadoBala == "preparado":
                        balaX = jugadorX
                        disparar_bala(balaX,jugadorY)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    movimientoJugador = 0

        #condicionales para que el jugador no se pueda salir de la pantalla
        if jugadorX <= 10:
            jugadorX = 10
        elif jugadorX >= 1125:
            jugadorX = 1125

        jugadorX = jugadorX + movimientoJugador
        jugador(jugadorX,jugadorY)

        #Movimiento de el enemigo
        for i in range(numero_enemigos):

            colisionJugador = colisiona(enemigoX[i]+64, enemigoY[i]+64, jugadorX+64, jugadorY+64, 80)
            if colisionJugador:
                juegoTerminado()
                estoyVivo = False
                eliminarEnemigos()
                break

            enemigoX[i] = enemigoX[i] + desplazarEnemigoX[i]
            enemigoY[i] = enemigoY[i] + desplazarEnemigoY[i]
            if enemigoX[i] < 5 or enemigoX[i] >= 1125:
                desplazarEnemigoX[i] = desplazarEnemigoX[i]*(-1)
            if enemigoY[i] < 2 or enemigoY[i] >= 700:
                desplazarEnemigoY[i] = desplazarEnemigoY[i]*(-1)

            # Definimos si la bala choco con el enemigo
            colision = colisiona(enemigoX[i]+64, enemigoY[i]+64, balaX, balaY,50)
            if colision and estadoBala == "ataque":
                balaY = 650
                estadoBala = "preparado"
                valor_puntaje += 1
                if valor_puntaje % 5 == 0 and valor_puntaje != 0:
                    valor_nivel += 1
                    crearEnemigos(1)
                    numero_enemigos += 1
                enemigoX[i] = random.randint(60,1050)
                enemigoY[i] = random.randint(70,300)

            enemigo(enemigoX[i], enemigoY[i], i)

        #Movimiento de la bala
        if balaY <= 0:
            estadoBala = "preparado"
            balaY = 650

        if estadoBala == "ataque":
            disparar_bala(balaX,balaY)
            balaY -= desplazarBala

        mostrarPuntaje(puntajeX,puntajeY)
        mostrarNivel(puntajeX,puntajeY)
        pygame.display.update()

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False


            if event.type == MOUSEBUTTONDOWN and event.button==1:
                if reintentar.collidepoint(mouse.get_pos()):
                    estoyVivo = True
                    crearEnemigos(2)
                    break
                if salir.collidepoint(mouse.get_pos()):
                    corriendo = False

            if reintentar.collidepoint(mouse.get_pos()):
                draw.rect(screen, (0,255,0),reintentar,0)
            else:
                draw.rect(screen, (0, 220, 0), reintentar, 0)

            if salir.collidepoint(mouse.get_pos()):
                draw.rect(screen, (255,0,0),salir,0)
            else:
                draw.rect(screen, (220,0, 0), salir, 0)

            texto_aceptar = font.render("Reintentar",True,(255,255,255))
            screen.blit(texto_aceptar,(260,160))

            texto_aceptar = font.render("Salir", True, (255, 255, 255))
            screen.blit(texto_aceptar, (710, 160))

            juegoTerminado()

            jugadorX = 570
            jugadorY = 650
            valor_puntaje = 0

            crearEnemigos(2)
            numero_enemigos = 2

            pygame.display.update()
#=========================================================================#