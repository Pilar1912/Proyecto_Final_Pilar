"""
Generador de sprites 2D para Spacedementia.
Crea 3 enemigos tipo arcade retro con estilo pixel art/cartoon oscuro.
"""

from PIL import Image, ImageDraw
import math


def create_red_creature():
    """Criatura orgánica roja tipo monstruo alienígena."""
    size = 60
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    
    # Cuerpo principal - forma orgánica
    body_points = [
        (cx - 15, cy - 18),
        (cx - 18, cy - 8),
        (cx - 20, cy + 5),
        (cx - 15, cy + 18),
        (cx + 0, cy + 22),
        (cx + 15, cy + 18),
        (cx + 20, cy + 5),
        (cx + 18, cy - 8),
        (cx + 15, cy - 18),
    ]
    draw.polygon(body_points, fill=(180, 20, 20), outline=(60, 0, 0))
    
    # Mandíbulas afiladas (arriba)
    jaw_top_left = [(cx - 10, cy - 18), (cx - 12, cy - 26), (cx - 6, cy - 20)]
    jaw_top_right = [(cx + 10, cy - 18), (cx + 12, cy - 26), (cx + 6, cy - 20)]
    draw.polygon(jaw_top_left, fill=(220, 10, 10), outline=(60, 0, 0))
    draw.polygon(jaw_top_right, fill=(220, 10, 10), outline=(60, 0, 0))
    
    # Mandíbulas afiladas (abajo)
    jaw_bottom_left = [(cx - 10, cy + 18), (cx - 12, cy + 26), (cx - 6, cy + 20)]
    jaw_bottom_right = [(cx + 10, cy + 18), (cx + 12, cy + 26), (cx + 6, cy + 20)]
    draw.polygon(jaw_bottom_left, fill=(220, 10, 10), outline=(60, 0, 0))
    draw.polygon(jaw_bottom_right, fill=(220, 10, 10), outline=(60, 0, 0))
    
    # Alas membranosas (arriba-izquierda y arriba-derecha)
    wing_left = [(cx - 18, cy - 8), (cx - 28, cy - 12), (cx - 26, cy - 2)]
    wing_right = [(cx + 18, cy - 8), (cx + 28, cy - 12), (cx + 26, cy - 2)]
    draw.polygon(wing_left, fill=(140, 10, 10), outline=(40, 0, 0))
    draw.polygon(wing_right, fill=(140, 10, 10), outline=(40, 0, 0))
    
    # Tentáculos cortos
    tentacle_points = [
        [(cx - 20, cy + 5), (cx - 28, cy + 10)],
        [(cx + 20, cy + 5), (cx + 28, cy + 10)],
    ]
    for points in tentacle_points:
        draw.line(points, fill=(220, 10, 10), width=3)
    
    # Ojos brillantes (3 ojos distribuidos)
    eye_positions = [(cx - 8, cy - 5), (cx, cy - 8), (cx + 8, cy - 5)]
    for ex, ey in eye_positions:
        draw.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 100, 100))
        draw.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=(0, 0, 0))
    
    # Detalles púrpura/negro en el cuerpo
    draw.ellipse([cx - 12, cy - 8, cx - 6, cy - 2], fill=(100, 0, 100, 150))
    draw.ellipse([cx + 6, cy - 8, cx + 12, cy - 2], fill=(100, 0, 100, 150))
    
    return img


def create_yellow_creature():
    """Parásito alienígena amarillo venenoso con púas."""
    size = 50
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    
    # Cuerpo principal - forma alargada y puntiaguda
    body_points = [
        (cx, cy - 16),
        (cx - 14, cy - 8),
        (cx - 16, cy + 4),
        (cx - 12, cy + 14),
        (cx, cy + 18),
        (cx + 12, cy + 14),
        (cx + 16, cy + 4),
        (cx + 14, cy - 8),
    ]
    draw.polygon(body_points, fill=(230, 220, 40), outline=(180, 160, 0))
    
    # Púas laterales (arriba)
    spikes_top = [
        [(cx - 16, cy - 4), (cx - 22, cy - 8)],
        [(cx + 16, cy - 4), (cx + 22, cy - 8)],
    ]
    for spike in spikes_top:
        draw.line(spike, fill=(255, 240, 100), width=2)
    
    # Púas laterales (abajo)
    spikes_bottom = [
        [(cx - 14, cy + 10), (cx - 22, cy + 12)],
        [(cx + 14, cy + 10), (cx + 22, cy + 12)],
    ]
    for spike in spikes_bottom:
        draw.line(spike, fill=(255, 240, 100), width=2)
    
    # Detalles verdes ácidos
    accent_points = [(cx - 8, cy - 2), (cx + 8, cy - 2), (cx, cy + 6)]
    draw.polygon(accent_points, fill=(100, 220, 80, 180))
    
    # Ventosas/picos en el centro
    for i, vx in enumerate([cx - 6, cx, cx + 6]):
        vy = cy
        draw.ellipse([vx - 2, vy - 2, vx + 2, vy + 2], fill=(200, 200, 0))
        draw.ellipse([vx - 1, vy - 1, vx + 1, vy + 1], fill=(100, 100, 0))
    
    # Líneas de púas pequeñas en los costados
    for y_offset in [-6, 0, 6]:
        draw.line([(cx - 16, cy + y_offset), (cx - 19, cy + y_offset - 2)], 
                  fill=(200, 190, 30), width=1)
        draw.line([(cx + 16, cy + y_offset), (cx + 19, cy + y_offset - 2)], 
                  fill=(200, 190, 30), width=1)
    
    return img


