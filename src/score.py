import pygame
import json
import os


class FloatingText:
    """Texto flotante que aparece al sumar puntos"""
    
    def __init__(self, text, x, y, color=(255, 255, 0)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 60
        self.velocity_y = -2
    
    def update(self):
        self.life -= 1
        self.y += self.velocity_y
        return self.life > 0
    
    def draw(self, screen, font):
        if self.life > 0:
            alpha = min(255, self.life * 4)
            text_surf = font.render(self.text, True, self.color)
            text_surf.set_alpha(alpha)
            screen.blit(text_surf, (self.x - 20, self.y))


class ScoreSystem:
    """Sistema de puntuación y combo"""
    
    def __init__(self):
        self.total_score = 0
        self.combo = 0
        self.max_combo = 0
        self.combo_timer = 0
        self.combo_timeout = 120  # 2 segundos a 60 FPS
        
        # ✅ SOLO los tipos de enemigos que tienes
        self.base_scores = {
            'normal': 100,   # Enemigo rojo (agil=False)
            'agil': 150,     # Enemigo amarillo (agil=True)
        }
        
        # Estadísticas
        self.kills_by_type = {
            'normal': 0,
            'agil': 0,
        }
        
        self.floating_texts = []
        self.high_score = self._load_high_score()
        self.new_record = False
    
    def _load_high_score(self):
        try:
            if os.path.exists('highscore.json'):
                with open('highscore.json', 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except:
            pass
        return 0
    
    def _save_high_score(self):
        try:
            with open('highscore.json', 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except:
            pass
    
    def _get_combo_multiplier(self):
        """Multiplicador según combo"""
        if self.combo >= 30:
            return 3.0
        elif self.combo >= 20:
            return 2.0
        elif self.combo >= 10:
            return 1.5
        elif self.combo >= 5:
            return 1.2
        return 1.0
    
    def add_score(self, enemy_type, x, y):
        """
        Añadir puntuación al eliminar un enemigo
        enemy_type puede ser: 'normal' o 'agil'
        """
        base_score = self.base_scores.get(enemy_type, 100)
        multiplier = self._get_combo_multiplier()
        
        # Bonus por racha
        bonus = 0
        if self.combo >= 20:
            bonus = int(base_score * 0.5)
        elif self.combo >= 10:
            bonus = int(base_score * 0.2)
        
        final_score = int(base_score * multiplier) + bonus
        
        # Actualizar puntuación
        self.total_score += final_score
        
        # Actualizar combo
        self.combo += 1
        self.combo_timer = self.combo_timeout
        
        if self.combo > self.max_combo:
            self.max_combo = self.combo
        
        # Actualizar estadísticas
        if enemy_type in self.kills_by_type:
            self.kills_by_type[enemy_type] += 1
        
        # Verificar récord
        if self.total_score > self.high_score:
            self.high_score = self.total_score
            self._save_high_score()
            self.new_record = True
        
        # Crear efecto visual
        self._add_floating_text(final_score, x, y, multiplier)
        
        return final_score
    
    def _add_floating_text(self, score, x, y, multiplier):
        self.floating_texts.append(FloatingText(f"+{score}", x, y))
        
        if multiplier > 1:
            self.floating_texts.append(
                FloatingText(f"x{multiplier}!", x, y - 20, (255, 150, 0))
            )
        elif self.combo >= 10:
            self.floating_texts.append(
                FloatingText("COMBO!", x, y - 20, (255, 200, 0))
            )
    
    def update(self):
        # Actualizar combo timer
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer == 0:
                self.combo = 0
        
        # Actualizar textos flotantes
        for text in self.floating_texts[:]:
            if not text.update():
                self.floating_texts.remove(text)
        
        self.new_record = False
    
    def draw(self, screen, font):
        # Puntuación actual
        score_text = font.render(f"SCORE: {self.total_score:06d}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        # High score
        high_text = font.render(f"HIGH: {self.high_score:06d}", True, (255, 255, 0))
        screen.blit(high_text, (10, 45))
        
        # Nuevo récord
        if self.new_record:
            record_font = pygame.font.Font(None, 24)
            record_text = record_font.render("NEW RECORD!", True, (255, 215, 0))
            screen.blit(record_text, (10, 75))
        
        # Combo
        if self.combo >= 5:
            if self.combo >= 30:
                color = (255, 50, 50)
            elif self.combo >= 20:
                color = (255, 100, 0)
            elif self.combo >= 10:
                color = (255, 200, 0)
            else:
                color = (255, 255, 255)
            
            combo_text = font.render(f"x{self.combo} COMBO", True, color)
            screen.blit(combo_text, (10, 110))
            
            # Barra de tiempo
            if self.combo_timer > 0:
                bar_width = 200 * (self.combo_timer / self.combo_timeout)
                pygame.draw.rect(screen, color, (10, 145, bar_width, 5))
        
        # Textos flotantes
        for text in self.floating_texts:
            text.draw(screen, font)
    
    def get_statistics(self):
        return {
            'total_score': self.total_score,
            'max_combo': self.max_combo,
            'total_kills': sum(self.kills_by_type.values()),
            'normal_kills': self.kills_by_type['normal'],
            'agil_kills': self.kills_by_type['agil']
        }