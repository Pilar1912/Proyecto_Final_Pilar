import math
import os

import pygame

from bullet import Bullet
from config import HEIGHT, RED, YELLOW


# Sprites cargados globalmente
_SPRITE_RED = None
_SPRITE_YELLOW = None


def _load_enemy_sprites():
    """Carga los sprites PNG de enemigos. Se ejecuta una vez."""
    global _SPRITE_RED, _SPRITE_YELLOW
    if _SPRITE_RED is not None:
        return
    
    try:
        assets_path = os.path.join(os.path.dirname(__file__), '..', 'assets')
        _SPRITE_RED = pygame.image.load(os.path.join(assets_path, 'enemy_red.png')).convert_alpha()
        _SPRITE_YELLOW = pygame.image.load(os.path.join(assets_path, 'enemy_yellow.png')).convert_alpha()
    except Exception as e:
        print(f"Advertencia: No se pudieron cargar sprites: {e}")
        _SPRITE_RED = None
        _SPRITE_YELLOW = None


# --- Enemigos espaciales: criaturas diferenciadas solo por color ---
class SpaceCreature:
    """Base para criaturas espaciales enemigas."""
    def __init__(self, x, y, size, speed, color, kind):
        self.x = x
        self.y = y
        self.size = size
        self.speed = min(speed, 9)
        self.kind = kind  # 'red' o 'yellow'
        self.color = color
        self.direction_x = 1
        _load_enemy_sprites()

    def shoot(self):
        return Bullet(self.x, self.y, 10, "LEFT")

    def move(self):
        self.x -= self.speed
        if self.kind == 'yellow':
            self.y += self.direction_x * 2
            if self.y < 30 or self.y > HEIGHT - 30:
                self.direction_x *= -1

    def draw(self, screen, player_x=None, player_y=None):
        """Dibuja el sprite PNG del enemigo."""
        if self.kind == 'red' and _SPRITE_RED:
            sprite = _SPRITE_RED
        elif self.kind == 'yellow' and _SPRITE_YELLOW:
            sprite = _SPRITE_YELLOW
        else:
            # Fallback: dibujar forma simple si no hay sprite
            s = self.size
            body = [
                (self.x - s * 0.45, self.y),
                (self.x, self.y - s * 0.22),
                (self.x + s * 0.3, self.y),
                (self.x, self.y + s * 0.22),
            ]
            pygame.draw.polygon(screen, self.color, body)
            pygame.draw.polygon(screen, (40, 40, 40), body, 2)
            return
        
        # Escalar el sprite al tamaño deseado
        scaled_sprite = pygame.transform.scale(sprite, (self.size, self.size))
        rect = scaled_sprite.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(scaled_sprite, rect)


# Alias para compatibilidad con el resto del juego
class Enemy(SpaceCreature):
    def __init__(self, x, y, size, speed, agil=False):
        # Rojo: criatura tipo A, Amarillo: criatura tipo B
        if agil:
            color = (255, 255, 0)  # Amarillo
            kind = 'yellow'
        else:
            color = (220, 20, 20)  # Rojo
            kind = 'red'
        super().__init__(x, y, size, speed, color, kind)
