import random

import pygame
from alien_boss_l2 import AlienBoss
from background import Background
from bullet import Bullet
from config import BLACK, BULLET_DAMAGE, FPS, HEIGHT, LEVEL_DURATION, RED, WHITE, WIDTH
from dragon_boss_l4 import DragonBoss
from explosion import Explosion
from goblin_boss_l3 import GoblinBoss
from phoenix_boss_l6 import PhoenixBoss
from player import Player
from powerup import PowerUp
from robot_boss_l1 import RobotBoss
from score import ScoreSystem
from spaceship_enemy import SpaceShipEnemy


class Game:
    def __init__(self, screen, sound_manager=None, start_level=1, num_players=1):
        self.screen = screen
        self.sound = sound_manager
        self.num_players = num_players if num_players in (1, 2) else 1
        # Soporte para 2 jugadores
        if self.num_players == 2:
            self.players = [
                Player(40, HEIGHT // 2, 20, 10, 3),  # Jugador 1
                Player(40, HEIGHT // 2 + 60, 20, 10, 3),  # Jugador 2 (desfasado)
            ]
        else:
            self.players = [Player(40, HEIGHT // 2, 20, 10, 3)]
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.projectiles = []  # Proyectiles especiales del jefe (bombitas explosivas)
        self.powerups = []
        self.explosions = []
        # self.score = 0
        self.level = start_level
        self.max_enemies = 5 + (3 * self.level)
        self.background = Background(self.level)
        self.paused = False
        self.auto_shoot_timer = 0
        self.game_over = False
        self.game_over_timer = 0
        self.score_system = ScoreSystem()

        # Timer de nivel (cuenta regresiva)
        self.level_timer = LEVEL_DURATION * FPS  # Frames totales del nivel
        self.boss_phase = False  # True cuando el timer llega a 0
        self.boss = None
        self.boss_minion_timer = 0

        # Flag para detectar timeout del Phoenix (nivel 6)
        self.phoenix_timeout = False
        self.timeout_display_timer = 0  # Timer para mostrar mensaje de timeout

    def run_frame(self, clock):
        """Ejecuta un frame del juego. Retorna 'quit', 'menu', o None."""
        self.screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused

        if self.game_over:
            self.game_over_timer += 1
            self.draw_game_elements()
            pygame.display.flip()
            clock.tick(FPS)
            # Volver al menú después de 3 segundos
            if self.game_over_timer >= FPS * 3:
                return "menu"
            return None

        if not self.paused:
            keys = pygame.key.get_pressed()
            # Jugador 1 (flechas y espacio)
            p1 = self.players[0]
            if keys[pygame.K_LEFT] and p1.x > p1.speed and p1.life > 0:
                p1.move("LEFT")
            if keys[pygame.K_RIGHT] and p1.x < WIDTH - p1.speed and p1.life > 0:
                p1.move("RIGHT")
            if keys[pygame.K_UP] and p1.y > p1.speed and p1.life > 0:
                p1.move("UP")
            if keys[pygame.K_DOWN] and p1.y < HEIGHT - p1.speed and p1.life > 0:
                p1.move("DOWN")
            if keys[pygame.K_SPACE] and p1.life > 0 and not self.phoenix_timeout:
                self.bullets.append(Bullet(p1.x, p1.y, 20, "RIGHT"))
                self._play_sound("shoot")

            # Jugador 2 (si existe): WASD y F para disparar
            if self.num_players == 2 and len(self.players) > 1:
                p2 = self.players[1]
                if keys[pygame.K_a] and p2.x > p2.speed and p2.life > 0:
                    p2.move("LEFT")
                if keys[pygame.K_d] and p2.x < WIDTH - p2.speed and p2.life > 0:
                    p2.move("RIGHT")
                if keys[pygame.K_w] and p2.y > p2.speed and p2.life > 0:
                    p2.move("UP")
                if keys[pygame.K_s] and p2.y < HEIGHT - p2.speed and p2.life > 0:
                    p2.move("DOWN")
                if keys[pygame.K_f] and p2.life > 0 and not self.phoenix_timeout:
                    self.bullets.append(Bullet(p2.x, p2.y, 20, "RIGHT"))
                    self._play_sound("shoot")

            self.update_game_state()

        self.draw_game_elements()
        pygame.display.flip()
        clock.tick(FPS)
        return None

    # Mantener compatibilidad con el loop anterior
    def run(self):
        running = True
        clock = pygame.time.Clock()
        while running:
            result = self.run_frame(clock)
            if result in ("quit", "menu"):
                running = False
        pygame.quit()

    def _play_sound(self, name):
        if self.sound:
            self.sound.play(name)

    def spawn_enemy(self):
        """Crea una nave espacial enemiga con propiedades según el nivel"""
        base_speed = 5 + (self.level - 1) * 0.5
        agil_chance = min(100, 10 + (20 * self.level))
        agil = random.randint(0, 100) < agil_chance
        speed = base_speed + 2 if agil else base_speed
        x = WIDTH
        y = random.randint(30, HEIGHT - 30)
        self.enemies.append(SpaceShipEnemy(x, y, 30, speed, agil))

    def spawn_powerup(self, x, y):
        """Crea un power-up aleatorio"""
        powerup_types = [
            PowerUp.WEAPON_LEFT,
            PowerUp.WEAPON_RIGHT,
            PowerUp.WEAPON_DIAG_RIGHT,
            PowerUp.WEAPON_DIAG_LEFT,
            PowerUp.WEAPON_DIAG_DOWN_RIGHT,
            PowerUp.WEAPON_DIAG_DOWN_LEFT,
            PowerUp.WEAPON_UP,
            PowerUp.WEAPON_DOWN,
            PowerUp.LIFE,
            PowerUp.SHIELD,
        ]
        powerup_type = random.choice(powerup_types)
        self.powerups.append(PowerUp(x, y, powerup_type))

    def auto_shoot_weapons(self):
        """Dispara automáticamente según los power-ups activos"""
        if PowerUp.WEAPON_LEFT in self.players.powerups:
            count = self.players.powerups[PowerUp.WEAPON_LEFT]["count"]
            for i in range(count):
                offset = (i - (count - 1) / 2) * 8
                self.bullets.append(
                    Bullet(self.players.x, self.players.y + offset, 20, "LEFT")
                )

        if PowerUp.WEAPON_RIGHT in self.players.powerups:
            count = self.players.powerups[PowerUp.WEAPON_RIGHT]["count"]

            if count == 0:
                self.bullets.append(Bullet(self.players.x, self.players.y, 20, "RIGHT"))
            elif count == 1:
                self.bullets.append(
                    Bullet(self.players.x, self.players.y - 8, 20, "RIGHT")
                )
                self.bullets.append(
                    Bullet(self.players.x, self.players.y + 8, 20, "RIGHT")
                )
            elif count == 2:
                self.bullets.append(
                    Bullet(self.players.x, self.players.y - 12, 20, "RIGHT")
                )
                self.bullets.append(Bullet(self.players.x, self.players.y, 20, "RIGHT"))
                self.bullets.append(
                    Bullet(self.players.x, self.players.y + 12, 20, "RIGHT")
                )
            else:
                self.bullets.append(
                    Bullet(self.players.x, self.players.y - 16, 20, "RIGHT")
                )
                self.bullets.append(
                    Bullet(self.players.x, self.players.y - 4, 20, "RIGHT")
                )
                self.bullets.append(
                    Bullet(self.players.x, self.players.y + 8, 20, "RIGHT")
                )

                if count >= 3:
                    self.bullets.append(
                        Bullet(self.players.x + 20, self.players.y, 20, "RIGHT")
                    )
                if count >= 4:
                    self.bullets.append(
                        Bullet(self.players.x + 30, self.players.y, 20, "RIGHT")
                    )
                if count >= 5:
                    self.bullets.append(
                        Bullet(self.players.x + 40, self.players.y, 20, "RIGHT")
                    )

        if PowerUp.WEAPON_DIAG_LEFT in self.players.powerups:
            self.bullets.append(Bullet(self.players.x, self.players.y, 15, "DIAG_LEFT"))
        if PowerUp.WEAPON_DIAG_RIGHT in self.players.powerups:
            self.bullets.append(Bullet(self.players.x, self.players.y, 15, "DIAG_RIGHT"))
        if PowerUp.WEAPON_DIAG_DOWN_LEFT in self.players.powerups:
            self.bullets.append(
                Bullet(self.players.x, self.players.y, 15, "DIAG_DOWN_LEFT")
            )
        if PowerUp.WEAPON_DIAG_DOWN_RIGHT in self.players.powerups:
            self.bullets.append(
                Bullet(self.players.x, self.players.y, 15, "DIAG_DOWN_RIGHT")
            )
        if PowerUp.WEAPON_UP in self.players.powerups:
            self.bullets.append(Bullet(self.players.x, self.players.y, 20, "UP"))
        if PowerUp.WEAPON_DOWN in self.players.powerups:
            self.bullets.append(Bullet(self.players.x, self.players.y, 20, "DOWN"))

    def update_game_state(self):
        # Mover balas del jugador
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.y < 0 or bullet.y > HEIGHT or bullet.x < 0 or bullet.x > WIDTH:
                self.bullets.remove(bullet)

        # Disparo automático con power-ups para cada jugador
        for idx, player in enumerate(self.players):
            if player.life > 0 and player.powerups:
                self.auto_shoot_timer += 1
                if self.auto_shoot_timer >= 10:
                    self.auto_shoot_timer = 0
                    self.auto_shoot_weapons_for(player)

        # Spawneo de enemigos
        any_alive = any(p.life > 0 for p in self.players)
        if (
            any_alive
            and not self.boss_phase
            and len(self.enemies) < self.max_enemies
        ):
            self.spawn_enemy()

        # Subditos del boss
        if self.boss_phase and self.boss and self.boss.alive and any_alive:
            self.boss_minion_timer += 1
            if self.boss_minion_timer >= 90 and len(self.enemies) < 3:
                self.boss_minion_timer = 0
                self.spawn_enemy()

        # Procesar enemigos - usar una lista para marcar los que hay que eliminar
        enemies_to_remove = []
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.x < 0:
                enemies_to_remove.append(enemy)
                continue

            # Verificar colisiones con balas
            bullet_hit = False
            for bullet in self.bullets[:]:
                if self.check_collision(bullet, enemy):
                    self.bullets.remove(bullet)
                    self.explosions.append(
                        Explosion(enemy.x, enemy.y, num_particles=16)
                    )
                    if enemy.agil:
                        enemy_type = "agil"
                    else:
                        enemy_type = "normal"

                    self.score_system.add_score(enemy_type, enemy.x, enemy.y)
                    enemies_to_remove.append(enemy)
                    self._play_sound("explosion")
                    if random.randint(0, 100) < 50:
                        self.spawn_powerup(enemy.x, enemy.y)
                    bullet_hit = True
                    break

            if bullet_hit:
                continue

            # Verificar ataque a cada jugador
            for player in self.players:
                if self.check_attack(enemy, player):
                    enemies_to_remove.append(enemy)
                    # Si el escudo está activo, protege completamente sin desactivarse
                    if player.shield_active:
                        pass
                    elif player.powerups:
                        loseable_powerups = [
                            p
                            for p in player.powerups.keys()
                            if p != PowerUp.WEAPON_RIGHT
                        ]
                        if loseable_powerups:
                            powerup_to_lose = random.choice(loseable_powerups)
                            player.remove_powerup(powerup_to_lose)
                        else:
                            player.life = max(player.life - 1, 0)
                        self._play_sound("hit")
                    else:
                        player.life = max(player.life - 1, 0)
                        self._play_sound("hit")
                    break

        # Eliminar todos los enemigos marcados
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

        # Disparos de enemigos
        if any_alive:
            for enemy in self.enemies:
                if random.randint(0, 100) < 5:
                    self.enemy_bullets.append(enemy.shoot())
                    self._play_sound("enemy_shoot")

        # Mover balas enemigas
        for bullet in self.enemy_bullets[:]:
            bullet.move()
            if bullet.x < 0 or bullet.x > WIDTH or bullet.y < 0 or bullet.y > HEIGHT:
                self.enemy_bullets.remove(bullet)

        # Colisiones entre balas del jugador y del enemigo
        for player_bullet in self.bullets[:]:
            for enemy_bullet in self.enemy_bullets[:]:
                if self.check_collision(player_bullet, enemy_bullet):
                    if player_bullet in self.bullets:
                        self.bullets.remove(player_bullet)
                    if enemy_bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(enemy_bullet)
                        self.score_system.total_score += 2
                    break

        # Colisiones balas enemigas con jugadores
        for bullet in self.enemy_bullets[:]:
            for player in self.players:
                if self.check_collision(bullet, player):
                    self.enemy_bullets.remove(bullet)
                    if player.shield_active:
                        pass
                    else:
                        player.life = max(player.life - 1, 0)
                        self._play_sound("hit")

        # MANEJO DE PROJECTILES ESPECIALES (BOMBITAS EXPLOSIVAS DEL JEFE)
        for projectile in self.projectiles[:]:
            projectile.move()
            if projectile.is_out_of_bounds():
                self.projectiles.remove(projectile)
                continue
            explosion_rect = projectile.get_explosion_rect()
            for player in self.players:
                player_rect = pygame.Rect(
                    player.x - player.size,
                    player.y - player.size,
                    player.size * 2,
                    player.size * 2,
                )
                if explosion_rect.colliderect(player_rect):
                    ox = projectile.x
                    oy = projectile.y
                    for _ in range(3):
                        self.explosions.append(
                            Explosion(
                                ox + random.randint(-30, 30),
                                oy + random.randint(-30, 30),
                                num_particles=32,
                            )
                        )
                    if player.shield_active:
                        pass
                    else:
                        player.life = max(player.life - 2, 0)
                        self._play_sound("hit")
                    self.projectiles.remove(projectile)
                    break

        # Mover y colisionar power-ups
        for powerup in self.powerups[:]:
            powerup.move()
            if powerup.x < 0 or powerup.x > WIDTH:
                self.powerups.remove(powerup)
            else:
                for player in self.players:
                    if self.check_collision(powerup, player):
                        if powerup.powerup_type == PowerUp.LIFE:
                            player.life += 1
                        elif powerup.powerup_type == PowerUp.SHIELD:
                            player.activate_shield()
                        else:
                            player.add_powerup(powerup.powerup_type)
                        self.powerups.remove(powerup)
                        self._play_sound("powerup")
                        break

        # Actualizar explosiones
        for explosion in self.explosions[:]:
            explosion.update()
            if explosion.is_dead():
                self.explosions.remove(explosion)

        # Actualizar escudo y powerups de cada jugador
        for player in self.players:
            player.update_shield()
            player.update_powerups()

        # Timer de nivel y fase de boss
        if not self.boss_phase:
            self.level_timer -= 1
            if self.level_timer <= 0:
                self.level_timer = 0
                self.boss_phase = True
                self.boss = self._create_boss(self.level)
                self.enemies.clear()
                self._play_sound("boss_appear")
        else:
            self._update_boss()
            if self.phoenix_timeout:
                self.timeout_display_timer += 1
                if self.timeout_display_timer >= FPS * 3:
                    self.level_timer = LEVEL_DURATION * FPS
                    self.boss_phase = False
                    self.boss = None
                    self.phoenix_timeout = False
                    self.timeout_display_timer = 0
                    self.enemies.clear()
                    self.projectiles.clear()
                    self._play_sound("level_up")

        self.score_system.update()
        self.background.update(self.level)

        # Detectar game over (todos los jugadores sin vidas)
        if all(p.life <= 0 for p in self.players) and not self.game_over:
            self.game_over = True
            self.game_over_timer = 0
            self._play_sound("game_over")

        # Eliminar todos los enemigos marcados
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.enemies.remove(enemy)

            # Resto del código sigue igual...
            if any_alive:
                for enemy in self.enemies:
                    if random.randint(0, 100) < 5:
                        self.enemy_bullets.append(enemy.shoot())
                        self._play_sound("enemy_shoot")

    def auto_shoot_weapons_for(self, player):
        # Dispara automáticamente según los power-ups activos para un jugador específico
        if PowerUp.WEAPON_LEFT in player.powerups:
            count = player.powerups[PowerUp.WEAPON_LEFT]["count"]
            for i in range(count):
                offset = (i - (count - 1) / 2) * 8
                self.bullets.append(Bullet(player.x, player.y + offset, 20, "LEFT"))
        if PowerUp.WEAPON_RIGHT in player.powerups:
            count = player.powerups[PowerUp.WEAPON_RIGHT]["count"]
            if count == 0:
                self.bullets.append(Bullet(player.x, player.y, 20, "RIGHT"))
            elif count == 1:
                self.bullets.append(Bullet(player.x, player.y - 8, 20, "RIGHT"))
                self.bullets.append(Bullet(player.x, player.y + 8, 20, "RIGHT"))
            elif count == 2:
                self.bullets.append(Bullet(player.x, player.y - 12, 20, "RIGHT"))
                self.bullets.append(Bullet(player.x, player.y, 20, "RIGHT"))
                self.bullets.append(Bullet(player.x, player.y + 12, 20, "RIGHT"))
            else:
                self.bullets.append(Bullet(player.x, player.y - 16, 20, "RIGHT"))
                self.bullets.append(Bullet(player.x, player.y - 4, 20, "RIGHT"))
                self.bullets.append(Bullet(player.x, player.y + 8, 20, "RIGHT"))
                if count >= 3:
                    self.bullets.append(Bullet(player.x + 20, player.y, 20, "RIGHT"))
                if count >= 4:
                    self.bullets.append(Bullet(player.x + 30, player.y, 20, "RIGHT"))
                if count >= 5:
                    self.bullets.append(Bullet(player.x + 40, player.y, 20, "RIGHT"))
        if PowerUp.WEAPON_DIAG_LEFT in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 15, "DIAG_LEFT"))
        if PowerUp.WEAPON_DIAG_RIGHT in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 15, "DIAG_RIGHT"))
        if PowerUp.WEAPON_DIAG_DOWN_LEFT in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 15, "DIAG_DOWN_LEFT"))
        if PowerUp.WEAPON_DIAG_DOWN_RIGHT in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 15, "DIAG_DOWN_RIGHT"))
        if PowerUp.WEAPON_UP in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 20, "UP"))
        if PowerUp.WEAPON_DOWN in player.powerups:
            self.bullets.append(Bullet(player.x, player.y, 20, "DOWN"))

    def _update_boss(self):
        if not self.boss or not self.boss.alive:
            return
        self.boss.move()

    # Timeout de Phoenix
        if isinstance(self.boss, PhoenixBoss):
            if self.boss.has_time_out() and not self.phoenix_timeout:
                self.phoenix_timeout = True
                self.timeout_display_timer = 0
                self._play_sound("boss_defeat")

    # Disparos del boss
        ref_player = next((p for p in self.players if p.life > 0), self.players[0])
        new_bullets, new_projectiles = self.boss.shoot(ref_player.x, ref_player.y)
        self.enemy_bullets.extend(new_bullets)
        self.projectiles.extend(new_projectiles)

    # Obtener el rectángulo del boss (definido una sola vez)
        boss_rect = self.boss.get_hit_rect()

    # Colisión de balas del jugador con el boss
        for bullet in self.bullets[:]:
            bullet_rect = pygame.Rect(bullet.x, bullet.y, bullet.width, bullet.height)
            if boss_rect.colliderect(bullet_rect):
                self.bullets.remove(bullet)
                self.boss.take_damage(BULLET_DAMAGE)
                if not self.boss.alive:
                    for _ in range(5):
                        ox = self.boss.x + random.randint(-40, 40)
                        oy = self.boss.y + random.randint(-40, 40)
                        self.explosions.append(Explosion(ox, oy, num_particles=24))
                    self._play_sound("boss_defeat")
                    self._advance_level()
                    break  # Salir del bucle porque el boss ya murió

    # Colisión del boss con cada jugador (solo si el boss sigue vivo)
        if self.boss and self.boss.alive:
            for player in self.players:
                player_rect = pygame.Rect(
                    player.x - player.size,
                    player.y - player.size,
                    player.size * 2,
                    player.size * 2,
            )
                if boss_rect.colliderect(player_rect):
                    if player.shield_active:
                        pass  # escudo protege
                    else:
                        player.life = max(player.life - 1, 0)
                        self._play_sound("hit")
                break  # solo daña a un jugador por frame

    def _create_boss(self, level):
        """Crea el jefe correspondiente al nivel."""
        if level == 1:
            return RobotBoss(level)
        elif level == 2:
            return AlienBoss(level)
        elif level == 3:
            return GoblinBoss(level)
        elif level == 4:
            return DragonBoss(level)
        elif level >= 5:
            # Nivel 5+: El nivel 6 es especial (Phoenix final), el 7+ repite ciclo
            if level == 5:
                # Nivel 5: KrakenBoss (aún no implementado, usar ciclo)
                boss_cycle = [RobotBoss, AlienBoss, GoblinBoss, DragonBoss]
                boss_class = boss_cycle[(level - 1) % 4]
                return boss_class(level)
            elif level == 6:
                # Nivel 6: JEFE FINAL - Phoenix con temporizador
                return PhoenixBoss(level)
            else:
                # Niveles 7+: ciclar entre todos los bosses
                boss_cycle = [RobotBoss, AlienBoss, GoblinBoss, DragonBoss, PhoenixBoss]
                boss_class = boss_cycle[(level - 1) % 5]
                return boss_class(level)

    def _advance_level(self):
        self.level += 1
        self.max_enemies = 5 + (3 * self.level)
        #self.players.size += 2
        for player in self.players:
            player.size += 2          # Aumentar tamaño
            player.life += 1          # Aumentar vida
        # self.score = 0
        #self.players.life += 1
        self.boss_phase = False
        self.boss = None
        self.level_timer = LEVEL_DURATION * FPS
        self.boss_minion_timer = 0
        self.projectiles = []  # Limpiar projectiles del jefe anterior
        self._play_sound("level_up")

    def draw_game_elements(self):
        self.background.draw(self.screen)
        # Dibujar ambos jugadores
        for idx, player in enumerate(self.players):
            player.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        # Enemigos: pasar la posición del jugador 1 como referencia (o el primero vivo)
        ref_player = next((p for p in self.players if p.life > 0), self.players[0])
        for enemy in self.enemies:
            enemy.draw(self.screen, ref_player.x, ref_player.y)
        for bullet in self.enemy_bullets:
            bullet.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        for powerup in self.powerups:
            powerup.draw(self.screen)
        for explosion in self.explosions:
            explosion.draw(self.screen)

        if self.boss and self.boss.alive:
            self.boss.draw(self.screen)
            self.boss.draw_health_bar(self.screen)

        font = pygame.font.SysFont("monospace", 20, bold=True)
        self.score_system.draw(self.screen, font)
        self.draw_text(f"Level: {self.level}", (5, 65), 16)

        # Mostrar vidas y powerups de cada jugador
        for idx, player in enumerate(self.players):
            y_offset = 85 + idx * 30
            self.draw_text(f"P{idx+1} Lifes: {player.life}", (5, y_offset), 16)
            if player.powerups:
                self.draw_powerups_visual(player, y_offset + 20)
                #self.draw_powerups_visual(self.players, y_offset)

        if not self.boss_phase:
            seconds_left = self.level_timer // FPS
            minutes = seconds_left // 60
            secs = seconds_left % 60
            timer_color = RED if seconds_left <= 10 else WHITE
            font = pygame.font.SysFont("monospace", 20, bold=True)
            timer_text = font.render(f"{minutes:02d}:{secs:02d}", 1, timer_color)
            self.screen.blit(timer_text, (WIDTH - 100, 5))
        else:
            font = pygame.font.SysFont("monospace", 20, bold=True)
            if isinstance(self.boss, PhoenixBoss) and not self.phoenix_timeout:
                time_left = self.boss.get_remaining_time()
                time_color = (
                    RED if time_left <= 5 else (255, 200, 0) if time_left <= 10 else WHITE
                )
                time_text = font.render(f"TIME: {time_left}s", 1, time_color)
                self.screen.blit(time_text, (WIDTH - 200, 5))
            boss_text = font.render("BOSS FIGHT!", 1, RED)
            self.screen.blit(boss_text, (WIDTH - 160, 45))

        if self.phoenix_timeout:
            font_large = pygame.font.SysFont("monospace", 60, bold=True)
            font_small = pygame.font.SysFont("monospace", 40, bold=True)
            timeout_text = font_large.render("TIME OUT!", 1, RED)
            timeout_rect = timeout_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
            self.screen.blit(timeout_text, timeout_rect)
            retry_text = font_small.render("LEVEL RESTART", 1, (255, 200, 0))
            retry_rect = retry_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 60))
            self.screen.blit(retry_text, retry_rect)

        if self.paused:
            self.draw_text("PAUSED", (WIDTH // 2 - 100, HEIGHT // 2 - 24), 48)

        # GAME OVER si todos los jugadores han perdido
        if all(p.life <= 0 for p in self.players):
            self.draw_text("GAME OVER", (WIDTH // 2 - 150, HEIGHT // 2 - 24), 48)
            font_small = pygame.font.SysFont("monospace", 20)
            back_text = font_small.render("Returning to menu...", True, (150, 150, 150))
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30))
            self.screen.blit(back_text, back_rect)

    #def draw_powerups_visual(self, players, y_pos=65):
    #def draw_powerups_visual(self, players, y_offset):
    def draw_powerups_visual(self, player, y_offset):
    #Dibuja los power-ups de un jugador en la posición y_offset.
        x_pos = 150
        spacing = 35
        y_pos = y_offset
        for powerup_type, data in player.powerups.items():
            count = data["count"]
            time_left = data["time"]
            color = PowerUp.COLORS.get(powerup_type, WHITE)
            symbol = PowerUp.SYMBOLS.get(powerup_type, "?")
        # Dibujar círculo, símbolo, etc.
            pygame.draw.circle(self.screen, color, (x_pos + 8, y_pos + 8), 10, 2)
            font_symbol = pygame.font.SysFont("monospace", 14, bold=True)
            symbol_text = font_symbol.render(symbol, 1, color)
            symbol_rect = symbol_text.get_rect(center=(x_pos + 8, y_pos + 8))
            self.screen.blit(symbol_text, symbol_rect)
            font_count = pygame.font.SysFont("monospace", 12)
            count_text = font_count.render(str(count), 1, color)
            self.screen.blit(count_text, (x_pos + 12, y_pos + 2))
            seconds_left = (time_left + 29) // 30
            font_time = pygame.font.SysFont("monospace", 10)
            time_text = font_time.render(f"{seconds_left}s", 1, (200, 200, 200))
            self.screen.blit(time_text, (x_pos - 3, y_pos + 16))
            x_pos += spacing

    def check_collision(self, obj1, obj2):
        if hasattr(obj1, "size"):
            x1_min = obj1.x - obj1.size // 2
            x1_max = obj1.x + obj1.size // 2
            y1_min = obj1.y
            y1_max = obj1.y + obj1.size
        else:
            x1_min = obj1.x
            x1_max = obj1.x + obj1.width
            y1_min = obj1.y
            y1_max = obj1.y + obj1.height

        if hasattr(obj2, "size"):
            x2_min = obj2.x - obj2.size // 2
            x2_max = obj2.x + obj2.size // 2
            y2_min = obj2.y
            y2_max = obj2.y + obj2.size
        else:
            x2_min = obj2.x
            x2_max = obj2.x + obj2.width
            y2_min = obj2.y
            y2_max = obj2.y + obj2.height

        return (
            x1_min < x2_max and x1_max > x2_min and y1_min < y2_max and y1_max > y2_min
        )

    def check_attack(self, enemy, player):
        enemy_left = enemy.x - enemy.size // 2 - player.size
        enemy_right = enemy.x + enemy.size // 2 + player.size
        enemy_top = enemy.y - enemy.size // 2
        enemy_bottom = enemy.y + enemy.size

        player_left = player.x
        player_right = player.x
        player_top = player.y - player.size
        player_bottom = player.y

        return (
            player_left >= enemy_left
            and player_right <= enemy_right
            and player_top >= enemy_top
            and player_bottom <= enemy_bottom
        )

    def draw_text(self, text, position, size):
        font = pygame.font.SysFont("monospace", size)
        label = font.render(text, 1, WHITE)
        self.screen.blit(label, position)

    