def create_space_robot():
    """Robot espacial futurista metálico - forma cuadrangular."""
    size = 80
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    
    # Cuerpo principal cuadrangular
    body_rect = [cx - 24, cy - 28, cx + 24, cy + 28]
    draw.rectangle(body_rect, fill=(90, 110, 135), outline=(180, 200, 220))
    draw.rectangle(body_rect, outline=(50, 70, 95), width=2)
    
    # Paneles superiores
    panel_top_left = [cx - 22, cy - 26, cx - 8, cy - 14]
    panel_top_right = [cx + 8, cy - 26, cx + 22, cy - 14]
    draw.rectangle(panel_top_left, fill=(70, 85, 105), outline=(180, 200, 220))
    draw.rectangle(panel_top_right, fill=(70, 85, 105), outline=(180, 200, 220))
    
    # Ojo central grande (visera)
    eye_box = [cx - 8, cy - 10, cx + 8, cy + 10]
    draw.ellipse(eye_box, fill=(50, 50, 50), outline=(200, 240, 255))
    draw.ellipse([cx - 5, cy - 7, cx + 5, cy + 7], fill=(150, 240, 255))
    draw.ellipse([cx - 2, cy - 4, cx + 2, cy + 4], fill=(0, 0, 0))
    
    # Cañones laterales (derecha)
    cannon_right = [cx + 20, cy - 8, cx + 30, cy + 8]
    draw.rectangle(cannon_right, fill=(80, 90, 110), outline=(200, 240, 255))
    draw.line([(cx + 30, cy - 6), (cx + 35, cy - 6)], fill=(255, 100, 80), width=3)
    draw.line([(cx + 30, cy + 6), (cx + 35, cy + 6)], fill=(255, 100, 80), width=3)
    
    # Cañones laterales (izquierda)
    cannon_left = [cx - 30, cy - 8, cx - 20, cy + 8]
    draw.rectangle(cannon_left, fill=(80, 90, 110), outline=(200, 240, 255))
    draw.line([(cx - 30, cy - 6), (cx - 35, cy - 6)], fill=(255, 100, 80), width=3)
    draw.line([(cx - 30, cy + 6), (cx - 35, cy + 6)], fill=(255, 100, 80), width=3)
    
    # Detalles de circuitos (líneas cian)
    draw.line([(cx - 18, cy + 15), (cx - 8, cy + 20)], fill=(120, 235, 255), width=1)
    draw.line([(cx + 8, cy + 15), (cx + 18, cy + 20)], fill=(120, 235, 255), width=1)
    draw.line([(cx - 12, cy + 22), (cx + 12, cy + 22)], fill=(120, 235, 255), width=1)
    
    # Placas blindadas inferiores
    armor_bottom = [cx - 22, cy + 18, cx + 22, cy + 26]
    draw.rectangle(armor_bottom, fill=(70, 85, 105), outline=(180, 200, 220))
    draw.line([(cx - 22, cy + 22), (cx + 22, cy + 22)], fill=(180, 200, 220), width=1)
    
    # Detalles de oxidación (naranjas)
    rust_spots = [(cx - 18, cy + 25), (cx + 12, cy - 22), (cx - 10, cy + 20)]
    for rx, ry in rust_spots:
        draw.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=(220, 100, 30))
    
    # Línea de energía central (azul)
    draw.line([(cx, cy - 28), (cx, cy + 28)], fill=(150, 240, 255), width=2)
    
    # Núcleo energético central (inferior al ojo)
    core_box = [cx - 6, cy + 12, cx + 6, cy + 18]
    draw.ellipse(core_box, fill=(255, 100, 0), outline=(200, 240, 255))
    draw.ellipse([cx - 2, cy + 14, cx + 2, cy + 16], fill=(255, 200, 100))
    
    return img


if __name__ == '__main__':
    import os
    
    assets_dir = 'assets'
    os.makedirs(assets_dir, exist_ok=True)
    
    # Generar enemigo rojo
    red_enemy = create_red_creature()
    red_enemy.save(f'{assets_dir}/enemy_red.png')
    print(f"✓ Sprite enemigo rojo guardado: {assets_dir}/enemy_red.png ({red_enemy.size[0]}x{red_enemy.size[1]}px)")
    
    # Generar enemigo amarillo
    yellow_enemy = create_yellow_creature()
    yellow_enemy.save(f'{assets_dir}/enemy_yellow.png')
    print(f"✓ Sprite enemigo amarillo guardado: {assets_dir}/enemy_yellow.png ({yellow_enemy.size[0]}x{yellow_enemy.size[1]}px)")
    
    # Generar jefe robot
    space_robot = create_space_robot()
    space_robot.save(f'{assets_dir}/boss_space_robot.png')
    print(f"✓ Sprite jefe robot guardado: {assets_dir}/boss_space_robot.png ({space_robot.size[0]}x{space_robot.size[1]}px)")
    
    print("\n✓ Todos los sprites han sido generados exitosamente.")
