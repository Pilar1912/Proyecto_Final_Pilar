import math
import random

import pygame
from config import HEIGHT, WIDTH


class Background:
    """Sistema planetario cinematográfico con Sol, planetas, nebulosas y estrellas."""

    def __init__(self, level=1):
        self.level = level
        self.frame_count = 0
        self.stars = []
        self.planets = []
        self.nebula_clouds = []
        self.sun = None
        self.asteroids = []
        self._generate(level)

    def _generate(self, level):
        """Genera el sistema planetario según el nivel."""
        self.level = level
        self.frame_count = 0

        # Generar estrellas de fondo
        self._generate_stars()

        # Generar nebulosas según el nivel
        self._generate_nebulosas(level)

        # Generar Sol en el centro derecha
        self._generate_sun()

        # Generar planetas orbitando el Sol
        self._generate_planets(level)

        # Generar asteroides para efecto cinético
        self._generate_asteroids()

    def _generate_stars(self):
        """Crea un campo de estrellas realistas."""
        self.stars = []
        for _ in range(200):
            self.stars.append(
                {
                    "x": random.randint(0, WIDTH),
                    "y": random.randint(0, HEIGHT),
                    "size": random.choice([1, 1, 1, 2]),
                    "brightness": random.randint(100, 255),
                    "twinkle_speed": random.uniform(0.02, 0.1),
                    "twinkle_offset": random.uniform(0, 2 * math.pi),
                }
            )

    def _generate_nebulosas(self, level):
        """Crea nebulosas de colores según el nivel."""
        self.nebula_clouds = []

        # Colores según nivel
        nebula_colors = [
            # Nivel 1: Azul profundo
            [(20, 50, 150), (50, 100, 200), (30, 80, 180)],
            # Nivel 2: Cian/Turquesa
            [(30, 120, 150), (60, 180, 200), (40, 150, 180)],
            # Nivel 3: Púrpura/Magenta
            [(100, 50, 150), (150, 80, 200), (120, 60, 180)],
            # Nivel 4: Naranja/Rojo
            [(180, 80, 30), (220, 100, 40), (200, 90, 35)],
        ]

        colors = nebula_colors[min(level - 1, 3)]

        # Crear múltiples nubes de nebulosa
        for i in range(5):
            self.nebula_clouds.append(
                {
                    "x": random.randint(200, WIDTH - 200),
                    "y": random.randint(100, HEIGHT - 100),
                    "radius": random.randint(150, 300),
                    "color": random.choice(colors),
                    "opacity": random.randint(20, 50),
                    "drift_x": random.uniform(-0.2, 0.2),
                    "drift_y": random.uniform(-0.2, 0.2),
                }
            )

    def _generate_sun(self):
        """Crea el Sol brillante."""
        self.sun = {
            "x": int(WIDTH * 0.75),
            "y": int(HEIGHT * 0.3),
            "radius": 80,
            "core_color": (255, 200, 0),
            "glow_color": (255, 150, 0),
            "heat_wave_frame": 0,
        }

    def _generate_planets(self, level):
        """Crea planetas orbitando el Sol."""
        self.planets = []

        planet_configs = [
            # (distancia, tamaño, color, velocidad_orbital, offset_inicial)
            (150, 20, (100, 50, 200), 0.008, 0),  # Púrpura
            (220, 35, (200, 100, 50), 0.005, 2),  # Naranja
            (300, 25, (50, 150, 200), 0.003, 4),  # Cian
            (380, 45, (150, 100, 50), 0.002, 1),  # Marrón
        ]

        for dist, size, color, speed, offset in planet_configs:
            self.planets.append(
                {
                    "distance": dist,
                    "size": size,
                    "color": color,
                    "orbit_speed": speed,
                    "angle": offset,
                    "rotation": 0,
                    "has_rings": size > 30,
                    "ring_color": (200, 180, 100),
                }
            )

    def _generate_asteroids(self):
        """Crea asteroides flotantes."""
        self.asteroids = []
        for _ in range(30):
            self.asteroids.append(
                {
                    "x": random.randint(0, WIDTH),
                    "y": random.randint(0, HEIGHT),
                    "speed": random.uniform(0.3, 1.5),
                    "size": random.randint(3, 12),
                    "rotation": random.uniform(0, 2 * math.pi),
                    "rotation_speed": random.uniform(-0.05, 0.05),
                    "color": random.choice(
                        [(120, 120, 120), (100, 100, 100), (140, 140, 140)]
                    ),
                }
            )

    def update(self, level=None):
        """Actualiza el estado del background."""
        if level is not None and level != self.level:
            self._generate(level)

        # Actualizar plantas (órbita)
        for planet in self.planets:
            planet["angle"] += planet["orbit_speed"]
            planet["rotation"] += 0.01

        # Actualizar asteroides
        for asteroid in self.asteroids:
            asteroid["x"] -= asteroid["speed"]
            asteroid["rotation"] += asteroid["rotation_speed"]
            if asteroid["x"] < -20:
                asteroid["x"] = WIDTH + 20
                asteroid["y"] = random.randint(0, HEIGHT)

        # Actualizar nebulosas
        for nebula in self.nebula_clouds:
            nebula["x"] += nebula["drift_x"]
            nebula["y"] += nebula["drift_y"]

        self.frame_count += 1

    def _draw_star(self, screen, star):
        """Dibuja una estrella con efecto twinkle."""
        x = int(star["x"])
        y = int(star["y"])
        base_brightness = star["brightness"]
        size = star["size"]

        # Efecto twinkle
        t = self.frame_count * star["twinkle_speed"] + star["twinkle_offset"]
        brightness = int(base_brightness * (0.6 + 0.4 * math.sin(t)))
        color = (brightness, brightness, brightness)

        if size <= 1:
            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                screen.set_at((x, y), color)
        else:
            pygame.draw.circle(screen, color, (x, y), size)

    def _draw_sun(self, screen):
        """Dibuja el Sol con efectos de brillo."""
        if not self.sun:
            return

        sun = self.sun
        x, y = int(sun["x"]), int(sun["y"])
        radius = sun["radius"]

        # Glow externo (pulsante)
        glow_radius = radius + int(20 * math.sin(self.frame_count * 0.05))
        glow_surface = pygame.Surface(
            (glow_radius * 2, glow_radius * 2), pygame.SRCALPHA
        )
        for i in range(glow_radius, 0, -1):
            alpha = int(100 * (1 - i / glow_radius) ** 2)
            pygame.draw.circle(
                glow_surface, (255, 150, 0, alpha), (glow_radius, glow_radius), i
            )
        screen.blit(glow_surface, (x - glow_radius, y - glow_radius))

        # Núcleo del Sol
        pygame.draw.circle(screen, sun["core_color"], (x, y), radius)
        pygame.draw.circle(screen, (255, 255, 100), (x, y), int(radius * 0.7))

        # Destellos
        for _ in range(3):
            angle = (self.frame_count * 0.02) + (_ * 2 * math.pi / 3)
            flare_x = int(x + math.cos(angle) * radius * 1.3)
            flare_y = int(y + math.sin(angle) * radius * 1.3)
            pygame.draw.circle(screen, (255, 200, 100), (flare_x, flare_y), 10)

    def _draw_planets(self, screen):
        """Dibuja los planetas orbitando el Sol."""
        if not self.sun:
            return

        sun_x, sun_y = self.sun["x"], self.sun["y"]

        for planet in self.planets:
            # Calcular posición orbital
            x = int(sun_x + math.cos(planet["angle"]) * planet["distance"])
            y = int(sun_y + math.sin(planet["angle"]) * planet["distance"])

            # Dibujar órbita (línea fina)
            if planet == self.planets[0]:  # Solo dibujar una vez
                pygame.draw.circle(
                    screen, (100, 100, 100), (sun_x, sun_y), planet["distance"], 1
                )

            # Dibujar planeta
            pygame.draw.circle(screen, planet["color"], (x, y), planet["size"])

            # Anillos si tiene
            if planet["has_rings"]:
                ring_radius = int(planet["size"] * 1.8)
                pygame.draw.ellipse(
                    screen,
                    planet["ring_color"],
                    (
                        x - ring_radius,
                        y - ring_radius // 3,
                        ring_radius * 2,
                        ring_radius // 1.5,
                    ),
                    2,
                )

            # Pequeño brillo
            pygame.draw.circle(
                screen,
                (255, 255, 255),
                (x - planet["size"] // 3, y - planet["size"] // 3),
                3,
            )

    def _draw_nebulosas(self, screen):
        """Dibuja las nebulosas con gradientes."""
        for nebula in self.nebula_clouds:
            x, y = int(nebula["x"]), int(nebula["y"])
            radius = nebula["radius"]
            color = nebula["color"]
            opacity = nebula["opacity"]

            # Crear superficie con alpha
            surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

            # Gradiente de opacidad
            for i in range(radius, 0, -2):
                alpha = int(opacity * (1 - i / radius) ** 2)
                pygame.draw.circle(
                    surf, (color[0], color[1], color[2], alpha), (radius, radius), i
                )

            if 0 <= x - radius < WIDTH and 0 <= y - radius < HEIGHT:
                screen.blit(surf, (x - radius, y - radius))

    def _draw_asteroids(self, screen):
        """Dibuja asteroides."""
        for asteroid in self.asteroids:
            x = int(asteroid["x"])
            y = int(asteroid["y"])
            size = asteroid["size"]
            color = asteroid["color"]

            if 0 <= x < WIDTH and 0 <= y < HEIGHT:
                pygame.draw.circle(screen, color, (x, y), size)
                # Pequeño brillo
                pygame.draw.circle(
                    screen, (200, 200, 200), (x - size // 3, y - size // 3), 1
                )

    def draw(self, screen):
        """Dibuja todo el background en orden de profundidad."""
        # 1. Fondo negro
        screen.fill((5, 5, 15))

        # 2. Nebulosas (muy atrás)
        self._draw_nebulosas(screen)

        # 3. Estrellas lejanas
        for star in self.stars:
            if star["size"] <= 1:
                self._draw_star(screen, star)

        # 4. Sistema solar (Sol y planetas)
        self._draw_sun(screen)
        self._draw_planets(screen)

        # 5. Asteroides
        self._draw_asteroids(screen)

        # 6. Estrellas cercanas
        for star in self.stars:
            if star["size"] > 1:
                self._draw_star(screen, star)
