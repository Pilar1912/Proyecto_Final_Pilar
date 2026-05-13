import math
import random

import pygame
from boss import Boss
from bullet import Bullet


class RobotBoss(Boss):
    """Jefe Nivel 1: Robot gigante de combate futurista."""

    def __init__(self, level):
        super().__init__(level, name="COMBAT ROBOT", size=100)

        # Propiedades visuales
        self.armor_color = (60, 60, 80)
        self.damage_spots = []
        self.spark_particles = []

        # LEDs dinámicos
        self.red_led_brightness = 255
        self.blue_led_brightness = 100
        self.led_pulse = 0

        # Cañones
        self.cannon_left_charge = 0
        self.cannon_right_charge = 0
        self.cannon_max_charge = 30

        # Brazos mecánicos
        self.arm_left_extension = 0
        self.arm_right_extension = 0

        # Ataque especial
        self.attack_pattern = 0
        self.pattern_timer = 0

    def _create_sparks(self, count=8):
        """Crea partículas de chispa."""
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            self.spark_particles.append(
                {
                    "x": self.x + random.randint(-20, 20),
                    "y": self.y + random.randint(-20, 20),
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.randint(15, 25),
                    "color": (255, 200, 0),
                }
            )

    def _update_particles(self):
        """Actualiza las partículas."""
        for spark in self.spark_particles[:]:
            spark["x"] += spark["vx"]
            spark["y"] += spark["vy"]
            spark["vy"] += 0.15  # Gravedad
            spark["life"] -= 1
            if spark["life"] <= 0:
                self.spark_particles.remove(spark)

    def move(self):
        """Movimiento del robot."""
        super().move()
        if not self.alive:
            return

        self._update_particles()

        # Actualizar LEDs
        self.led_pulse += 0.05
        self.red_led_brightness = int(150 + 100 * abs(math.sin(self.led_pulse)))
        self.blue_led_brightness = int(100 + 100 * abs(math.cos(self.led_pulse)))

        # Cargar cañones
        if self.cannon_left_charge < self.cannon_max_charge:
            self.cannon_left_charge += 0.5
        if self.cannon_right_charge < self.cannon_max_charge:
            self.cannon_right_charge += 0.5

        # Brazos mecánicos
        self.arm_left_extension = 0.3 + 0.2 * math.sin(self.frame_count * 0.05)
        self.arm_right_extension = 0.3 + 0.2 * math.cos(self.frame_count * 0.05)

    def take_damage(self, damage):
        """El robot recibe daño."""
        super().take_damage(damage)
        self._create_sparks(10)
        if not self.alive:
            for _ in range(20):
                self._create_sparks(8)

    def _create_bullets(self):
        """Crea los disparos del robot."""
        if not self.alive:
            return []

        bullets = []
        self.shoot_cooldown -= 1

        if self.shoot_cooldown > 0:
            return []

        self.shoot_cooldown = 20
        self.pattern_timer += 1

        if self.pattern_timer > 80:
            self.attack_pattern = (self.attack_pattern + 1) % 3
            self.pattern_timer = 0

        # Patrón 0: Rayos alternados
        if self.attack_pattern == 0:
            if self.cannon_left_charge >= self.cannon_max_charge:
                bullets.append(Bullet(self.x - 40, self.y - 20, 15, "LEFT"))
                bullets.append(Bullet(self.x - 40, self.y - 20, 15, "LEFT"))
                self.cannon_left_charge = 0
                self._create_sparks(6)
            if self.cannon_right_charge >= self.cannon_max_charge:
                bullets.append(Bullet(self.x - 40, self.y + 20, 15, "LEFT"))
                bullets.append(Bullet(self.x - 40, self.y + 20, 15, "LEFT"))
                self.cannon_right_charge = 0
                self._create_sparks(6)

        # Patrón 1: Misiles diagonales
        elif self.attack_pattern == 1:
            if self.cannon_left_charge >= self.cannon_max_charge:
                for offset in [-1, 0, 1]:
                    bullets.append(
                        Bullet(self.x - 35, self.y - 15 + offset * 5, 13, "DIAG_LEFT")
                    )
                self.cannon_left_charge = 0

        # Patrón 2: Ráfaga
        else:
            for i in range(-2, 3):
                bullets.append(Bullet(self.x - 30, self.y + i * 8, 12, "LEFT"))
            self._create_sparks(10)

        return bullets

    def draw(self, screen):
        """Dibuja el robot completo."""
        if not self.alive:
            return

        x, y = int(self.x), int(self.y)

        # Cuerpo principal
        pygame.draw.rect(screen, self.armor_color, (x - 40, y - 50, 80, 100))
        pygame.draw.rect(screen, (100, 120, 150), (x - 40, y - 50, 80, 100), 3)

        # Cabeza
        pygame.draw.circle(screen, (70, 70, 90), (x, y - 60), 25)
        pygame.draw.circle(screen, (100, 120, 150), (x, y - 60), 25, 2)

        # Visor holográfico
        pygame.draw.circle(screen, (0, 255, 150), (x, y - 60), 12)
        pygame.draw.circle(screen, (100, 255, 200), (x, y - 60), 12, 1)

        # LEDs rojos (ojos)
        pygame.draw.circle(
            screen, (self.red_led_brightness, 50, 50), (x - 8, y - 65), 5
        )
        pygame.draw.circle(
            screen, (self.red_led_brightness, 50, 50), (x + 8, y - 65), 5
        )

        # LED azul central
        pygame.draw.circle(screen, (50, 100, self.blue_led_brightness), (x, y - 55), 4)

        # Cañones
        pygame.draw.rect(screen, (80, 60, 60), (x - 45, y - 15, 25, 10))
        pygame.draw.rect(screen, (80, 60, 60), (x - 45, y + 5, 25, 10))

        # Carga de cañones
        left_charge = int(20 * (self.cannon_left_charge / self.cannon_max_charge))
        right_charge = int(20 * (self.cannon_right_charge / self.cannon_max_charge))
        pygame.draw.rect(
            screen,
            (255, 100 * (1 - self.cannon_left_charge / self.cannon_max_charge), 0),
            (x - 40, y - 12, left_charge, 8),
        )
        pygame.draw.rect(
            screen,
            (255, 100 * (1 - self.cannon_right_charge / self.cannon_max_charge), 0),
            (x - 40, y + 8, right_charge, 8),
        )

        # Brazos mecánicos
        arm_length = 50
        left_arm_x = (
            x - 30 + int(arm_length * self.arm_left_extension * math.cos(math.pi))
        )
        left_arm_y = y - 30 - arm_length // 2
        right_arm_x = (
            x - 30 + int(arm_length * self.arm_right_extension * math.cos(math.pi))
        )
        right_arm_y = y + 30 + arm_length // 2

        pygame.draw.line(
            screen, (100, 80, 80), (x - 30, y - 30), (left_arm_x, left_arm_y), 8
        )
        pygame.draw.line(
            screen, (100, 80, 80), (x - 30, y + 30), (right_arm_x, right_arm_y), 8
        )

        # Daño visible
        damage_ratio = 1 - (self.hp / self.max_hp)
        if damage_ratio > 0.3:
            for _ in range(int(damage_ratio * 5)):
                dx = x + random.randint(-40, 40)
                dy = y + random.randint(-50, 50)
                pygame.draw.circle(
                    screen, (120, 60, 60), (dx, dy), random.randint(3, 6)
                )

        # Partículas
        for spark in self.spark_particles:
            pygame.draw.circle(
                screen, spark["color"], (int(spark["x"]), int(spark["y"])), 1
            )

    def get_hit_rect(self):
        """Retorna el hitbox del robot."""
        return pygame.Rect(
            self.x - 40,
            self.y - 50,
            80,
            100,
        )

    @property
    def frame_count(self):
        """Compatibilidad con animaciones."""
        return int(pygame.time.get_ticks() / 30)
