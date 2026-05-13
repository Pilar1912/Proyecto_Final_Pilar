import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class PhoenixBoss(Boss):
    """Jefe Nivel 6 (Final): Fénix cósmico de fuego y energía.

    Mecánica especial: El jugador tiene 20 segundos para derrotar este jefe.
    Si se agota el tiempo, el jugador pierde automáticamente.
    """

    def __init__(self, level):
        super().__init__(level, name="COSMIC PHOENIX", size=130)

        self.wing_spread = 0
        self.flame_particles = []
        self.energy_particles = []
        self.body_color = (200, 100, 30)
        self.fire_intensity = 0
        self.flight_height_offset = 0

        # MECÁNICA ESPECIAL: Temporizador de 20 segundos (600 frames a 30 FPS)
        self.boss_timer = 600  # 20 segundos
        self.time_out = False  # Flag para detectar cuando se acaba el tiempo

    def _create_flame_particles(self, x, y, count=25):
        """Crea partículas de fuego."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.flame_particles.append(
                {
                    "x": x,
                    "y": y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(15, 30),
                    "max_life": 30,
                    "color": random.choice(
                        [(255, 150, 0), (255, 100, 0), (255, 200, 100)]
                    ),
                }
            )

    def _create_energy_particles(self, count=15):
        """Crea partículas de energía."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.energy_particles.append(
                {
                    "x": self.x + random.randint(-50, 50),
                    "y": self.y + random.randint(-50, 50),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(10, 25),
                    "color": (100, 200, 255),
                }
            )

    def _update_particles(self):
        """Actualiza partículas."""
        for particle in self.flame_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["vy"] += 0.1  # Gravedad
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.flame_particles.remove(particle)

        for particle in self.energy_particles[:]:
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["life"] -= 1
            if particle["life"] <= 0:
                self.energy_particles.remove(particle)

    def move(self):
        """Movimiento del fénix."""
        super().move()
        if not self.alive:
            return

        # Actualizar temporizador especial del Phoenix (20 segundos)
        if self.boss_timer > 0:
            self.boss_timer -= 1
        else:
            self.time_out = True

        self._update_particles()

        # Animación de alas
        self.wing_spread = 50 + 30 * math.sin(pygame.time.get_ticks() / 200)

        # Movimiento ondulante
        self.flight_height_offset = 30 * math.sin(pygame.time.get_ticks() / 400)

        # Intensidad de fuego
        self.fire_intensity = int(
            150 + 100 * abs(math.sin(pygame.time.get_ticks() / 150))
        )

    def get_remaining_time(self):
        """Retorna el tiempo restante en segundos."""
        return max(0, self.boss_timer // 30)  # Convertir frames a segundos (30 FPS)

    def has_time_out(self):
        """Retorna True si se ha agotado el tiempo."""
        return self.time_out

    def take_damage(self, damage):
        """Recibe daño."""
        super().take_damage(damage)
        self._create_flame_particles(self.x, self.y, count=30)
        self._create_energy_particles(20)

    def _create_bullets(self):
        """Crea disparos de fuego y energía."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 17

        # Fuego frontal intenso
        for i in range(-2, 3):
            bullets.append(Bullet(self.x - 55, self.y + i * 12, 16, "LEFT"))

        # Rayos de energía laterales
        bullets.append(Bullet(self.x - 40, self.y - 50, 14, "DIAG_LEFT"))
        bullets.append(Bullet(self.x - 40, self.y + 50, 14, "DIAG_LEFT"))

        self._create_flame_particles(self.x - 60, self.y, count=30)

        return bullets

    def draw(self, screen):
        """Dibuja el fénix con efectos visuales futuristas e intensos."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y + self.flight_height_offset)

        # Efecto de estrés: si queda poco tiempo, el Phoenix brilla rojo
        time_remaining = self.get_remaining_time()
        stress_level = max(
            0, 1 - (time_remaining / 20)
        )  # 0 a 1, siendo 1 máximo estrés

        # Halo de fuego con efecto de estrés
        halo_radius = int(60 + 20 * math.sin(pygame.time.get_ticks() / 200))
        halo_color_intensity = int(255 * stress_level)

        # Crear halos concéntricos para efecto de energía
        for halo_offset in range(3):
            halo_r = halo_radius + (halo_offset * 10)
            halo_alpha = int(60 * (1 - halo_offset * 0.3))
            halo_surf = pygame.Surface((halo_r * 2, halo_r * 2), pygame.SRCALPHA)

            # Color cambia a rojo según estrés
            base_color = (255, int(100 * (1 - stress_level)), 0)
            stress_color = (255, 0, 0)
            color = (
                int(
                    base_color[0] * (1 - stress_level) + stress_color[0] * stress_level
                ),
                int(
                    base_color[1] * (1 - stress_level) + stress_color[1] * stress_level
                ),
                int(
                    base_color[2] * (1 - stress_level) + stress_color[2] * stress_level
                ),
            )

            pygame.draw.circle(
                halo_surf, color + (halo_alpha,), (halo_r, halo_r), halo_r
            )
            screen.blit(halo_surf, (x - halo_r, y - halo_r))

        # Cola larga y ondulante
        tail_length = 5
        tail_x, tail_y = x - 80, y
        for i in range(tail_length):
            segment_offset = math.sin(pygame.time.get_ticks() / 200 + i * 0.5) * 15
            next_tail_x = tail_x - 30
            next_tail_y = tail_y + segment_offset

            color = (255, int(150 - i * 20), 0)
            pygame.draw.line(
                screen, color, (tail_x, tail_y), (next_tail_x, next_tail_y), 12 - i
            )
            tail_x, tail_y = next_tail_x, next_tail_y

        # Cuerpo principal
        body_points = [
            (x - 30, y),
            (x + 30, y - 20),
            (x + 40, y),
            (x + 30, y + 20),
        ]
        pygame.draw.polygon(screen, self.body_color, body_points)
        pygame.draw.polygon(screen, (255, 150, 50), body_points, 2)

        # Alas
        # Ala superior izquierda
        wing_points_left = [
            (x - 20, y - 10),
            (x - 20 - int(self.wing_spread), y - 40),
            (x, y - 20),
        ]
        pygame.draw.polygon(screen, (255, self.fire_intensity, 100), wing_points_left)
        pygame.draw.polygon(screen, (255, 200, 150), wing_points_left, 1)

        # Ala superior derecha
        wing_points_right = [
            (x + 20, y - 10),
            (x + 20 + int(self.wing_spread), y - 40),
            (x, y - 20),
        ]
        pygame.draw.polygon(screen, (255, self.fire_intensity, 100), wing_points_right)
        pygame.draw.polygon(screen, (255, 200, 150), wing_points_right, 1)

        # Cabeza
        pygame.draw.circle(screen, self.body_color, (x + 35, y), 15)
        pygame.draw.circle(screen, (255, 150, 50), (x + 35, y), 15, 1)

        # Ojos brillantes - cambian de color según estrés
        eye_color = (
            int(255 * (1 - stress_level) + 255 * stress_level),
            int(255 * (1 - stress_level) + 50 * stress_level),
            int(100 * (1 - stress_level)),
        )
        pygame.draw.circle(screen, eye_color, (x + 40, y - 5), 5)
        pygame.draw.circle(screen, (255, 255, 200), (x + 40, y - 5), 5, 1)
        pygame.draw.circle(screen, eye_color, (x + 40, y + 5), 5)
        pygame.draw.circle(screen, (255, 255, 200), (x + 40, y + 5), 5, 1)

        # Pico
        pygame.draw.polygon(
            screen,
            (200, 100, 0),
            [
                (x + 50, y),
                (x + 60, y - 3),
                (x + 60, y + 3),
            ],
        )

        # EFECTOS FUTURISTAS: Rayos de energía cósmica
        if stress_level > 0.3:  # Más rayos cuando hay estrés
            num_rays = int(8 + stress_level * 12)
            for i in range(num_rays):
                angle = (i / num_rays) * (2 * math.pi) + (pygame.time.get_ticks() / 100)
                ray_length = int(50 + 30 * stress_level)
                end_x = x + math.cos(angle) * ray_length
                end_y = y + math.sin(angle) * ray_length
                color = (100, 200 + int(55 * stress_level), 255)
                pygame.draw.line(screen, color, (x, y), (int(end_x), int(end_y)), 1)

        # Partículas de fuego
        for particle in self.flame_particles:
            alpha_ratio = particle["life"] / particle["max_life"]
            pygame.draw.circle(
                screen,
                particle["color"],
                (int(particle["x"]), int(particle["y"])),
                int(3 * alpha_ratio),
            )

        # Partículas de energía
        for particle in self.energy_particles:
            pygame.draw.circle(
                screen, particle["color"], (int(particle["x"]), int(particle["y"])), 2
            )

        # ONDA DE CHOQUE bajo estrés
        if stress_level > 0.5:
            shock_radius = int(100 + 50 * math.sin(pygame.time.get_ticks() / 100))
            shock_color = (255, int(100 * (1 - stress_level)), 0)
            pygame.draw.circle(screen, shock_color, (x, y), shock_radius, 2)

    def get_hit_rect(self):
        """Retorna el hitbox."""
        return pygame.Rect(
            self.x - 50,
            self.y - 60,
            100,
            120,
        )
