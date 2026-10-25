import math
import pygame

class Bala:
    def __init__(self, x, y, tipo, angulo=0):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.radio = 5
        self.activa = True

        if self.tipo == "basica":
            self.vel_x = 0
            self.vel_y = -10
        elif self.tipo == "parabola":
            self.vel_x = 4      
            self.vel_y = -12    
            self.gravedad = 0.5 
        elif self.tipo == "conica":
            velocidad = 10
            radianes = math.radians(angulo) 
            self.vel_x = math.sin(radianes) * velocidad
            self.vel_y = -math.cos(radianes) * velocidad

    def actualizar(self):
        if self.tipo == "parabola":
            self.vel_y += self.gravedad

        self.x += self.vel_x
        self.y += self.vel_y

        if self.y < -50 or self.y > 650 or self.x < -50 or self.x > 950:
            self.activa = False

    def dibujar(self, pantalla):
        if self.tipo == "basica":
            color = (255, 255, 0)
        elif self.tipo == "parabola":
            color = (255, 128, 0) 
        else:
            color = (0, 255, 255) 
        
        pygame.draw.circle(pantalla, color, (int(self.x), int(self.y)), self.radio)


class GestorArmas:
    def __init__(self):
        self.armas = ["basica", "parabola", "conica"]
        self.arma_actual = 0 
        self.municion = {
            "basica": float('inf'), 
            "parabola": 20,
            "conica": 15
        }

    def cambiar_arma(self):
        self.arma_actual = (self.arma_actual + 1) % 3

    def disparar(self, nave_x, nave_y):
        tipo = self.armas[self.arma_actual]
        balas_nuevas = []

        if self.municion[tipo] > 0:
            if tipo == "basica":
                balas_nuevas.append(Bala(nave_x, nave_y, "basica"))
            elif tipo == "parabola":
                balas_nuevas.append(Bala(nave_x, nave_y, "parabola"))
                self.municion["parabola"] -= 1
            elif tipo == "conica":
                balas_nuevas.append(Bala(nave_x, nave_y, "conica", -20))
                balas_nuevas.append(Bala(nave_x, nave_y, "conica", 0))
                balas_nuevas.append(Bala(nave_x, nave_y, "conica", 20))
                self.municion["conica"] -= 1

        return balas_nuevas

    def dibujar_interfaz(self, pantalla):
        fuente = pygame.font.SysFont("monospace", 18, bold=True)
        tipo_arma = self.armas[self.arma_actual]
        
        texto_municion = "Inf" if tipo_arma == "basica" else str(self.municion[tipo_arma])
        texto_arma = f"ARMA: {tipo_arma.upper()} | BALAS: {texto_municion}"
        
        render_texto = fuente.render(texto_arma, True, (255, 255, 0))
        pantalla.blit(render_texto, (500, 20))