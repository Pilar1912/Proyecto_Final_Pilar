"""import random
import math
import sys
import os

import pygame

# Permitir importar agujeronegro.py desde la raíz del proyecto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from agujeronegro import BlackHole
from config import HEIGHT, WIDTH


class Background:
    #Campo de estrellas parallax con colores sutiles y efecto de brillo.

    # Paletas de color por nivel (colores sutiles para estrellas especiales)
    LEVEL_ACCENTS = [
        # Nivel 1: azules fríos
        [(100, 140, 255), (80, 120, 200), (150, 180, 255)],
        # Nivel 2: cyans
        [(80, 220, 220), (100, 255, 200), (60, 180, 180)],
        # Nivel 3: verdes/amarillos
        [(120, 255, 80), (200, 255, 100), (180, 220, 60)],
        # Nivel 4: naranjas/rojos
        [(255, 160, 60), (255, 100, 60), (255, 200, 80)],
        # Nivel 5+: magentas/rojos intensos
        [(255, 80, 120), (200, 60, 255), (255, 60, 80)],
    ]

    def __init__(self, level=1):
        self.level = level
        self.frame_count = 0
        self.stars = []
        self.nebula_particles = []
        self.background_planets = []
        self.black_hole = None
        self._generate(level)

    def _generate(self, level):
       #Genera el campo de estrellas según el nivel.
        self.level = level
        self.stars = []
        self.nebula_particles = []

        accents = self.LEVEL_ACCENTS[min(level - 1, 4)]

        # 3 capas de parallax con diferentes velocidades
        # Capa 1: estrellas lejanas (lentas, pequeñas, tenues)
        for _ in range(120):
            self.stars.append(self._make_star(
                speed_range=(0.3, 0.8),
                size_range=(1, 1),
                brightness_range=(60, 120),
                accents=accents,
                color_chance=0.05,
                twinkle_chance=0.02,
            ))

        # Capa 2: estrellas medias
        for _ in range(80 + level * 10):
            self.stars.append(self._make_star(
                speed_range=(1.0, 2.0),
                size_range=(1, 2),
                brightness_range=(100, 180),
                accents=accents,
                color_chance=0.12,
                twinkle_chance=0.08,
            ))

        # Capa 3: estrellas cercanas (rápidas, grandes, brillantes)
        for _ in range(30 + level * 5):
            self.stars.append(self._make_star(
                speed_range=(2.5, 4.0 + level * 0.3),
                size_range=(2, 3),
                brightness_range=(160, 255),
                accents=accents,
                color_chance=0.2,
                twinkle_chance=0.15,
            ))

        # Nebulosas más visibles según el nivel
        # Nivel 1-2: nebulosa sutil; Nivel 3+: nebulosas prominentes
        accent = random.choice(accents)
        nebula_count = 20 + level * 10  # Aumenta con nivel
        for _ in range(nebula_count):
            self.nebula_particles.append({
                "x": random.randint(0, WIDTH),
                "y": random.randint(0, HEIGHT),
                "speed": random.uniform(0.15, 0.5),
                "size": random.randint(30, 80 + level * 10),  # Nebulosas más grandes en niveles altos
                "color": accent,
                "alpha": random.randint(15, 40),  # Más opacas
            })
        
        # Planetas de fondo decorativos (crean profundidad)
        self.background_planets = []
        if level >= 2:
            for _ in range(2 + level):
                self.background_planets.append({
                    "x": random.randint(int(WIDTH * 0.6), WIDTH),
                    "y": random.randint(0, HEIGHT),
                    "radius": random.randint(20, 50 + level * 5),
                    "color": random.choice(accents),
                    "alpha": random.randint(30, 80),
                })

        # Agujero negro de fondo (posición estratégica según nivel)
        # Aparece desde nivel 2, se hace más grande en niveles altos
        if level >= 2:
            bh_radius = 35 + level * 8  # crece con el nivel
            # Posición: zona derecha-superior, lejos del jugador (que está a la izquierda)
            bh_x = int(WIDTH * 0.72)
            bh_y = int(HEIGHT * 0.35)
            self.black_hole = BlackHole(bh_x, bh_y, radius=bh_radius)
        else:
            self.black_hole = None

    def _make_star(self, speed_range, size_range, brightness_range,
                   accents, color_chance, twinkle_chance):
        b = random.randint(*brightness_range)

        # Decidir color
        r = random.random()
        if r < color_chance * 0.4:
            # Roja sutil
            color = (min(255, b + 80), max(0, b - 60), max(0, b - 80))
        elif r < color_chance * 0.7:
            # Naranja/amarilla sutil
            color = (min(255, b + 40), min(255, b + 10), max(0, b - 60))
        elif r < color_chance * 0.9:
            # Azulada sutil
            color = (max(0, b - 40), max(0, b - 20), min(255, b + 60))
        elif r < color_chance:
            # Color del acento del nivel
            accent = random.choice(accents)
            ratio = b / 255
            color = (int(accent[0] * ratio), int(accent[1] * ratio), int(accent[2] * ratio))
        else:
            # Blanca normal
            color = (b, b, b)

        return {
            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),
            "speed": random.uniform(*speed_range),
            "size": random.choice(range(size_range[0], size_range[1] + 1)),
            "color": color,
            "base_color": color,
            "twinkle": random.random() < twinkle_chance,
            "twinkle_speed": random.uniform(0.03, 0.12),
            "twinkle_offset": random.uniform(0, math.pi * 2),
        }

    def update(self, level=None):
        if level is not None and level != self.level:
            self._generate(level)

        for star in self.stars:
            star["x"] -= star["speed"]
            if star["x"] < -5:
                star["x"] = WIDTH + random.randint(0, 20)
                star["y"] = random.randint(0, HEIGHT)

        for p in self.nebula_particles:
            p["x"] -= p["speed"]
            if p["x"] < -p["size"]:
                p["x"] = WIDTH + p["size"]
                p["y"] = random.randint(0, HEIGHT)

        # Actualizar agujero negro
        if self.black_hole:
            self.black_hole.update(1.0)

        self.frame_count += 1

    def _draw_star(self, screen, star):
       #Dibuja una estrella individual con efecto twinkle.
        x = int(star["x"])
        y = int(star["y"])
        color = star["base_color"]
        size = star["size"]

        if star["twinkle"]:
            t = self.frame_count * star["twinkle_speed"] + star["twinkle_offset"]
            glow = (math.sin(t) + 1) / 2
            r = min(255, int(color[0] * (0.4 + glow * 0.6)))
            g = min(255, int(color[1] * (0.4 + glow * 0.6)))
            b = min(255, int(color[2] * (0.4 + glow * 0.6)))
            color = (r, g, b)

            if glow > 0.85 and size >= 2:
                halo_alpha = int(30 * (glow - 0.85) / 0.15)
                halo_surf = pygame.Surface((8, 8), pygame.SRCALPHA)
                pygame.draw.circle(
                    halo_surf,
                    (color[0], color[1], color[2], halo_alpha),
                    (4, 4), 4,
                )
                screen.blit(halo_surf, (x - 4, y - 4))

        if size <= 1:
            screen.set_at((x, y), color)
        else:
            pygame.draw.circle(screen, color, (x, y), size)

    def draw(self, screen):
        # 1. Nebulosa de fondo (lo más lejano)
        for p in self.nebula_particles:
            surf = pygame.Surface((p["size"] * 2, p["size"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (p["color"][0], p["color"][1], p["color"][2], p["alpha"]),
                (p["size"], p["size"]),
                p["size"],
            )
            screen.blit(surf, (int(p["x"]) - p["size"], int(p["y"]) - p["size"]))

        # 2. Estrellas lejanas (capa 1: size == 1, speed < 1)
        for star in self.stars:
            if star["size"] <= 1:
                self._draw_star(screen, star)

        # 3. AGUJERO NEGRO (entre estrellas lejanas y cercanas = profundidad)
        if self.black_hole:
            self.black_hole.draw(screen)

        # 4. Estrellas medias y cercanas (capas 2 y 3: pasan por delante)
        for star in self.stars:
            if star["size"] > 1:
                self._draw_star(screen, star)
                """
