import math

import pygame


class Player:
    def __init__(self, x, y, size, speed, life):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.life = life
        # Diccionario de power-ups activos {tipo: {"count": n, "time": frames}}
        self.powerups = {}
        self.shield_active = False
        self.shield_time = 0  # Tiempo en frames (450 = 15 segundos a 30 FPS)

    def add_powerup(self, powerup_type):
        """Agregar un power-up (hasta 5 para WEAPON_RIGHT, 3 para otros frontales, 1 para otros)
        Duración: 30 segundos (900 frames a 30 FPS)"""
        # WEAPON_RIGHT puede acumular hasta 5 (dispara en patrón: 1, 2, 3, 4, 5 balas)
        # WEAPON_LEFT hasta 3
        if powerup_type == "WEAPON_RIGHT":
            max_count = 5
        elif powerup_type == "WEAPON_LEFT":
            max_count = 3
        else:
            max_count = 1

        powerup_duration = 900  # 30 segundos a 30 FPS

        if powerup_type not in self.powerups:
            self.powerups[powerup_type] = {"count": 0, "time": 0}

        if self.powerups[powerup_type]["count"] < max_count:
            self.powerups[powerup_type]["count"] += 1
            self.powerups[powerup_type]["time"] = powerup_duration

    def remove_powerup(self, powerup_type):
        """Remover un power-up"""
        if powerup_type in self.powerups and self.powerups[powerup_type]["count"] > 0:
            self.powerups[powerup_type]["count"] -= 1
            if self.powerups[powerup_type]["count"] == 0:
                del self.powerups[powerup_type]

    def has_powerup(self, powerup_type):
        """Verificar si tiene un power-up específico"""
        return (
            powerup_type in self.powerups and self.powerups[powerup_type]["count"] > 0
        )

    def get_powerups_list(self):
        """Obtener lista de power-ups activos con contadores"""
        result = []
        for ptype, data in self.powerups.items():
            if data["count"] > 0:
                result.append(f"{ptype}x{data['count']}")
        return result

    def update_powerups(self):
        """Actualiza la duración de los power-ups y los elimina si expiran"""
        powerups_to_remove = []
        for ptype, data in self.powerups.items():
            if data["time"] > 0:
                data["time"] -= 1
            if data["time"] <= 0:
                powerups_to_remove.append(ptype)

        for ptype in powerups_to_remove:
            if ptype in self.powerups:
                del self.powerups[ptype]

    def activate_shield(self):
        """Activa el escudo por 15 segundos (450 frames a 30 FPS)"""
        self.shield_active = True
        self.shield_time = 450  # 15 segundos

    def update_shield(self):
        """Actualiza el estado del escudo cada frame"""
        if self.shield_active and self.shield_time > 0:
            self.shield_time -= 1
        elif self.shield_time <= 0:
            self.shield_active = False

    def move(self, direction):
        if direction == "LEFT":
            self.x -= self.speed
        elif direction == "RIGHT":
            self.x += self.speed
        elif direction == "UP":
            self.y -= self.speed
        elif direction == "DOWN":
            self.y += self.speed

    # def draw(self, screen):
    # pygame.draw.circle(screen, BLUE, (self.x, self.y), self.size)

    def draw(self, screen):
        x, y = self.x, self.y
        s = self.size

        # Sombra más suave (con alpha blending)
        sombra_offset = 4
        shadow_surface = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.polygon(
            shadow_surface,
            (0, 0, 30, 100),
            [
                (x + s + sombra_offset - (s * 2), y + sombra_offset - (s * 2)),
                (x - s + sombra_offset - (s * 2), y - s + sombra_offset - (s * 2)),
                (x - s + sombra_offset - (s * 2), y + s + sombra_offset - (s * 2)),
            ],
        )
        screen.blit(shadow_surface, (0, 0))

        # Cuerpo principal con gradiente real
        for i in range(5):  # Múltiples capas para gradiente
            factor = i / 5
            color = (
                30 + int(50 * factor),
                30 + int(50 * factor),
                100 + int(100 * factor),
            )
            offset = i * 1.5
            pygame.draw.polygon(
                screen,
                color,
                [
                    (x + s - offset, y),
                    (x - s + offset, y - s + offset),
                    (x - s + offset, y + s - offset),
                ],
            )

        # Detalles estructurales (paneles)
        pygame.draw.line(screen, (150, 150, 220), (x - s + 5, y), (x + s - 5, y), 1)
        pygame.draw.line(screen, (150, 150, 220), (x - s // 2, y - s // 2), (x, y), 1)
        pygame.draw.line(screen, (150, 150, 220), (x - s // 2, y + s // 2), (x, y), 1)

        # Cabina con efecto vidrio realista
        # Vidrio base
        pygame.draw.circle(screen, (80, 130, 200), (x, y), s // 2)
        # Reflejo principal
        pygame.draw.circle(screen, (180, 220, 255), (x - 3, y - 3), s // 3)
        # Reflejo secundario
        pygame.draw.circle(screen, (200, 240, 255), (x - 1, y - 4), s // 4)
        # Brillo especular
        pygame.draw.circle(screen, (255, 255, 255), (x - 4, y - 5), s // 6)
        # Marco de la cabina
        pygame.draw.circle(screen, (100, 100, 150), (x, y), s // 2, 1)

        # Alas mejoradas con efecto 3D
        # Ala superior
        ala_sup = [
            (x - s // 2, y - s // 2),
            (x - s - 5, y - s - 3),
            (x - s // 2, y - s // 3),
        ]
        pygame.draw.polygon(screen, (40, 40, 120), ala_sup)
        pygame.draw.polygon(screen, (70, 70, 180), ala_sup, 1)

        # Ala inferior
        ala_inf = [
            (x - s // 2, y + s // 2),
            (x - s - 5, y + s + 3),
            (x - s // 2, y + s // 3),
        ]
        pygame.draw.polygon(screen, (40, 40, 120), ala_inf)
        pygame.draw.polygon(screen, (70, 70, 180), ala_inf, 1)

        # Detalles de las alas (ranuras)
        pygame.draw.line(
            screen,
            (20, 20, 80),
            (x - s // 1.5, y - s // 2.5),
            (x - s - 3, y - s - 1),
            1,
        )
        pygame.draw.line(
            screen,
            (20, 20, 80),
            (x - s // 1.5, y + s // 2.5),
            (x - s - 3, y + s + 1),
            1,
        )

        # Motor con efecto metálico
        pygame.draw.rect(screen, (80, 80, 120), (x - s - 6, y - 5, 10, 10))
        pygame.draw.rect(screen, (120, 120, 180), (x - s - 6, y - 5, 10, 10), 1)
        # Detalle del motor
        pygame.draw.circle(screen, (60, 60, 100), (x - s - 3, y), 3)

        # Llama del motor con animación más realista
        import random

        flame_length = random.randint(8, 15)
        flame_offset = random.randint(-2, 2)

        # Capa exterior (naranja)
        pygame.draw.polygon(
            screen,
            (255, 100, 0),
            [
                (x - s - 5, y + flame_offset),
                (x - s - 5 - flame_length, y + flame_offset // 2),
                (x - s - 5, y - 1 + flame_offset),
            ],
        )

        # Capa interior (amarilla)
        pygame.draw.polygon(
            screen,
            (255, 200, 50),
            [
                (x - s - 5, y + flame_offset // 2),
                (x - s - 5 - flame_length // 1.5, y + flame_offset // 3),
                (x - s - 5, y - 0.5 + flame_offset // 2),
            ],
        )

        # Núcleo (blanco)
        pygame.draw.polygon(
            screen,
            (255, 255, 200),
            [
                (x - s - 5, y + flame_offset // 3),
                (x - s - 5 - flame_length // 3, y + flame_offset // 4),
                (x - s - 5, y + flame_offset // 3),
            ],
        )

        # Efecto de glow de la llama
        glow = pygame.Surface((20, 15), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 150, 0, 80), (10, 7), 10)
        screen.blit(glow, (x - s - 15, y - 8))

        # Luces de navegación con efecto pulsante
        time = pygame.time.get_ticks() / 1000
        pulse = abs(math.sin(time * 3))  # Pulsación sinusoidal

        # Luz roja (estribor)
        red_intensity = int(150 + 105 * pulse)
        pygame.draw.circle(screen, (red_intensity, 0, 0), (x - s + 3, y - s + 3), 3)
        # Efecto glow rojo
        red_glow = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(red_glow, (red_intensity, 0, 0, 100), (4, 4), 4)
        screen.blit(red_glow, (x - s, y - s))

        # Luz verde (babor)
        green_intensity = int(150 + 105 * pulse)
        pygame.draw.circle(screen, (0, green_intensity, 0), (x - s + 3, y + s - 3), 3)
        # Efecto glow verde
        green_glow = pygame.Surface((8, 8), pygame.SRCALPHA)
        pygame.draw.circle(green_glow, (0, green_intensity, 0, 100), (4, 4), 4)
        screen.blit(green_glow, (x - s, y + s - 6))

        # Faro intermitente superior
        beacon = int(200 + 55 * abs(math.sin(time * 5)))
        pygame.draw.circle(screen, (beacon, beacon, 100), (x, y - s // 1.5), 2)

        # Detalles de superficie (remaches/líneas)
        for offset in [-3, 0, 3]:
            pygame.draw.circle(
                screen, (60, 60, 100), (x - s // 2 + offset, y - s // 3), 1
            )
            pygame.draw.circle(
                screen, (60, 60, 100), (x - s // 2 + offset, y + s // 3), 1
            )

        # Efecto de brillo en los bordes
        border_glow = pygame.Surface((s * 2, s * 2), pygame.SRCALPHA)
        pygame.draw.polygon(
            border_glow,
            (100, 100, 255, 50),
            [(x + s, y), (x - s, y - s), (x - s, y + s)],
            2,
        )
        screen.blit(border_glow, (0, 0))

        # Escudo protector
        if self.shield_active:
            # Círculo protector con parpadeo
            pulse = abs(math.sin(pygame.time.get_ticks() / 500))
            shield_alpha = int(100 + 50 * pulse)
            shield_size = int(s * 2 + 10)
            shield_surface = pygame.Surface(
                (shield_size * 2, shield_size * 2), pygame.SRCALPHA
            )
            pygame.draw.circle(
                shield_surface,
                (255, 165, 0, shield_alpha),
                (shield_size, shield_size),
                shield_size,
            )
            pygame.draw.circle(
                shield_surface,
                (255, 200, 100, 200),
                (shield_size, shield_size),
                shield_size,
                2,
            )
            screen.blit(shield_surface, (x - shield_size, y - shield_size))
