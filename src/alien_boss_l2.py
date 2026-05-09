import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class AlienBoss(Boss):
    """Jefe Nivel 2: Lagarto alienígena biomecánico gigante."""

    def __init__(self, level):
        super().__init__(level, name="BIOMECH ALIEN", size=120)

        # Propiedades visuales
        self.scale_colors = [(80, 150, 100), (60, 130, 80), (100, 170, 120)]
        self.eye_glow = 0
        self.jaw_angle = 0
        self.tail_segments = 6
        self.spark_particles = []

        # Ataques especiales
        self.energy_blast_charge = 0
        self.breath_attack_timer = 0
        self.claw_swipe_active = False

    def _create_energy_particles(self, count=15):
        """Crea partículas de energía."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.spark_particles.append(
                {
                    "x": self.x + random.randint(-30, 30),
                    "y": self.y + random.randint(-30, 30),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(20, 35),
                    "color": random.choice(
                        [(100, 255, 150), (50, 200, 100), (150, 255, 200)]
                    ),
                }
            )

    def _update_particles(self):
        """Actualiza partículas."""
        for particle in self.spark_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.spark_particles.remove(particle)

    def move(self):
        """Movimiento del lagarto."""
        super().move()
        if not self.alive:
            return

        self._update_particles()

        # Animaciones
        self.eye_glow = int(100 + 100 * math.sin(pygame.time.get_ticks() / 200))
        self.jaw_angle = math.sin(pygame.time.get_ticks() / 300) * 0.3
        self.breath_attack_timer += 1

    def take_damage(self, damage):
        """Recibe daño."""
        super().take_damage(damage)
        self._create_energy_particles(15)

    def _create_bullets(self):
        """Crea disparos de energía."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 18
        self.energy_blast_charge += 1

        # Patrón 1: Soplo de energía
        if self.energy_blast_charge % 3 == 0:
            for i in range(-2, 3):
                bullets.append(Bullet(self.x - 50, self.y + i * 10, 14, "LEFT"))
            self._create_energy_particles(20)

        # Patrón 2: Proyectiles en abanico
        elif self.energy_blast_charge % 2 == 0:
            angles = ["LEFT", "DIAG_LEFT"]
            for angle in angles:
                for offset in [-1, 0, 1]:
                    bullets.append(Bullet(self.x - 45, self.y + offset * 12, 12, angle))

        return bullets

    def draw(self, screen):
        """Dibuja el lagarto biomecánico."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        # Cola ondulante
        tail_y = y
        for i in range(self.tail_segments):
            segment_x = x - (i + 1) * 30
            offset = math.sin(pygame.time.get_ticks() / 200 + i * 0.5) * 15
            tail_y += offset

            pygame.draw.circle(
                screen, self.scale_colors[i % 3], (segment_x, int(tail_y)), 12 - i // 2
            )
            pygame.draw.circle(
                screen, (120, 200, 150), (segment_x, int(tail_y)), 12 - i // 2, 1
            )

        # Cuerpo principal
        body_width = 80
        body_height = 100
        body_rect = pygame.Rect(
            x - body_width // 2, y - body_height // 2, body_width, body_height
        )
        pygame.draw.ellipse(screen, self.scale_colors[0], body_rect)
        pygame.draw.ellipse(screen, (100, 180, 130), body_rect, 2)

        # Escamas metálicas
        for i in range(5):
            scale_y = y - 40 + i * 20
            pygame.draw.circle(screen, self.scale_colors[(i) % 3], (x - 20, scale_y), 8)
            pygame.draw.circle(screen, (150, 220, 180), (x - 20, scale_y), 8, 1)
            pygame.draw.circle(
                screen, self.scale_colors[(i + 1) % 3], (x + 20, scale_y), 8
            )
            pygame.draw.circle(screen, (150, 220, 180), (x + 20, scale_y), 8, 1)

        # Cabeza
        head_x, head_y = x + 40, y - 30
        pygame.draw.ellipse(
            screen, self.scale_colors[2], (head_x - 35, head_y - 30, 60, 50)
        )
        pygame.draw.ellipse(
            screen, (100, 180, 130), (head_x - 35, head_y - 30, 60, 50), 2
        )

        # Ojos brillantes
        eye_left_x, eye_left_y = head_x - 15, head_y - 15
        eye_right_x, eye_right_y = head_x + 15, head_y - 15

        pygame.draw.circle(screen, (50, 100, 200), (eye_left_x, eye_left_y), 8)
        pygame.draw.circle(screen, (100, 200, 255), (eye_left_x, eye_left_y), 8, 1)
        pygame.draw.circle(screen, (100, 255, 100), (eye_left_x - 2, eye_left_y - 2), 3)

        pygame.draw.circle(screen, (50, 100, 200), (eye_right_x, eye_right_y), 8)
        pygame.draw.circle(screen, (100, 200, 255), (eye_right_x, eye_right_y), 8, 1)
        pygame.draw.circle(
            screen, (100, 255, 100), (eye_right_x - 2, eye_right_y - 2), 3
        )

        # Mandíbula inferior
        jaw_y = head_y + 15 + int(10 * self.jaw_angle)
        pygame.draw.ellipse(screen, (100, 160, 110), (head_x - 30, jaw_y, 50, 20))
        pygame.draw.ellipse(screen, (120, 180, 130), (head_x - 30, jaw_y, 50, 20), 1)

        # Dientes
        for i in range(5):
            tooth_x = head_x - 25 + i * 10
            pygame.draw.polygon(
                screen,
                (200, 200, 200),
                [
                    (tooth_x, jaw_y),
                    (tooth_x - 3, jaw_y + 8),
                    (tooth_x + 3, jaw_y + 8),
                ],
            )

        # Garras en los lados
        for side in [-1, 1]:
            for i in range(3):
                claw_x = x + side * 50
                claw_y = y - 30 + i * 30
                pygame.draw.line(
                    screen,
                    (150, 100, 100),
                    (claw_x, claw_y),
                    (claw_x + side * 20, claw_y - 10),
                    4,
                )

        # Partículas de energía
        for particle in self.spark_particles:
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

    def get_hit_rect(self):
        """Retorna el hitbox."""
        return pygame.Rect(
            self.x - 60,
            self.y - 60,
            120,
            120,
        )
