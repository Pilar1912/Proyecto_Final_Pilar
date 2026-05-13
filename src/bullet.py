import pygame
from config import BLUE, GREEN, YELLOW


class Bullet:
    def __init__(self, x, y, speed, direction, custom_vx=None, custom_vy=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = 5
        self.height = 10
        self.direction = direction  # "UP", "DOWN", "LEFT", "RIGHT", "DIAG_LEFT", "DIAG_RIGHT", "DIAG_DOWN_LEFT", "DIAG_DOWN_RIGHT", "BOSS_CUSTOM"
        self.frame = 0  # Contador para animación retro
        self.custom_vx = custom_vx  # Velocidad X personalizada para disparos del jefe
        self.custom_vy = custom_vy  # Velocidad Y personalizada para disparos del jefe

    def move(self):
        if self.direction == "BOSS_CUSTOM":
            # Movimiento personalizado con velocidades custom
            if self.custom_vx is not None and self.custom_vy is not None:
                self.x += self.custom_vx
                self.y += self.custom_vy
        elif self.direction == "UP":
            self.y -= self.speed
        elif self.direction == "DOWN":
            self.y += self.speed
        elif self.direction == "LEFT":
            self.x -= self.speed
        elif self.direction == "RIGHT":
            self.x += self.speed
        elif self.direction == "DIAG_LEFT":
            self.x -= self.speed * 0.7
            self.y -= self.speed * 0.7
        elif self.direction == "DIAG_RIGHT":
            self.x += self.speed * 0.7
            self.y -= self.speed * 0.7
        elif self.direction == "DIAG_DOWN_LEFT":
            self.x -= self.speed * 0.7
            self.y += self.speed * 0.7
        elif self.direction == "DIAG_DOWN_RIGHT":
            self.x += self.speed * 0.7
            self.y += self.speed * 0.7
        self.frame += 1

    def draw(self, screen):
        if self.direction == "RIGHT":
            # Bala principal del jugador: alargadita retro naranja/rojo pulsante
            # Animación retro: alterna entre naranja y rojo cada 3 frames
            colors = [(255, 140, 0), (255, 50, 50)]  # Naranja y Rojo
            color = colors[(self.frame // 3) % 2]

            # Dibujar forma alargada (rectángulo horizontal)
            bullet_width = 16
            bullet_height = 6
            pygame.draw.rect(
                screen,
                color,
                (
                    int(self.x - bullet_width // 2),
                    int(self.y - bullet_height // 2),
                    bullet_width,
                    bullet_height,
                ),
            )

            # Añadir punta puntiaguda (triángulo)
            tip_points = [
                (int(self.x + bullet_width // 2), int(self.y)),
                (int(self.x + bullet_width // 2 + 4), int(self.y - 3)),
                (int(self.x + bullet_width // 2 + 4), int(self.y + 3)),
            ]
            pygame.draw.polygon(screen, (255, 200, 0), tip_points)

            # Efecto de brillo retro en el centro (cada 6 frames)
            if (self.frame // 6) % 2 == 0:
                pygame.draw.rect(
                    screen,
                    (255, 255, 150),
                    (
                        int(self.x - bullet_width // 4),
                        int(self.y - 2),
                        bullet_width // 2,
                        4,
                    ),
                )
        elif self.direction == "BOSS_CUSTOM":
            # Disparos del jefe: más brillantes y futuristas (verde/cian con plasma)
            bullet_width = 14
            bullet_height = 8

            # Color pulsante futurista
            colors = [(0, 255, 150), (0, 200, 255)]  # Verde lima y Cian
            color = colors[(self.frame // 3) % 2]

            # Dibujar rectángulo del proyectil
            pygame.draw.rect(
                screen,
                color,
                (
                    int(self.x - bullet_width // 2),
                    int(self.y - bullet_height // 2),
                    bullet_width,
                    bullet_height,
                ),
            )

            # Aura de energía
            pygame.draw.rect(
                screen,
                (0, 255, 200),
                (
                    int(self.x - bullet_width // 2 - 1),
                    int(self.y - bullet_height // 2 - 1),
                    bullet_width + 2,
                    bullet_height + 2,
                ),
                1,
            )

            # Núcleo brillante
            if (self.frame // 4) % 2 == 0:
                pygame.draw.circle(
                    screen, (255, 255, 255), (int(self.x), int(self.y)), 2
                )
        else:
            color = YELLOW if self.direction == "DOWN" else GREEN
            if self.direction == "UP":
                color = (0, 255, 255)  # Cian
            elif self.direction == "LEFT":
                color = BLUE
            elif self.direction in (
                "DIAG_LEFT",
                "DIAG_RIGHT",
                "DIAG_DOWN_LEFT",
                "DIAG_DOWN_RIGHT",
            ):
                color = (0, 255, 100)  # Verde claro
            pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
