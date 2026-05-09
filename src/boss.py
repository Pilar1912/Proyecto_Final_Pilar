import math
import random

import pygame
from bullet import Bullet
from config import BOSS_HP, HEIGHT, WHITE, WIDTH
from projectile import Projectile


class Boss:
    """Clase base para todos los jefes finales.

    Subclases deben implementar:
        - draw(screen): renderizado visual del boss
        - _create_bullets(): patron de disparo especifico
    Opcionalmente pueden sobreescribir:
        - get_hit_rect(): hitbox personalizado
        - move(): comportamiento de movimiento extra
    """

    def __init__(self, level, name="BOSS", size=80):
        self.name = name
        self.size = size
        self.x = WIDTH - self.size - 40
        self.y = HEIGHT // 2
        self.base_x = self.x
        self.hp = BOSS_HP + (level - 1) * 50
        self.max_hp = self.hp
        self.speed_y = 2
        self.direction_y = 1  # 1 = abajo, -1 = arriba
        self.alive = True
        self.level = level
        self._animation_frame = 0  # Contador de frames para animaciones

        # IA de carga (embestida hacia la izquierda)
        self.charging = False
        self.charge_speed = 6
        self.charge_target_x = WIDTH // 2
        self.charge_cooldown = 0
        self.charge_cooldown_max = 150
        self.returning = False

        # Disparo
        self.shoot_cooldown = 0
        self.shoot_rate = 20

        # NUEVAS MECÁNICAS: Disparos automáticos hacia el jugador
        self.auto_shoot_timer = 0  # Temporizador para disparos automáticos
        self.auto_shoot_interval = random.randint(
            30, 90
        )  # 1-3 segundos (30-90 frames a 30 FPS)
        self.projectile_timer = 0  # Temporizador para bombitas explosivas
        self.projectile_interval = 150  # Cada 5 segundos (150 frames a 30 FPS)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def move(self):
        if not self.alive:
            return

        self._animation_frame += 1

        # Actualizar contadores de disparos automáticos
        self.auto_shoot_timer += 1
        self.projectile_timer += 1

        if not self.charging and not self.returning:
            self.y += self.speed_y * self.direction_y
            if self.y <= self.size:
                self.direction_y = 1
            elif self.y >= HEIGHT - self.size:
                self.direction_y = -1

            self.charge_cooldown -= 1
            if self.charge_cooldown <= 0 and random.randint(0, 100) < 2:
                self.charging = True

        elif self.charging:
            self.x -= self.charge_speed
            if self.x <= self.charge_target_x:
                self.charging = False
                self.returning = True

        elif self.returning:
            self.x += self.charge_speed
            if self.x >= self.base_x:
                self.x = self.base_x
                self.returning = False
                self.charge_cooldown = self.charge_cooldown_max

    def shoot(self, player_x=None, player_y=None):
        """
        Dispara balas segun el patron del boss y disparos automáticos hacia el jugador.

        Args:
            player_x: Posición X del jugador (para disparos automáticos)
            player_y: Posición Y del jugador (para disparos automáticos)

        Returns:
            Lista con balas normales y proyectiles especiales
        """
        if not self.alive:
            return [], []

        all_bullets = []
        all_projectiles = []

        # Disparos del patrón específico del jefe
        self.shoot_cooldown -= 1
        if self.shoot_cooldown <= 0:
            self.shoot_cooldown = self.shoot_rate
            all_bullets.extend(self._create_bullets())

        # NUEVOS DISPAROS AUTOMÁTICOS HACIA EL JUGADOR
        if player_x is not None and player_y is not None:
            # Disparos automáticos cada 1-3 segundos
            if self.auto_shoot_timer >= self.auto_shoot_interval:
                self.auto_shoot_timer = 0
                self.auto_shoot_interval = random.randint(
                    30, 90
                )  # Siguiente intervalo aleatorio
                # Dispara 2-3 balas hacia el jugador
                all_bullets.extend(
                    self._shoot_at_player(
                        player_x, player_y, num_bullets=random.randint(2, 3)
                    )
                )

            # Bombitas explosivas cada 5 segundos
            if self.projectile_timer >= self.projectile_interval:
                self.projectile_timer = 0
                all_projectiles.append(self._shoot_explosive_bomb(player_x, player_y))

        return all_bullets, all_projectiles

    def _shoot_at_player(self, player_x, player_y, num_bullets=2):
        """Crea disparos normales dirigidos hacia el jugador."""
        bullets = []

        # Calcular ángulo hacia el jugador
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return bullets

        # Normalizar dirección
        dir_x = dx / distance
        dir_y = dy / distance

        # Crear múltiples disparos con pequeños ángulos de separación
        for i in range(num_bullets):
            # Ángulo adicional para dispersión (arcade effect)
            angle_offset = (i - (num_bullets - 1) / 2) * 0.3
            angle = math.atan2(dy, dx) + angle_offset

            # Convertir ángulo a dirección
            new_dir_x = math.cos(angle)
            new_dir_y = math.sin(angle)

            # Crear bala personalizada con dirección
            bullet = Bullet(
                self.x - self.size // 2,
                self.y + (i - (num_bullets - 1) / 2) * 15,
                14,
                "BOSS_CUSTOM",
                custom_vx=new_dir_x * 14,
                custom_vy=new_dir_y * 14,
            )
            bullets.append(bullet)

        return bullets

    def _shoot_explosive_bomb(self, player_x, player_y):
        """Crea una bombita explosiva dirigida hacia el jugador."""
        bomb = Projectile(self.x - self.size // 2, self.y, player_x, player_y, speed=6)
        return bomb

    def _create_bullets(self):
        """Sobreescribir en subclases para definir patron de disparo."""
        return [
            Bullet(self.x - self.size // 2, self.y, 12, "LEFT"),
        ]

    def draw(self, screen):
        """Sobreescribir en subclases para el renderizado."""
        pass

    def get_hit_rect(self):
        """Retorna el hitbox como pygame.Rect. Sobreescribir si es necesario."""
        return pygame.Rect(
            self.x - self.size // 2,
            self.y - self.size // 2,
            self.size,
            self.size,
        )

    def draw_health_bar(self, screen):
        """Dibuja la barra de vida del jefe en la parte superior de la pantalla."""
        if not self.alive:
            return

        bar_width = 400
        bar_height = 20
        bar_x = WIDTH // 2 - bar_width // 2
        bar_y = 10

        # Fondo de la barra (gris oscuro)
        pygame.draw.rect(screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))

        # Barra de vida (rojo -> amarillo -> verde segun HP)
        hp_ratio = self.hp / self.max_hp
        fill_width = int(bar_width * hp_ratio)
        if hp_ratio > 0.5:
            bar_color = (int(255 * (1 - hp_ratio) * 2), 255, 0)
        else:
            bar_color = (255, int(255 * hp_ratio * 2), 0)
        pygame.draw.rect(screen, bar_color, (bar_x, bar_y, fill_width, bar_height))

        # Borde de la barra
        pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)

        # Texto del jefe
        font = pygame.font.SysFont("monospace", 14, bold=True)
        label = font.render(f"{self.name}  {self.hp}/{self.max_hp}", 1, WHITE)
        label_rect = label.get_rect(center=(WIDTH // 2, bar_y + bar_height // 2))
        screen.blit(label, label_rect)
