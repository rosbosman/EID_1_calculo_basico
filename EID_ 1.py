import math
import random
import pygame

ANCHO, ALTO = 900, 600
FPS = 60
HUD_ALTO = 50
VIDA_MAXIMA = 30
DANO_ENEMIGO = {"normal": 6, "triangulo": 10, "circulo": 15, "jefe": 30}
DANO_ARMA = {"basica": 2, "parabola": 5, "conica": 6}
INVULNERABLE_MS = 1000
MAX_ENEMIGOS_JEFE = 6  

class Naves:
    def __init__(self):
        self.x = ANCHO / 2
        self.y = ALTO - 70
        self.radio = 18
        self.velocidad = 5
        self.vida = VIDA_MAXIMA
        self.ultimo_golpe = -INVULNERABLE_MS
  
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad

        self.x = max(self.radio, min(ANCHO - self.radio, self.x))
        self.y = max(HUD_ALTO + self.radio, min(ALTO - self.radio, self.y))
 
    def recibir_dano(self, tipo_enemigo, ahora):
        if ahora - self.ultimo_golpe < INVULNERABLE_MS: 
            return
        self.vida = max(0, self.vida - DANO_ENEMIGO[tipo_enemigo])
        self.ultimo_golpe = ahora
 
    def dibujar(self, pantalla):
        ahora = pygame.time.get_ticks()
        if ahora - self.ultimo_golpe < INVULNERABLE_MS and (ahora // 100) % 2 == 0:
            return
        r = self.radio
        puntos = [
            (self.x, self.y - r),
            (self.x - r, self.y + r),
            (self.x, self.y + r // 2),
            (self.x + r, self.y + r),
        ]
        pygame.draw.polygon(pantalla, (80, 200, 255), puntos)

    def obtener_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

class Bala:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.x_origen = x
        self.y_origen = y
        self.tipo = tipo
        self.radio = 5
        self.activa = True
        self.tiempo = 0

    def actualizar(self):
        self.tiempo += 1
        if self.tipo == "basica":
            self.y -= 10
        elif self.tipo == "parabola":
            self.x = self.x_origen + self.tiempo * 4
            self.y = self.y_origen - (12 * self.tiempo - 0.25 * (self.tiempo ** 2))
        elif self.tipo == "conica":
            r = 60
            velocidad_angular = 0.15
            self.x = self.x_origen - r + r * math.cos(velocidad_angular * self.tiempo)
            self.y = self.y_origen + r * math.sin(velocidad_angular * self.tiempo)
            
            if self.tiempo * velocidad_angular >= 2 * math.pi:
                self.activa = False

        if self.y < -50 or self.y > ALTO + 50 or self.x < -50 or self.x > ANCHO + 50:
            self.activa = False

    def dibujar(self, pantalla):
        color = (255, 255, 0) if self.tipo == "basica" else (255, 128, 0) if self.tipo == "parabola" else (0, 255, 255)
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), self.radio)
        
    def obtener_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

class GestorArmas:
    def __init__(self):
        self.armas = ["basica", "parabola", "conica"]
        self.arma_actual = 0 
        self.municion = {"basica": float('inf'), "parabola": 20, "conica": 15}
        self.balas = []

    def cambiar_arma(self):
        self.arma_actual = (self.arma_actual + 1) % 3

    def disparar(self, nave_x, nave_y):
        tipo = self.armas[self.arma_actual]
        if self.municion[tipo] > 0:
            self.balas.append(Bala(nave_x, nave_y, tipo))
            if tipo != "basica":
                self.municion[tipo] -= 1

    def actualizar_balas(self, pantalla, enemigos):
        for bala in self.balas[:]:
            bala.actualizar()
            bala.dibujar(pantalla)
            rect_bala = bala.obtener_rect()
            for enemigo in enemigos[:]:
                if rect_bala.colliderect(enemigo.obtener_rect()):
                    enemigo.vida -= DANO_ARMA[bala.tipo]
                    bala.activa = False
                    if enemigo.vida <= 0:
                        if enemigo in enemigos:
                            enemigos.remove(enemigo)
                    break
            if not bala.activa and bala in self.balas:
                self.balas.remove(bala)

    def dibujar_interfaz(self, pantalla):
        fuente = pygame.font.SysFont("monospace", 16, bold=True)
        tipo_arma = self.armas[self.arma_actual]
        texto_municion = "Inf" if tipo_arma == "basica" else str(self.municion[tipo_arma])
        render_texto = fuente.render(f"[Z] ARMA: {tipo_arma.upper()} | BALAS: {texto_municion} | [ESPACIO] DISPARAR", True, (255, 255, 0))
        pantalla.blit(render_texto, (20, 20))

