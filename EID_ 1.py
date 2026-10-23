import math
import random
import pygame

ANCHO, ALTO = 900, 600
FPS = 60

LIMITE_IZQUIERDO = 500
CARRIL_CENTRO = 700

class Naves:
    def __init__(self):
        pass

    def mover(self, teclas):
        pass

    def dibujar(self, pantalla):
        pass

class balas:
    def __init__(self):
        pass

    def actualizar(self):
        pass

    def dibujar(self, pantalla):
        pass

class Enemigos:
    def __init__(self, x_base, y, es_jefe=False):
        self.x_base = x_base       
        self.x = x_base            
        self.y = y                 
        self.es_jefe = es_jefe
        
        self.angulo = random.uniform(0, math.pi * 2)
        
        self.direccion_y = 1  
        self.velocidad_y = 2.0
        
        self.direccion_angulo = 1.0 if random.random() > 0.5 else -1.0
        
        if self.es_jefe:
            self.ancho, self.alto = 80, 80
            self.color = (255, 0, 0)
            self.vida_maxima = 10
            self.vida = 10
            self.amplitud_sin = 100     
            self.velocidad_angulo = 0.05 
        else:
            self.ancho, self.alto = 40, 40
            self.color = (0, 255, 0)
            self.vida_maxima = 5
            self.vida = 5
            self.amplitud_sin = 70      
            self.velocidad_angulo = 0.06 
            
    def actualizar(self):
        self.y += self.velocidad_y * self.direccion_y
        
        self.angulo += self.velocidad_angulo * self.direccion_angulo
        self.x = self.x_base + math.sin(self.angulo) * self.amplitud_sin
        
        if self.x < LIMITE_IZQUIERDO:
            self.x = LIMITE_IZQUIERDO
            self.direccion_angulo *= -1  
        elif self.x + self.ancho > ANCHO:
            self.x = ANCHO - self.ancho
            self.direccion_angulo *= -1

        if self.y + self.alto > ALTO:
            self.y = ALTO - self.alto
            self.direccion_y = -1  
        elif self.y < 0 and self.direccion_y == -1:
            self.y = 0
            self.direccion_y = 1   

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), self.ancho, self.alto))
        
        if self.es_jefe:
            largo_barra = self.ancho
            vida_proporcional = (self.vida / self.vida_maxima) * largo_barra
            pygame.draw.rect(pantalla, (100, 0, 0), (int(self.x), int(self.y) - 12, largo_barra, 6))
            pygame.draw.rect(pantalla, (255, 0, 0), (int(self.x), int(self.y) - 12, int(vida_proporcional), 6))
        else:
            largo_barra = self.ancho
            vida_proporcional = (self.vida / self.vida_maxima) * largo_barra
            pygame.draw.rect(pantalla, (80, 20, 20), (int(self.x), int(self.y) - 8, largo_barra, 4))
            pygame.draw.rect(pantalla, (0, 255, 100), (int(self.x), int(self.y) - 8, int(vida_proporcional), 4))


def gestionar_colisiones_enemigos(lista_enemigos):
    for i in range(len(lista_enemigos)):
        for j in range(i + 1, len(lista_enemigos)):
            e1 = lista_enemigos[i]
            e2 = lista_enemigos[j]
            
            rect1 = pygame.Rect(e1.x, e1.y, e1.ancho, e1.alto)
            rect2 = pygame.Rect(e2.x, e2.y, e2.ancho, e2.alto)
            
            if rect1.colliderect(rect2):
                traslape_x = min(e1.x + e1.ancho, e2.x + e2.ancho) - max(e1.x, e2.x)
                traslape_y = min(e1.y + e1.alto, e2.y + e2.alto) - max(e1.y, e2.y)
                
                if traslape_x < traslape_y:
                    e1.direccion_angulo *= -1
                    e2.direccion_angulo *= -1
                    
                    if e1.x < e2.x:
                        e1.x -= traslape_x / 2
                        e2.x += traslape_x / 2
                    else:
                        e1.x += traslape_x / 2
                        e2.x -= traslape_x / 2
                else:
                    e1.direccion_y *= -1
                    e2.direccion_y *= -1
                    
                    if e1.y < e2.y:
                        e1.y -= traslape_y / 2
                        e2.y += traslape_y / 2
                    else:
                        e1.y += traslape_y / 2
                        e2.y -= traslape_y / 2

def crear_oleada(numero):
    lista_enemigos = []
    
    if numero == 1:
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -50))
    elif numero == 2:
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -50))
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -180)) 
    elif numero == 3:
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -50))
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -180))
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -310)) 
    elif numero >= 4:
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -100, es_jefe=True))
        lista_enemigos.append(Enemigos(CARRIL_CENTRO, -280))
        
    return lista_enemigos

def dibujar_interfaz(pantalla, oleada):
    fuente = pygame.font.SysFont("monospace", 24)
    texto_oleada = f"OLEADA: {oleada}"
    if oleada >= 4:
        texto_oleada += " - ¡JEFE EN CAMINO!"
    render_texto = fuente.render(texto_oleada, True, (255, 255, 255))
    pantalla.blit(render_texto, (20, 20))

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("SI LAS COLISIONES SE BUGUEAN DENUEVO ME MATO")
    reloj = pygame.time.Clock()
    
    numero_oleada = 1
    lista_enemigos = crear_oleada(numero_oleada)
    
    corriendo = True
    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
                
                #ESTO SE ELEMINA ERA PA PROBAR LAS OLEADAS
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and len(lista_enemigos) > 0:
                    lista_enemigos[0].vida -= 1 
                    if lista_enemigos[0].vida <= 0:
                        lista_enemigos.pop(0)
                        
        for enemigo in lista_enemigos:
            enemigo.actualizar()
            
        gestionar_colisiones_enemigos(lista_enemigos)
            
        if len(lista_enemigos) == 0:
            numero_oleada += 1
            lista_enemigos = crear_oleada(numero_oleada)
            
        pantalla.fill((10, 10, 20))
        
        for enemigo in lista_enemigos:
            enemigo.dibujar(pantalla)
            
        dibujar_interfaz(pantalla, numero_oleada)
        
        pygame.display.flip()
        reloj.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()