import random
import math
import sys
import os
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agujeronegro import BlackHole
from config import HEIGHT, WIDTH


class Background:
    """
    Fondo espacial estilo galaxia:
    - nebulosas púrpura/azul
    - estrellas con profundidad
    - glow galáctico
    - polvo cósmico
    - agujero negro
    """

    def __init__(self, level=1):

        self.level = level
        self.frame_count = 0

        self.stars = []
        self.nebulae = []
        self.planets = []
        self.shooting_stars = []

        self.black_hole = None

        self._generate(level)
        self._make_deep_space_bg()

    # =========================================================
    # FONDO GALÁCTICO
    # =========================================================

    def _make_deep_space_bg(self):

        surf = pygame.Surface((WIDTH, HEIGHT))

        # -----------------------------------------------------
        # GRADIENTE ESPACIAL
        # -----------------------------------------------------

        for y in range(HEIGHT):

            t = y / HEIGHT

            r = int(5 + 20 * (1 - abs(t - 0.5) * 2))
            g = int(5 + 10 * (1 - abs(t - 0.5) * 2))
            b = int(20 + 50 * (1 - abs(t - 0.5) * 2))

            pygame.draw.line(surf, (r, g, b), (0, y), (WIDTH, y))

        # -----------------------------------------------------
        # GLOW GALÁCTICO CENTRAL
        # -----------------------------------------------------

        glow_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        center_x = WIDTH // 2
        center_y = HEIGHT // 3

        for radius in range(350, 0, -8):

            alpha = max(0, int(80 * (1 - radius / 350)))

            color = (
                120,
                80,
                200,
                alpha
            )

            pygame.draw.circle(
                glow_surface,
                color,
                (center_x, center_y),
                radius
            )

        surf.blit(glow_surface, (0, 0))

        # -----------------------------------------------------
        # POLVO CÓSMICO
        # -----------------------------------------------------

        for _ in range(5000):

            x = random.randint(0, WIDTH - 1)
            y = random.randint(0, HEIGHT - 1)

            brightness = random.randint(5, 40)

            choice = random.random()

            # tonos variados tipo galaxia
            if choice < 0.15:
                color = (
                    brightness // 2,
                    brightness // 2,
                    brightness
                )

            elif choice < 0.30:
                color = (
                    brightness,
                    brightness // 2,
                    brightness
                )

            else:
                color = (
                    brightness,
                    brightness,
                    brightness
                )

            surf.set_at((x, y), color)

        # -----------------------------------------------------
        # ESTRELLAS GRANDES CON GLOW
        # -----------------------------------------------------

        for _ in range(50):

            x = random.randint(0, WIDTH)
            y = random.randint(0, HEIGHT)

            radius = random.randint(2, 5)

            glow = pygame.Surface(
                (radius * 8, radius * 8),
                pygame.SRCALPHA
            )

            for r in range(radius * 4, 0, -1):

                alpha = int(25 * (1 - r / (radius * 4)))

                pygame.draw.circle(
                    glow,
                    (255, 255, 255, alpha),
                    (radius * 4, radius * 4),
                    r
                )

            surf.blit(
                glow,
                (x - radius * 4, y - radius * 4)
            )

        self.space_bg = surf

    # =========================================================
    # ESTRELLAS
    # =========================================================

    def _make_star(self, speed, size, brightness):

        rand = random.random()

        if rand < 0.03:
            color = (180, 200, 255)

        elif rand < 0.05:
            color = (255, 240, 180)

        elif rand < 0.08:
            color = (220, 150, 255)

        else:
            color = (
                brightness,
                brightness,
                brightness
            )

        return {

            "x": random.randint(0, WIDTH),
            "y": random.randint(0, HEIGHT),

            "speed": speed,
            "size": size,
            "color": color,

            "twinkle": random.random() < 0.08,

            "twinkle_speed": random.uniform(0.02, 0.08),

            "twinkle_offset": random.uniform(
                0,
                math.pi * 2
            ),
        }

    # =========================================================
    # NEBULOSAS
    # =========================================================

    def _add_nebula(self):

        x = random.randint(-200, WIDTH)
        y = random.randint(-100, HEIGHT)

        width = random.randint(250, 500)
        height = random.randint(120, 250)

        colors = [

            (120, 70, 200, 18),
            (70, 120, 255, 18),
            (255, 120, 180, 14),
            (180, 80, 255, 15),
        ]

        return {

            "x": x,
            "y": y,

            "width": width,
            "height": height,

            "color": random.choice(colors),

            "angle": random.uniform(0, math.pi),

            "speed": random.uniform(0.03, 0.08),
        }

    # =========================================================
    # PLANETAS
    # =========================================================

    def _add_planet(self):

        palette = [

            (120, 100, 80),
            (90, 110, 130),
            (200, 180, 140),
            (180, 140, 100),
            (100, 120, 150),
        ]

        color = random.choice(palette)

        radius = random.randint(25, 55)

        return {

            "x": random.randint(int(WIDTH * 0.7), WIDTH - 40),

            "y": random.randint(40, HEIGHT - 40),

            "radius": radius,

            "color": color,

            "phase_angle": random.uniform(
                0,
                math.pi / 3
            ),
        }

    # =========================================================
    # GENERACIÓN
    # =========================================================

    def _generate(self, level):

        self.stars = []
        self.nebulae = []
        self.planets = []
        self.shooting_stars = []

        # estrellas lejanas
        for _ in range(350):

            self.stars.append(

                self._make_star(
                    speed=0.3,
                    size=1,
                    brightness=random.randint(80, 150)
                )
            )

        # estrellas medias
        for _ in range(180 + level * 5):

            self.stars.append(

                self._make_star(
                    speed=random.uniform(0.8, 1.5),
                    size=random.choice([1, 2]),
                    brightness=random.randint(120, 200)
                )
            )

        # estrellas cercanas
        for _ in range(80 + level * 3):

            self.stars.append(

                self._make_star(
                    speed=random.uniform(2.0, 3.5),
                    size=random.choice([2, 3]),
                    brightness=random.randint(180, 255)
                )
            )

        # nebulosas
        nebula_count = 10 + level

        for _ in range(nebula_count):

            self.nebulae.append(
                self._add_nebula()
            )

        # pocos planetas
        if level >= 4:

            num_planets = 1

            for _ in range(num_planets):

                self.planets.append(
                    self._add_planet()
                )

        # agujero negro
        if level >= 3:

            bh_radius = 30 + level * 3

            bh_x = int(WIDTH * 0.8)
            bh_y = int(HEIGHT * 0.3)

            self.black_hole = BlackHole(
                bh_x,
                bh_y,
                radius=bh_radius
            )

        else:
            self.black_hole = None

    # =========================================================
    # UPDATE
    # =========================================================

    def update(self, level=None):

        if level is not None and level != self.level:

            self._generate(level)
            self.level = level

        # mover estrellas
        for star in self.stars:

            star["x"] -= star["speed"]

            if star["x"] < -10:

                star["x"] = WIDTH + random.randint(0, 30)
                star["y"] = random.randint(0, HEIGHT)

        # mover nebulosas
        for neb in self.nebulae:

            neb["x"] -= neb["speed"]

            if neb["x"] + neb["width"] < 0:

                neb["x"] = WIDTH + random.randint(0, 100)

                neb["y"] = random.randint(
                    0,
                    HEIGHT
                )

        # agujero negro
        if self.black_hole:

            self.black_hole.update(1.0)

        # estrellas fugaces
        if random.random() < 0.002:

            self.shooting_stars.append({

                "x": random.randint(0, WIDTH),

                "y": random.randint(
                    0,
                    HEIGHT // 2
                ),

                "vx": random.uniform(-10, -5),

                "vy": random.uniform(1, 3),

                "life": random.randint(20, 40)
            })

        for s in self.shooting_stars[:]:

            s["x"] += s["vx"]
            s["y"] += s["vy"]

            s["life"] -= 1

            if (
                s["life"] <= 0
                or s["x"] < 0
                or s["y"] > HEIGHT
            ):

                self.shooting_stars.remove(s)

        self.frame_count += 1

    # =========================================================
    # DIBUJAR ESTRELLA
    # =========================================================

    def _draw_star(self, screen, star):

        x = int(star["x"])
        y = int(star["y"])

        color = star["color"]
        size = star["size"]

        if star["twinkle"]:

            t = (
                self.frame_count
                * star["twinkle_speed"]
                + star["twinkle_offset"]
            )

            glow = (math.sin(t) + 1) / 2

            factor = 0.6 + glow * 0.4

            color = tuple(

                min(255, int(c * factor))
                for c in star["color"]
            )

        if size == 1:

            screen.set_at((x, y), color)

        else:

            pygame.draw.circle(
                screen,
                color,
                (x, y),
                size
            )

    # =========================================================
    # DRAW
    # =========================================================

    def draw(self, screen):

        # fondo
        screen.blit(self.space_bg, (0, 0))

        # -----------------------------------------------------
        # NEBULOSAS
        # -----------------------------------------------------

        for neb in self.nebulae:

            neb_surf = pygame.Surface(
                (neb["width"], neb["height"]),
                pygame.SRCALPHA
            )

            cx = neb["width"] // 2
            cy = neb["height"] // 2

            max_r = neb["width"] // 2

            for r in range(max_r, 0, -6):

                alpha = int(
                    neb["color"][3]
                    * (1 - r / max_r)
                )

                color = (

                    neb["color"][0],
                    neb["color"][1],
                    neb["color"][2],
                    alpha
                )

                pygame.draw.ellipse(

                    neb_surf,

                    color,

                    (
                        cx - r,
                        cy - r // 3,
                        r * 2,
                        r
                    )
                )

            rotated = pygame.transform.rotate(
                neb_surf,
                math.degrees(neb["angle"])
            )

            screen.blit(
                rotated,
                (neb["x"], neb["y"])
            )

        # -----------------------------------------------------
        # ESTRELLAS
        # -----------------------------------------------------

        for star in self.stars:

            self._draw_star(screen, star)

        # -----------------------------------------------------
        # PLANETAS
        # -----------------------------------------------------

        for p in self.planets:

            pygame.draw.circle(

                screen,

                p["color"],

                (
                    int(p["x"]),
                    int(p["y"])
                ),

                p["radius"]
            )

            shadow_surf = pygame.Surface(
                (p["radius"] * 2, p["radius"] * 2),
                pygame.SRCALPHA
            )

            shadow_center = (

                p["radius"]
                + int(
                    p["radius"]
                    * 0.3
                    * math.cos(p["phase_angle"])
                ),

                p["radius"]
            )

            pygame.draw.circle(

                shadow_surf,

                (0, 0, 0, 140),

                shadow_center,

                p["radius"]
            )

            screen.blit(

                shadow_surf,

                (
                    int(p["x"]) - p["radius"],
                    int(p["y"]) - p["radius"]
                )
            )

        # -----------------------------------------------------
        # AGUJERO NEGRO
        # -----------------------------------------------------

        if self.black_hole:

            for r in range(
                self.black_hole.radius + 5,
                self.black_hole.radius + 35,
                5
            ):

                alpha = max(
                    0,
                    80 - (
                        r
                        - self.black_hole.radius
                    ) * 3
                )

                ellipse_rect = pygame.Rect(

                    self.black_hole.x - r,

                    self.black_hole.y - int(r * 0.4),

                    r * 2,

                    int(r * 0.8)
                )

                pygame.draw.ellipse(

                    screen,

                    (255, 100, 40, alpha),

                    ellipse_rect,

                    1
                )

            self.black_hole.draw(screen)

        # -----------------------------------------------------
        # ESTRELLAS FUGACES
        # -----------------------------------------------------

        for s in self.shooting_stars:

            start = (
                int(s["x"]),
                int(s["y"])
            )

            end = (
                int(s["x"] - s["vx"] * 2),
                int(s["y"] - s["vy"] * 2)
            )

            pygame.draw.line(

                screen,

                (255, 255, 200),

                start,

                end,

                2
            )

            pygame.draw.circle(

                screen,

                (255, 240, 200),

                start,

                2
            )