#!/usr/bin/env python3
"""Script para actualizar volúmenes en sound_manager.py"""

file_path = "src/sound_manager.py"

# Leer el archivo
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Realizar reemplazos de volumen
replacements = [
    # Cambiar 10000 a 14000 (_tone)
    ("int(val * 10000)", "int(val * 14000)"),
    # Cambiar 9000 a 12000 (_sweep, _game_over)
    ("int(val * 9000)", "int(val * 12000)"),
    # Cambiar 8000 a 11000 (_coin, _boss_defeat)
    ("int(val * 8000)", "int(val * 11000)"),
    # Cambiar 11000 a 14000 (_explosion, _boss_roar)
    ("int(val * 11000)", "int(val * 14000)"),
]

for old, new in replacements:
    content = content.replace(old, new)

# Escribir el archivo actualizado
with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("✓ Volúmenes actualizados correctamente en sound_manager.py")
