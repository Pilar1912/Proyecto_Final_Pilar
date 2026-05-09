import random

import pygame
from bullet import Bullet
from config import HEIGHT


class SpaceShipEnemy:
    """Nave espacial enemiga futurista con diseño avanzado."""

    def __init__(self, x, y, size, speed, agil=False):
        self.x = x
        self.y = y
        self.size = size
        self.speed = min(speed, 9)  # Límite de velocidad
        self.agil = agil
        self.direction_y = 1  # Para movimiento zigzag
        self.ship_type = (
            random.choice(["fighter", "scout", "interceptor"])
            if agil
            else random.choice(["freighter", "carrier"])
        )

        # Sistema de luces LED
        self.led_colors = self._get_led_colors()
        self.engine_glow = 255
        self.engine_glow_direction = -1

        # Propulsores
        self.thruster_particles = []

        # Rotación
        self.rotation = 0

    def _get_led_colors(self):
        """Obtiene los colores LED según el tipo de nave."""
        if self.agil:
            return {"primary": (0, 150, 255), "secondary": (0, 255, 100)}  # Cyan/Verde
        else:
            return {"primary": (255, 100, 0), "secondary": (255, 150, 50)}  # Naranja

    def shoot(self):
        """Dispara un proyectil energético."""
        return Bullet(self.x, self.y, 10, "LEFT")

    def move(self):
        """Mueve la nave hacia la izquierda."""
        self.x -= self.speed

        # Movimiento zigzag para naves ágiles
        if self.agil:
            self.y += self.direction_y * 2
            if self.y < 30 or self.y > HEIGHT - 30:
                self.direction_y *= -1

        # Actualizar propulsores
        self._update_engine()

    def _update_engine(self):
        """Actualiza el brillo del motor."""
        self.engine_glow += self.engine_glow_direction * 5
        if self.engine_glow >= 255:
            self.engine_glow = 255
            self.engine_glow_direction = -1
        elif self.engine_glow <= 150:
            self.engine_glow = 150
            self.engine_glow_direction = 1

        # Generar partículas de propulsor ocasionalmente
        if random.random() < 0.3:
            self._create_thruster_particle()

    def _create_thruster_particle(self):
        """Crea una partícula de propulsor."""
        self.thruster_particles.append(
            {
                "x": self.x + random.randint(-5, 5),
                "y": self.y + random.randint(-self.size // 2, self.size // 2),
                "vx": random.uniform(-2, -5),
                "vy": random.uniform(-1, 1),
                "life": random.randint(10, 20),
                "max_life": 20,
                "color": random.choice(
                    [self.led_colors["primary"], self.led_colors["secondary"]]
                ),
            }
        )

    def _update_particles(self):
        """Actualiza las partículas de propulsor."""
        for particle in self.thruster_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.thruster_particles.remove(particle)

    def draw(self, screen, player_x=None, player_y=None):
        """Dibuja la nave espacial con efectos futuristas."""
        self._update_particles()

        # Dibujar partículas de propulsor primero
        for particle in self.thruster_particles:
            alpha = int(200 * (particle["life"] / particle["max_life"]))
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

        x, y = int(self.x), int(self.y)

        if self.ship_type in ["fighter", "interceptor", "scout"]:
            self._draw_fighter(screen, x, y)
        else:
            self._draw_freighter(screen, x, y)

    def _draw_fighter(self, screen, x, y):
        """Dibuja una nave caza/interceptor compacta."""
        # Cuerpo principal
        main_body = [
            (x + self.size // 2, y),  # Punta delantera
            (x - self.size // 2, y - self.size // 3),  # Atrás superior
            (x - self.size // 3, y),  # Atrás centro
            (x - self.size // 2, y + self.size // 3),  # Atrás inferior
        ]
        pygame.draw.polygon(screen, (100, 150, 200), main_body)
        pygame.draw.polygon(screen, (150, 200, 255), main_body, 2)

        # Alas energéticas
        wing_color = self.led_colors["primary"]
        # Ala izquierda
        pygame.draw.line(
            screen, wing_color, (x, y), (x - self.size // 2, y - self.size // 2), 2
        )
        # Ala derecha
        pygame.draw.line(
            screen, wing_color, (x, y), (x - self.size // 2, y + self.size // 2), 2
        )

        # LEDs principales
        pygame.draw.circle(
            screen, self.led_colors["primary"], (x + self.size // 3, y), 3
        )
        pygame.draw.circle(
            screen, self.led_colors["secondary"], (x + self.size // 3, y - 4), 2
        )
        pygame.draw.circle(
            screen, self.led_colors["secondary"], (x + self.size // 3, y + 4), 2
        )

        # Motor de energía trasero
        engine_color = (int(self.engine_glow), int(self.engine_glow * 0.6), 0)
        pygame.draw.circle(screen, engine_color, (x - self.size // 2, y), 4)
        pygame.draw.circle(screen, (255, 200, 0), (x - self.size // 2, y), 4, 1)

    def _draw_freighter(self, screen, x, y):
        """Dibuja una nave de carga más grande."""
        # Cuerpo principal grande
        pygame.draw.rect(
            screen,
            (80, 100, 150),
            (x - self.size // 2, y - self.size // 3, self.size, self.size // 1.5),
        )
        pygame.draw.rect(
            screen,
            (120, 150, 200),
            (x - self.size // 2, y - self.size // 3, self.size, self.size // 1.5),
            2,
        )

        # Domos de carga
        dome_color = (100, 120, 180)
        pygame.draw.circle(screen, dome_color, (x - self.size // 4, y), self.size // 4)
        pygame.draw.circle(
            screen, (150, 180, 220), (x - self.size // 4, y), self.size // 4, 1
        )
        pygame.draw.circle(screen, dome_color, (x + self.size // 4, y), self.size // 5)
        pygame.draw.circle(
            screen, (150, 180, 220), (x + self.size // 4, y), self.size // 5, 1
        )

        # LEDs de carga (múltiples)
        for i in range(-1, 2):
            led_x = x - self.size // 2 + 5
            led_y = y + i * 5
            pygame.draw.circle(screen, self.led_colors["primary"], (led_x, led_y), 2)

        # Propulsores traseros
        pygame.draw.circle(
            screen,
            (int(self.engine_glow), 100, 50),
            (x - self.size // 2, y - self.size // 5),
            3,
        )
        pygame.draw.circle(
            screen,
            (int(self.engine_glow), 100, 50),
            (x - self.size // 2, y + self.size // 5),
            3,
        )

    def get_hit_rect(self):
        """Retorna el rectángulo de colisión."""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size,
        )
