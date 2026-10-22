import math as MA
import random as RA
import pygame as PYG
 
ANCHO, ALTO = 900, 600
FPS = 60
HUD_ALTO = 50
VIDA_MAXIMA = 30
DANO_ENEMIGO = {1: 6, 2: 10, 3: 15, 4: 30}
INVULNERABLE_MS = 1000
TOTAL_DE_OLEADAS = 4
 
 
class Naves:
    def __init__(self):
        self.x = ANCHO / 2
        self.y = ALTO - 70
        self.radio = 18 # radio de la circunferencia con la que se calcula las coliciones
        self.velocidad = 5
        self.vida = VIDA_MAXIMA
        self.ultimo_golpe = -INVULNERABLE_MS # parte en  -INVULNERABLE_MS para que el  el prigolpe si cuente 
  
    def mover(self, teclas):
        if teclas[PYG.K_LEFT]:
            self.x -= self.velocidad
        if teclas[PYG.K_RIGHT]:
            self.x += self.velocidad


            # en pygame el eje crece hacia abajo , por eso arriba resta y abajp suma
        if teclas[PYG.K_UP]:
            self.y -= self.velocidad
        if teclas[PYG.K_DOWN]:
            self.y += self.velocidad

            # es el limite del mapa min evita pasarse del borde derecho inferior y max evita pasarse del izquuierdo superior
            #se usa el dadio para que la nave completa quede dentra
            #el borde  superior esta la barra de la interfaz
        self.x = max(self.radio, min(ANCHO - self.radio, self.x))
        self.y = max(HUD_ALTO + self.radio, min(ALTO - self.radio, self.y))
 
    def recibir_dano(self, tipo_enemigo, ahora):
        if ahora - self.ultimo_golpe < INVULNERABLE_MS: 
            return # si el golpe fua  hace menos tiempo que invinerable el golpe se ignora sin esto si  la nave reciviria adaño a  cada rato 
        self.vida = max(0, self.vida - DANO_ENEMIGO[tipo_enemigo])# el daño depende del tipo de enemigo , max(0)evita que la vida quede en negativo
        self.ultimo_golpe = ahora # se registra  el momento del golpe para activa la invunerabilidad 
 
    def dibujar(self, pantalla):
        ahora = PYG.time.get_ticks()
        if ahora - self.ultimo_golpe < INVULNERABLE_MS and (ahora // 100) % 2 == 0:
            return
         # la nave es un poligno de 4 puntos calculado a partir del centro  y el radio  apunta hacia arriba, ala izquierda muesca central y ala derecha
        r = self.radio
        puntos = [
            (self.x, self.y - r),
            (self.x - r, self.y + r),
            (self.x, self.y + r // 2),
            (self.x + r, self.y + r),
        ]
        PYG.draw.polygon(pantalla, (80, 200, 255), puntos)

        def hay_colision(a, b):
            distancia = MA.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)
            return distancia <= a.radio + b.radio







        

class balas :
    def __init__(self):
        pass

    def actualizar(self):
        pass

    def dibujar (self, pantalla):
        pass

class Enemigos:
    def __init__(self, x , y , es_jefe= False):
            pass



    def actualizar(self):
    
        pass
 
    def dibujar(self, pantalla):
       
        pass


    def crear_oleada(numero):
   
        pass

    def dibujar_interfaz(pantalla):
    
     pass


    def main():
     PYG.init()
    pantalla = PYG.display.set_mode((ANCHO, ALTO))
    reloj = PYG.time.Clock()
    nave = Naves()
    corriendo = True
    while corriendo:
        for evento in PYG.event.get():
            if evento.type == PYG.QUIT:
                corriendo = False
        teclas = PYG.key.get_pressed()
        nave.mover(teclas)
        pantalla.fill((10, 10, 20))
        nave.dibujar(pantalla)
        PYG.display.flip()
        reloj.tick(FPS)
    PYG.quit()
