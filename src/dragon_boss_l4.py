import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class DragonBoss(Boss):
    """Jefe Nivel 4: Dragón espacial mecánico gigante."""

    def __init__(self, level):
        super().__init__(level, name="COSMIC DRAGON", size=140)

        # Propiedades visuales
        self.body_color = (100, 50, 150)
        self.armor_color = (150, 100, 200)
        self.fire_particles = []
        self.wing_particles = []

        # Alas de energía
        self.wing_angle = 0
        self.wing_glow = 0

        # Fuego cósmico
        self.fire_breath_active = False
        self.fire_breath_cooldown = 0
        self.fire_breath_cooldown_max = 80

        # Propulsores
        self.thruster_glow = [0, 0]

    def _create_fire_particles(self, x, y, count=20):
        """Crea partículas de fuego cósmico."""
        for _ in range(count):
            angle = random.uniform(-0.5, 0.5)  # Dispersión frontal
            speed = random.uniform(4, 8)
            self.fire_particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": -math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(15, 30),
                    "max_life": 30,
                    "color": random.choice(
                        [(255, 150, 50), (255, 100, 0), (255, 200, 100)]
                    ),
                }
            )

    def _create_wing_particles(self):
        """Crea partículas de energía de las alas."""
        for i in range(2):
            for _ in range(5):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(1, 3)
                self.wing_particles.append(
                    {
                        "x": self.x + random.randint(-50, 50),
                        "y": self.y + (i - 1) * 60 + random.randint(-20, 20),
                        "vx": math.cos(angle) * speed,
                        "vy": math.sin(angle) * speed,
                        "life": random.randint(10, 20),
                        "color": (100, 200, 255),
                    }
                )

    def _update_particles(self):
        """Actualiza partículas."""
        for particle in self.fire_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.fire_particles.remove(particle)

        for particle in self.wing_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.wing_particles.remove(particle)

    def move(self):
        """Movimiento del dragón."""
        super().move()
        if not self.alive:
            return

        self._update_particles()

        # Animaciones de alas
        self.wing_angle += 0.08
        self.wing_glow = int(150 + 100 * abs(math.sin(self.wing_angle)))

        # Control de fuego
        self.fire_breath_cooldown -= 1

        # Propulsores
        self.thruster_glow[0] = int(150 + 100 * math.sin(pygame.time.get_ticks() / 150))
        self.thruster_glow[1] = int(150 + 100 * math.cos(pygame.time.get_ticks() / 150))

        # Crear partículas ocasionalmente
        if random.random() < 0.2:
            self._create_wing_particles()

    def take_damage(self, damage):
        """Recibe daño."""
        super().take_damage(damage)
        self._create_fire_particles(self.x, self.y, count=20)

    def _create_bullets(self):
        """Crea disparos de fuego y energía."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 20

        # Fuego cósmico
        if self.fire_breath_cooldown <= 0:
            for i in range(-3, 4):
                bullets.append(Bullet(self.x - 60, self.y + i * 8, 15, "LEFT"))
            self._create_fire_particles(self.x - 60, self.y, count=30)
            self.fire_breath_cooldown = self.fire_breath_cooldown_max

        # Proyectiles de energía de las alas
        for i in range(-1, 2):
            bullets.append(Bullet(self.x - 40, self.y - 50 + i * 50, 13, "DIAG_LEFT"))

        return bullets

    def draw(self, screen):
        """Dibuja el dragón mecánico."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        # Cola ondulante
        tail_length = 4
        tail_x, tail_y = x - 100, y
        for i in range(tail_length):
            segment_offset = math.sin(pygame.time.get_ticks() / 200 + i) * 15
            next_tail_x = tail_x - 40
            next_tail_y = tail_y + segment_offset
            pygame.draw.line(
                screen,
                (150, 100, 200),
                (tail_x, tail_y),
                (next_tail_x, next_tail_y),
                15,
            )
            tail_x, tail_y = next_tail_x, next_tail_y

        # Cuerpo principal
        body_points = [
            (x - 60, y),  # Centro trasero
            (x - 20, y - 40),  # Lomo
            (x + 40, y - 35),  # Cuello
            (x + 60, y),  # Cabeza frontal
            (x + 40, y + 35),  # Vientre
            (x - 20, y + 40),  # Vientre trasero
        ]
        pygame.draw.polygon(screen, self.body_color, body_points)
        pygame.draw.polygon(screen, self.armor_color, body_points, 3)

        # Armadura metálica
        for i, point in enumerate(body_points[:-1]):
            next_point = body_points[i + 1]
            mid_x = (point[0] + next_point[0]) // 2
            mid_y = (point[1] + next_point[1]) // 2
            pygame.draw.circle(screen, (200, 150, 250), (mid_x, mid_y), 8)
            pygame.draw.circle(screen, (255, 200, 255), (mid_x, mid_y), 8, 1)

        # Alas de energía (izquierda)
        wing_width = 70
        wing_height = 50
        wing_angle_rad = math.sin(self.wing_angle) * 0.4

        # Ala izquierda
        wing_points_left = [
            (x - 30, y - 50),
            (
                x - 30 - int(wing_width * math.cos(wing_angle_rad)),
                y - 50 - int(wing_height * math.sin(wing_angle_rad)),
            ),
            (x + 10, y - 80),
        ]
        pygame.draw.polygon(screen, (100, 150, 255), wing_points_left)
        pygame.draw.polygon(screen, (150, 200, 255), wing_points_left, 2)

        # Ala derecha (espejo)
        wing_points_right = [
            (x - 30, y + 50),
            (
                x - 30 - int(wing_width * math.cos(wing_angle_rad)),
                y + 50 + int(wing_height * math.sin(wing_angle_rad)),
            ),
            (x + 10, y + 80),
        ]
        pygame.draw.polygon(screen, (100, 150, 255), wing_points_right)
        pygame.draw.polygon(screen, (150, 200, 255), wing_points_right, 2)

        # Efectos de energía en las alas
        pygame.draw.line(
            screen, (150, self.wing_glow, 255), (x - 30, y - 50), (x + 10, y - 80), 3
        )
        pygame.draw.line(
            screen, (150, self.wing_glow, 255), (x - 30, y + 50), (x + 10, y + 80), 3
        )

        # Cabeza del dragón
        head_points = [
            (x + 50, y),  # Punta del hocico
            (x + 30, y - 20),  # Arriba del hocico
            (x + 30, y + 20),  # Abajo del hocico
        ]
        pygame.draw.polygon(screen, self.body_color, head_points)
        pygame.draw.polygon(screen, self.armor_color, head_points, 2)

        # Ojos del dragón
        pygame.draw.circle(screen, (0, 255, 150), (x + 40, y - 10), 8)
        pygame.draw.circle(screen, (100, 255, 200), (x + 40, y - 10), 8, 1)
        pygame.draw.circle(screen, (0, 255, 150), (x + 40, y + 10), 8)
        pygame.draw.circle(screen, (100, 255, 200), (x + 40, y + 10), 8, 1)

        # Fauces
        pygame.draw.line(screen, (255, 100, 0), (x + 50, y - 5), (x + 65, y - 5), 3)
        pygame.draw.line(screen, (255, 100, 0), (x + 50, y + 5), (x + 65, y + 5), 3)

        # Cuernos
        pygame.draw.line(
            screen, self.armor_color, (x + 35, y - 25), (x + 40, y - 40), 3
        )
        pygame.draw.line(
            screen, self.armor_color, (x + 35, y + 25), (x + 40, y + 40), 3
        )

        # Propulsores traseros
        pygame.draw.circle(
            screen, (self.thruster_glow[0], 100, 200), (x - 80, y - 25), 12
        )
        pygame.draw.circle(screen, (200, 150, 255), (x - 80, y - 25), 12, 1)
        pygame.draw.circle(
            screen, (self.thruster_glow[1], 100, 200), (x - 80, y + 25), 12
        )
        pygame.draw.circle(screen, (200, 150, 255), (x - 80, y + 25), 12, 1)

        # Partículas de fuego
        for particle in self.fire_particles:
            alpha_ratio = particle["life"] / particle["max_life"]
            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                int(3 * alpha_ratio),
            )

        # Partículas de alas
        for particle in self.wing_particles:
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

    def get_hit_rect(self):
        """Retorna el hitbox."""
        return pygame.Rect(
            self.x - 70,
            self.y - 70,
            140,
            140,
        )