class Enemigos:
    def __init__(self, x_base, y, tipo="normal"):
        self.x_base = x_base       
        self.x = x_base            
        self.y = y                 
        self.tipo = tipo
        self.ultima_invocacion = pygame.time.get_ticks()
        self.direccion_y = 1
        
        if self.tipo == "jefe":
            self.A, self.B, self.C, self.D = 100, 0.05, math.pi, x_base
            self.ancho, self.alto, self.color, self.vida = 80, 80, (255, 0, 0), 30
        elif self.tipo == "triangulo":
            self.A, self.B, self.C, self.D = 85, 0.07, math.pi/4, x_base
            self.ancho, self.alto, self.color, self.vida = 50, 50, (255, 255, 0), 10
        elif self.tipo == "circulo":
            self.A, self.B, self.C, self.D = 75, 0.065, math.pi/2, x_base
            self.ancho, self.alto, self.color, self.vida = 50, 50, (255, 128, 0), 8
        else:
            self.A, self.B, self.C, self.D = 70, 0.06, 0, x_base
            self.ancho, self.alto, self.color, self.vida = 50, 50, (0, 255, 0), 5
        self.vida_maxima = self.vida

    def actualizar(self, lista_enemigos=None):
        
        self.y += self.direccion_y
        if self.y >= ALTO - self.alto:
            self.y = ALTO - self.alto
            self.direccion_y = -1
        elif self.y <= HUD_ALTO:
            self.y = HUD_ALTO
            self.direccion_y = 1

       
        self.x = self.A * math.sin(self.B * self.y + self.C) + self.D
       

        if self.tipo == "jefe" and lista_enemigos is not None:
            ahora = pygame.time.get_ticks()
            if ahora - self.ultima_invocacion >= 5000:
                self.ultima_invocacion = ahora

                if len(lista_enemigos) < MAX_ENEMIGOS_JEFE:
                    tipo_invocado = random.choice(["normal", "triangulo", "circulo"])
                    alto_invocado = 50
                    ancho_invocado = 50

                    
                    y_aparicion = min(self.y + self.alto, ALTO - alto_invocado)
                    y_aparicion = max(HUD_ALTO, y_aparicion)

                   
                    x_base = max(85, min(ANCHO - 85 - ancho_invocado, self.x))
                    lista_enemigos.append(
                        Enemigos(x_base, y_aparicion, tipo_invocado)
                    )

    def dibujar(self, pantalla):
        if self.tipo == "jefe":
            pygame.draw.ellipse(pantalla, self.color, (int(self.x), int(self.y), self.ancho, self.alto - 20))
        elif self.tipo == "triangulo":
            pygame.draw.polygon(pantalla, self.color, [(self.x, self.y), (self.x + self.ancho, self.y), (self.x + self.ancho/2, self.y + self.alto)])
        elif self.tipo == "circulo":
            pygame.draw.circle(pantalla, self.color, (int(self.x + self.ancho/2), int(self.y + self.alto/2)), int(self.ancho/2))
        else:
            pygame.draw.rect(pantalla, self.color, (int(self.x), int(self.y), self.ancho, self.alto))
            
        pygame.draw.rect(pantalla, (255, 0, 0), (int(self.x), int(self.y) - 10, int((self.vida / self.vida_maxima) * self.ancho), 5))

    def obtener_rect(self):
       
        alto_colision = self.alto - 20 if self.tipo == "jefe" else self.alto
        return pygame.Rect(self.x, self.y, self.ancho, alto_colision)

