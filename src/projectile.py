import math
import random

import pygame
from config import CYAN, HEIGHT, MAGENTA, WHITE, WIDTH


class Projectile:
    """Clase para proyectiles especiales (bombitas explosivas) de los jefes.

    Diferencias con Bullet:
    - Área de explosión más grande
    - Más daño
    - Efectos visuales futuristas (energía, plasma)
    - Movimiento hacia el jugador
    """

    def __init__(self, x, y, target_x, target_y, speed=8):
        """
        Crea un proyectil explosivo que se mueve hacia el objetivo.

        Args:
            x: Posición inicial X
            y: Posición inicial Y
            target_x: Posición X del objetivo (jugador)
            target_y: Posición Y del objetivo (jugador)
            speed: Velocidad de movimiento del proyectil
        """
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.radius = 12  # Radio del projectil
        self.explosion_radius = 80  # Radio de explosión cuando impacta
        self.damage = 15  # Daño más alto que las balas normales

        # Efectos visuales
        self.frame = 0
        self.trail_particles = []
        self.energy_rings = []
        self.glow_intensity = 255

        # Crear anillos de energía iniciales
        for i in range(3):
            self.energy_rings.append(
                {
                    "radius": self.radius + (i * 3),
                    "opacity": 200 - (i * 60),
                    "pulse": i * 1.5,
                }
            )

    def move(self):
        """Mueve el proyectil hacia el objetivo (jugador)."""
        # Calcular dirección hacia el jugador
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            # Normalizar y mover
            vx = (dx / distance) * self.speed
            vy = (dy / distance) * self.speed
            self.x += vx
            self.y += vy

        self.frame += 1

        # Crear partículas de rastro
        if self.frame % 2 == 0:
            self._create_trail_particle()

        # Actualizar partículas de rastro
        self._update_trail_particles()

        # Actualizar anillos de energía
        for ring in self.energy_rings:
            ring["pulse"] += 0.15
            ring["opacity"] = int(200 - (60 * abs(math.sin(ring["pulse"]))))

    def _create_trail_particle(self):
        """Crea partículas de rastro (energía/plasma)."""
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(0.5, 2)
        self.trail_particles.append(
            {
                "x": self.x,
                "y": self.y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": random.randint(10, 20),
                "max_life": 20,
                "color": random.choice([CYAN, MAGENTA, (100, 255, 255)]),
            }
        )

    def _update_trail_particles(self):
        """Actualiza las partículas de rastro."""
        for particle in self.trail_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.trail_particles.remove(particle)

    def draw(self, screen):
        """Dibuja el proyectil con efectos visuales futuristas."""
        x, y = int(self.x), int(self.y)

        # Dibujar partículas de rastro
        for particle in self.trail_particles:
            alpha = int(255 * (particle["life"] / particle["max_life"]))
            # Usando círculos para simular plasma
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

        # Dibujar anillos de energía pulsante
        for ring in self.energy_rings:
            if ring["opacity"] > 0:
                # Dibujar anillo
                pygame.draw.circle(screen, CYAN, (x, y), int(ring["radius"]), 2)

        # Núcleo del proyectil (gradiente simulado con múltiples círculos)
        pygame.draw.circle(screen, MAGENTA, (x, y), self.radius)
        pygame.draw.circle(screen, CYAN, (x, y), self.radius - 3, 2)

        # Efecto de brillo central pulsante
        glow_size = int(self.radius * 0.4)
        pygame.draw.circle(screen, WHITE, (x, y), glow_size)

        # Rayos de energía desde el centro (cada 6 frames)
        if self.frame % 6 == 0:
            for i in range(4):
                angle = (i * math.pi / 2) + (self.frame * 0.05)
                ex = x + math.cos(angle) * (self.radius + 5)
                ey = y + math.sin(angle) * (self.radius + 5)
                pygame.draw.line(screen, CYAN, (x, y), (int(ex), int(ey)), 1)

    def is_out_of_bounds(self):
        """Verifica si el proyectil está fuera del área visible."""
        return (
            self.x < -50 or self.x > WIDTH + 50 or self.y < -50 or self.y > HEIGHT + 50
        )

    def get_explosion_rect(self):
        """Retorna el rectángulo de área de explosión."""
        return pygame.Rect(
            self.x - self.explosion_radius,
            self.y - self.explosion_radius,
            self.explosion_radius * 2,
            self.explosion_radius * 2,
        )
