import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class KrakenBoss(Boss):
    """Jefe Nivel 5: Kraken cósmico oscuro."""

    def __init__(self, level):
        super().__init__(level, name="COSMIC KRAKEN", size=150)

        self.tentacle_count = 8
        self.tentacles = [
            {"angle": i * 2 * math.pi / self.tentacle_count, "wave": 0}
            for i in range(self.tentacle_count)
        ]
        self.eye_particles = []
        self.ink_particles = []
        self.body_color = (50, 30, 80)

    def _create_ink_particles(self, count=25):
        """Crea partículas de tinta."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            self.ink_particles.append(
                {
                    "x": self.x + random.randint(-40, 40),
                    "y": self.y + random.randint(-40, 40),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(20, 35),
                    "max_life": 35,
                    "size": random.randint(3, 8),
                }
            )

    def _update_particles(self):
        """Actualiza partículas."""
        for particle in self.ink_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.ink_particles.remove(particle)

    def move(self):
        """Movimiento del kraken."""
        super().move()
        if not self.alive:
            return

        self._update_particles()

        # Animación de tentáculos
        for tentacle in self.tentacles:
            tentacle["wave"] += 0.03

    def take_damage(self, damage):
        """Recibe daño."""
        super().take_damage(damage)
        self._create_ink_particles(20)

    def _create_bullets(self):
        """Crea disparos de tinta."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 18

        # Disparos desde tentáculos
        for i in range(3):
            angle = 0.3 + i * 0.3
            bullets.append(Bullet(self.x - 50, self.y - 40 + i * 40, 14, "LEFT"))

        self._create_ink_particles(15)
        return bullets

    def draw(self, screen):
        """Dibuja el kraken."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        # Tentáculos ondulantes
        for idx, tentacle in enumerate(self.tentacles):
            tentacle_length = 80
            tentacle_x = x
            tentacle_y = y

            for segment in range(5):
                wave_offset = math.sin(tentacle["wave"] + segment) * 20
                next_x = tentacle_x - tentacle_length // 5
                next_y = tentacle_y + wave_offset

                pygame.draw.line(
                    screen,
                    (100, 50, 150),
                    (tentacle_x, tentacle_y),
                    (next_x, next_y),
                    10,
                )
                tentacle_x, tentacle_y = next_x, next_y

        # Cuerpo principal
        pygame.draw.circle(screen, self.body_color, (x, y), 50)
        pygame.draw.circle(screen, (100, 70, 150), (x, y), 50, 2)

        # Ojos grandes
        eye_offset = 25
        pygame.draw.circle(screen, (200, 100, 255), (x - eye_offset, y - 15), 12)
        pygame.draw.circle(screen, (100, 150, 200), (x - eye_offset, y - 15), 12, 1)
        pygame.draw.circle(screen, (50, 50, 50), (x - eye_offset - 4, y - 18), 5)

        pygame.draw.circle(screen, (200, 100, 255), (x + eye_offset, y - 15), 12)
        pygame.draw.circle(screen, (100, 150, 200), (x + eye_offset, y - 15), 12, 1)
        pygame.draw.circle(screen, (50, 50, 50), (x + eye_offset - 4, y - 18), 5)

        # Partículas
        for particle in self.ink_particles:
            color = (50, 30, 80)
            alpha = int(100 * (particle["life"] / particle["max_life"]))
            pygame.draw.circle(
                screen,
                color,
                (int(particle["x"]), int(particle["y"])),
                particle["size"],
            )

    def get_hit_rect(self):
        """Retorna el hitbox."""
        return pygame.Rect(self.x - 60, self.y - 60, 120, 120)
