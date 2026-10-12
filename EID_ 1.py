import math
import random
import pygame


ANCHO, ALTO = 900, 600
FPS = 60


class Nava :
    def __init__(self):
        pass

    def mover(self, teclas):
        pass

    def dibujar(self, pantalla):
        pass



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
        pygame.init()
        pantalla = pygame.display.set_mode((ANCHO, ALTO))
        reloj = pygame.time.Clock()
 
        corriendo = True
        while corriendo:
         for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
 
        pantalla.fill((10, 10, 20))
       
        pygame.display.flip()
        reloj.tick(FPS)
 
    pygame.quit()
 
 
    if __name__ == "__main__":
             main()

 