def crear_oleada(numero):
    lista = []
    if numero == 1:
        lista.append(Enemigos(450, 50, "normal"))
    elif numero == 2:
        lista.extend([Enemigos(300, 50, "normal"), Enemigos(600, 100, "triangulo")])
    elif numero == 3:
        lista.extend([Enemigos(200, 50, "normal"), Enemigos(450, 100, "triangulo"), Enemigos(700, 50, "circulo")])
    elif numero >= 4:
        lista.extend([Enemigos(450, 80, "jefe"), Enemigos(200, 80, "normal")])
    return lista

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    reloj = pygame.time.Clock()
    
    estado = "inicio"
    
    nave = Naves()
    armas = GestorArmas()
    numero_oleada = 1
    enemigos = crear_oleada(numero_oleada)
    
    fuente_titulo = pygame.font.SysFont("monospace", 48, bold=True)
    fuente_texto = pygame.font.SysFont("monospace", 24)
    
    corriendo = True
    while corriendo:
        ahora = pygame.time.get_ticks()
        pantalla.fill((10, 10, 20))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False
            if evento.type == pygame.KEYDOWN:
                if estado == "inicio":
                    if evento.key == pygame.K_RETURN:
                        estado = "jugando"
                elif estado == "jugando":
                    if evento.key == pygame.K_z:
                        armas.cambiar_arma()
                    if evento.key == pygame.K_SPACE:
                        armas.disparar(nave.x, nave.y)
                elif estado == "fin":
                    if evento.key == pygame.K_r:
                        nave = Naves()
                        armas = GestorArmas()
                        numero_oleada = 1
                        enemigos = crear_oleada(numero_oleada)
                        estado = "jugando"

        if estado == "inicio":
            titulo = fuente_titulo.render("ARCADE", True, (0, 255, 255))
            instruccion = fuente_texto.render("Presiona ENTER para iniciar", True, (255, 255, 255))
            pantalla.blit(titulo, (ANCHO/2 - titulo.get_width()/2, ALTO/2 - 50))
            pantalla.blit(instruccion, (ANCHO/2 - instruccion.get_width()/2, ALTO/2 + 50))

        elif estado == "jugando":
            teclas = pygame.key.get_pressed()
            nave.mover(teclas)
                
            if not enemigos:
                numero_oleada += 1
                if numero_oleada > 4:
                    estado = "fin" 
                else:
                    enemigos = crear_oleada(numero_oleada)
                
            for enemigo in enemigos[:]:
                enemigo.actualizar(enemigos)
                enemigo.dibujar(pantalla)
                if nave.obtener_rect().colliderect(enemigo.obtener_rect()):
                    nave.recibir_dano(enemigo.tipo, ahora)
                    
            armas.actualizar_balas(pantalla, enemigos)
            nave.dibujar(pantalla)
            armas.dibujar_interfaz(pantalla)
            
            fuente_vida = pygame.font.SysFont("monospace", 16, bold=True)
            texto_vida = fuente_vida.render(f"VIDA: {nave.vida} | OLEADA: {numero_oleada}", True, (255, 255, 255))
            pantalla.blit(texto_vida, (650, 20))
            
            if nave.vida <= 0:
                estado = "fin"

        elif estado == "fin":
            mensaje_fin = "¡VICTORIA!" if nave.vida > 0 else "JUEGO TERMINADO"
            color_fin = (0, 255, 0) if nave.vida > 0 else (255, 0, 0)
            
            titulo_fin = fuente_titulo.render(mensaje_fin, True, color_fin)
            reinicio = fuente_texto.render("Apreta R para volver a iniciar", True, (255, 255, 255))
            pantalla.blit(titulo_fin, (ANCHO/2 - titulo_fin.get_width()/2, ALTO/2 - 50))
            pantalla.blit(reinicio, (ANCHO/2 - reinicio.get_width()/2, ALTO/2 + 50))
            
        pygame.display.flip()
        reloj.tick(FPS)
        
    pygame.quit()

if __name__ == "__main__":
    main()