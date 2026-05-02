import math
 
import pygame
from config import BLUE, CYAN, GREEN, WHITE, YELLOW
 
 
class PowerUp:
    # Tipos de power-ups
    WEAPON_LEFT = "WEAPON_LEFT"
    WEAPON_RIGHT = "WEAPON_RIGHT"
    WEAPON_DIAG_RIGHT = "WEAPON_DIAG_RIGHT"
    WEAPON_DIAG_LEFT = "WEAPON_DIAG_LEFT"
    WEAPON_DIAG_DOWN_RIGHT = "WEAPON_DIAG_DOWN_RIGHT"
    WEAPON_DIAG_DOWN_LEFT = "WEAPON_DIAG_DOWN_LEFT"
    WEAPON_UP = "WEAPON_UP"
    WEAPON_DOWN = "WEAPON_DOWN"
    LIFE = "LIFE"
    SHIELD = "SHIELD"
 
    # Colores por tipo
    COLORS = {
        WEAPON_LEFT: BLUE,
        WEAPON_RIGHT: BLUE,
        WEAPON_DIAG_RIGHT: YELLOW,
        WEAPON_DIAG_LEFT: YELLOW,
        WEAPON_DIAG_DOWN_RIGHT: YELLOW,
        WEAPON_DIAG_DOWN_LEFT: YELLOW,
        WEAPON_UP: CYAN,
        WEAPON_DOWN: GREEN,
        LIFE: (255, 100, 100),  # Rosa
        SHIELD: (255, 140, 0),  # Naranja
    }
 
    # Símbolos por tipo
    SYMBOLS = {
        WEAPON_LEFT: "◀",
        WEAPON_RIGHT: "▶",
        WEAPON_DIAG_RIGHT: "↗",
        WEAPON_DIAG_LEFT: "↖",
        WEAPON_DIAG_DOWN_RIGHT: "↘",
        WEAPON_DIAG_DOWN_LEFT: "↙",
        WEAPON_UP: "↑",
        WEAPON_DOWN: "↓",
        LIFE: "♥",
        SHIELD: "⚔",
    }
 
    def __init__(self, x, y, powerup_type):
        self.x = x
        self.y = y
        self.size = 15
        self.powerup_type = powerup_type
        self.speed_x = 3  # Velocidad hacia la izquierda
        self.speed_y = 0.5  # Amplitud del movimiento sinusoidal
        self.age = 0  # Contador de frames para la onda sinusoidal
 
    def move(self):
        # Movimiento de derecha a izquierda
        self.x -= self.speed_x
        # Movimiento sinusoidal en Y
        self.y += math.sin(self.age * 0.1) * self.speed_y
        self.age += 1
 
    """
    def draw(self, screen):
        color = self.COLORS.get(self.powerup_type, WHITE)
        # Dibujar como estrella
        pygame.draw.polygon(
            screen,
            color,
            [
                (self.x, self.y - self.size),
                (self.x + self.size // 2, self.y - self.size // 3),
                (self.x + self.size, self.y - self.size // 3),
                (self.x + self.size // 2 + 3, self.y + self.size // 3),
                (self.x + self.size // 2 + 6, self.y + self.size),
                (self.x, self.y + self.size // 2),
                (self.x - self.size // 2 - 6, self.y + self.size),
                (self.x - self.size // 2 - 3, self.y + self.size // 3),
                (self.x - self.size, self.y - self.size // 3),
                (self.x - self.size // 2, self.y - self.size // 3),
            ],
        )
        """
 
    def draw(self, screen):
        color = self.COLORS.get(self.powerup_type, WHITE)
 
        if self.powerup_type == self.LIFE:
            # Factor de escala - cambia este número para hacerlo más grande
            escala = 2.0  # 1.5 = más grande, 2.0 = mucho más grande, 2.5 = enorme
 
            # Círculo izquierdo
            pygame.draw.circle(
                screen,
                color,
                (self.x - int(4 * escala), self.y - int(3 * escala)),
                int(4 * escala),
            )
 
            # Círculo derecho
            pygame.draw.circle(
                screen,
                color,
                (self.x + int(4 * escala), self.y - int(3 * escala)),
                int(4 * escala),
            )
 
            # Triángulo inferior
            pygame.draw.polygon(
                screen,
                color,
                [
                    (self.x - int(7.2 * escala), self.y - int(1 * escala)),
                    (self.x, self.y + int(7.2 * escala)),
                    (self.x + int(7.2 * escala), self.y - int(1 * escala)),
                ],
            )
 
            # Rellenar centro
            pygame.draw.circle(
                screen, color, (self.x, self.y - int(1 * escala)), int(3 * escala)
            )
 
        else:
            # Código original de la estrella
            pygame.draw.polygon(
                screen,
                color,
                [
                    (self.x, self.y - self.size),
                    (self.x + self.size // 2, self.y - self.size // 3),
                    (self.x + self.size, self.y - self.size // 3),
                    (self.x + self.size // 2 + 3, self.y + self.size // 3),
                    (self.x + self.size // 2 + 6, self.y + self.size),
                    (self.x, self.y + self.size // 2),
                    (self.x - self.size // 2 - 6, self.y + self.size),
                    (self.x - self.size // 2 - 3, self.y + self.size // 3),
                    (self.x - self.size, self.y - self.size // 3),
                    (self.x - self.size // 2, self.y - self.size // 3),
                ],
            )
 
 