import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class GoblinBoss(Boss):
    """Jefe Nivel 3: Duende oscuro futurista, pequeño pero peligroso."""

    def __init__(self, level):
        super().__init__(level, name="DARK GOBLIN", size=60)

        # Propiedades visuales
        self.skin_color = (30, 40, 80)
        self.eyes_color = (255, 50, 50)
        self.glow_effect = 0
        self.teleport_cooldown = 0
        self.teleport_cooldown_max = 60
        self.weapon_glow = 0
        self.laser_particles = []

        # Velocidad aumentada
        self.speed_y = 3
        self.charge_speed = 8

    def _create_laser_particles(self, x, y, count=10):
        """Crea partículas de láser."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 6)
            self.laser_particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(10, 20),
                    "color": (200, 50, 255),
                }
            )

    def _update_particles(self):
        """Actualiza partículas de láser."""
        for particle in self.laser_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.laser_particles.remove(particle)

    def move(self):
        """Movimiento especial del duende - muy rápido."""
        if not self.alive:
            return

        self._update_particles()

        if not self.charging and not self.returning:
            self.y += self.speed_y * self.direction_y
            if self.y <= self.size:
                self.direction_y = 1
            elif self.y >= 1080 - self.size:
                self.direction_y = -1

            self.charge_cooldown -= 1
            # Más frecuentes que otros jefes
            if self.charge_cooldown <= 0 and random.randint(0, 100) < 5:
                self.charging = True

        elif self.charging:
            self.x -= self.charge_speed
            if self.x <= 1920 // 2:
                self.charging = False
                self.returning = True
                # Teletransportarse a posición aleatoria
                self.teleport_cooldown = self.teleport_cooldown_max

        elif self.returning:
            self.x += self.charge_speed
            if self.x >= self.base_x:
                self.x = self.base_x
                self.returning = False
                self.charge_cooldown = self.charge_cooldown_max

        # Animaciones
        self.glow_effect = int(100 + 100 * abs(math.sin(pygame.time.get_ticks() / 150)))
        self.weapon_glow = int(150 + 100 * abs(math.cos(pygame.time.get_ticks() / 100)))

    def take_damage(self, damage):
        """Recibe daño."""
        super().take_damage(damage)
        self._create_laser_particles(self.x, self.y, count=15)

    def _create_bullets(self):
        """Crea disparos de láser rápidos."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 15  # Más rápido que otros

        # Patrón 1: Rayos láser directos (muy rápidos)
        for i in range(-1, 2):
            bullets.append(Bullet(self.x - 25, self.y + i * 10, 16, "LEFT"))

        # Patrón 2: Rayos caoticos ocasionales
        if random.random() < 0.4:
            for _ in range(2):
                bullet = Bullet(
                    self.x - 25, self.y, 15, random.choice(["LEFT", "DIAG_LEFT"])
                )
                bullets.append(bullet)

        self._create_laser_particles(self.x - 25, self.y, count=8)

        return bullets

    def draw(self, screen):
        """Dibuja el duende oscuro futurista."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        # Aura mágica oscura
        aura_radius = int(35 + 10 * math.sin(pygame.time.get_ticks() / 200))
        aura_surf = pygame.Surface((aura_radius * 2, aura_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            aura_surf, (100, 30, 150, 80), (aura_radius, aura_radius), aura_radius
        )
        screen.blit(aura_surf, (x - aura_radius, y - aura_radius))

        # Cuerpo pequeño
        pygame.draw.ellipse(screen, self.skin_color, (x - 18, y - 20, 36, 40))
        pygame.draw.ellipse(screen, (100, 50, 150), (x - 18, y - 20, 36, 40), 2)

        # Cabeza puntiaguda
        points = [
            (x, y - 35),  # Punta superior
            (x - 15, y - 15),
            (x + 15, y - 15),
        ]
        pygame.draw.polygon(screen, self.skin_color, points)
        pygame.draw.polygon(screen, (100, 50, 150), points, 2)

        # Orejas puntiagudas
        pygame.draw.polygon(
            screen,
            self.skin_color,
            [(x - 15, y - 25), (x - 22, y - 40), (x - 10, y - 30)],
        )
        pygame.draw.polygon(
            screen,
            self.skin_color,
            [(x + 15, y - 25), (x + 22, y - 40), (x + 10, y - 30)],
        )

        # Ojos rojos brillantes
        pygame.draw.circle(screen, (255, 50, 50), (x - 8, y - 20), 5)
        pygame.draw.circle(screen, (255, 100, 100), (x - 8, y - 20), 5, 1)
        pygame.draw.circle(screen, (255, 200, 200), (x - 7, y - 22), 2)

        pygame.draw.circle(screen, (255, 50, 50), (x + 8, y - 20), 5)
        pygame.draw.circle(screen, (255, 100, 100), (x + 8, y - 20), 5, 1)
        pygame.draw.circle(screen, (255, 200, 200), (x + 7, y - 22), 2)

        # Boca malvada
        pygame.draw.line(screen, (100, 30, 100), (x - 5, y - 10), (x + 5, y - 10), 2)
        pygame.draw.line(screen, (100, 30, 100), (x - 5, y - 10), (x, y - 5), 1)
        pygame.draw.line(screen, (100, 30, 100), (x + 5, y - 10), (x, y - 5), 1)

        # Brazos con armas de energía
        # Brazo izquierdo
        pygame.draw.line(screen, self.skin_color, (x - 18, y - 5), (x - 40, y - 10), 4)
        # Arma de energía izquierda
        weapon_left_color = (self.weapon_glow, 50, 255)
        pygame.draw.circle(screen, weapon_left_color, (x - 42, y - 10), 8)
        pygame.draw.circle(screen, (200, 100, 255), (x - 42, y - 10), 8, 1)

        # Brazo derecho
        pygame.draw.line(screen, self.skin_color, (x + 18, y - 5), (x + 40, y - 10), 4)
        # Arma de energía derecha
        weapon_right_color = (self.weapon_glow, 50, 255)
        pygame.draw.circle(screen, weapon_right_color, (x + 42, y - 10), 8)
        pygame.draw.circle(screen, (200, 100, 255), (x + 42, y - 10), 8, 1)

        # Piernas digitales
        for leg_offset in [-8, 8]:
            pygame.draw.line(
                screen,
                (50, 100, 150),
                (x + leg_offset, y + 20),
                (x + leg_offset, y + 30),
                3,
            )
            pygame.draw.circle(screen, (100, 150, 200), (x + leg_offset, y + 32), 4)

        # Efecto de teletransportación (si está cargando)
        if self.charging:
            for _ in range(3):
                offset_x = random.randint(-10, 10)
                offset_y = random.randint(-10, 10)
                alpha = random.randint(50, 150)
                pygame.draw.rect(
                    screen,
                    (50, 100, 200),
                    (x + offset_x - 18, y + offset_y - 20, 36, 40),
                    1,
                )

        # Partículas de láser
        for particle in self.laser_particles:
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

    def get_hit_rect(self):
        """Retorna el hitbox."""
        return pygame.Rect(
            self.x - 20,
            self.y - 35,
            40,
            70,
        )
