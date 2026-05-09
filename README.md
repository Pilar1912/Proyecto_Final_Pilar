
# SpaceDementia - Arcade Shooter

## Descripción General
**SpaceDementia** es un juego de disparos arcade retro desarrollado en Python y Pygame. Controlas una nave espacial que debe sobrevivir oleadas de enemigos, enfrentarse a bosses únicos, recolectar power-ups y superar niveles con dificultad progresiva. El juego destaca por su estética ochentera, efectos visuales de partículas, fondo animado y una arquitectura modular orientada a objetos.

<div align="center">
  <img src="game.png" alt="Vista previa del juego" width="900"/>
</div>

---

## Características Principales

- **Movimiento 4 direcciones** (flechas)
- **Disparo principal**: derecha, animación retro
- **Power-ups**: 7 tipos, acumulables y visuales
- **Bosses**: 6 jefes únicos (robot, alien, dragón, goblin, kraken, fénix) + jefe cubo final
- **Sistema de partículas**: explosiones, efectos de bosses, fondo animado
- **HUD**: puntuación, nivel, vidas, power-ups activos
- **Dificultad progresiva**: más enemigos, mayor velocidad, bosses más complejos
- **Fondo animado**: 4 capas, paralaje, efectos por nivel
- **Soporte para gamepad y teclado**

---

## Niveles y Enemigos

- **Niveles**: Cada nivel dura 2 minutos, con incremento de dificultad y aparición de boss al final.
- **Enemigos normales**: Movimiento lineal, disparan balas azules, pueden ser ágiles (zigzag).
- **Bosses**:
  - **RobotBoss** (Nivel 1): Ataques directos y disparos múltiples.
  - **AlienBoss** (Nivel 2): Genera partículas chispa, movimientos erráticos.
  - **GoblinBoss** (Nivel 3): Dispara ráfagas y se teletransporta.
  - **DragonBoss** (Nivel 4): Lanza partículas de fuego y alas.
  - **KrakenBoss** (Nivel 5): Ataques de tentáculos y proyectiles especiales.
  - **PhoenixBoss** (Nivel 6): Renace tras ser derrotado, ataques de fuego.
  - **CubeBoss** (Final): Cubo 3D, IA de embestida, disparos múltiples, barra de vida.

---

## Power-ups

| Tipo                | Color   | Efecto                                 | Stack      |
|---------------------|---------|----------------------------------------|------------|
| WEAPON_LEFT         | Azul    | Disparo automático a la izquierda      | Hasta 3    |
| WEAPON_RIGHT        | Azul    | Disparo automático a la derecha        | Hasta 5    |
| WEAPON_DIAG_LEFT    | Amarillo| Disparo diagonal superior izquierda    | Máx 1      |
| WEAPON_DIAG_RIGHT   | Amarillo| Disparo diagonal superior derecha      | Máx 1      |
| WEAPON_UP           | Cian    | Disparo hacia arriba                   | Máx 1      |
| WEAPON_DOWN         | Verde   | Disparo hacia abajo                    | Máx 1      |
| LIFE                | Rosa    | Recupera 1 vida                        | Máx 1      |
| SHIELD              | Blanco  | Escudo temporal                        | Máx 1      |

- **Spawn**: 50% de probabilidad al destruir enemigo.
- **Movimiento**: Oscilación sinusoidal, derecha a izquierda.
- **Pérdida**: Al recibir daño, pierdes un power-up antes de perder vida.

---

## Sistema de Partículas y Efectos Visuales

- **Explosiones**: 16 partículas por enemigo, colores aleatorios, fade progresivo.
- **Bosses**: Cada boss genera partículas únicas (chispa, fuego, alas, etc.).
- **Fondo**: Estrellas, nebulosas, agujero negro animado, paralaje.

---

## Interfaz y HUD

- **Puntuación**: +10 por enemigo, +2 por bala destruida.
- **Nivel**: Muestra nivel actual y barra de progreso.
- **Vidas**: Inicial 3, +1 por nivel y por power-up LIFE.
- **Power-ups activos**: Indicador visual y contador.
- **Mensajes**: Pausa, Game Over, Victoria.

---

## ¿Cómo Jugar?

| Acción            | Tecla/Control         |
|-------------------|----------------------|
| Mover             | Flechas / D-pad      |
| Disparar          | Espacio / Botón A    |
| Pausar/Reanudar   | P / Start            |
| Salir             | Q / ESC / Back       |

### Estrategia
1. Recoge power-ups para maximizar disparos.
2. Esquiva enemigos ágiles y balas.
3. Aprovecha el crecimiento de la nave por nivel.
4. Derrota bosses para avanzar y desbloquear nuevos retos.

---

## Arquitectura del Juego

El juego está estructurado en módulos y clases principales:

- **Game**: Controlador central, gestiona lógica, colisiones, spawn, bosses, HUD.
- **Player**: Movimiento, power-ups, colisiones, escudo.
- **Enemy**: Movimiento, disparo, variantes normal y ágil.
- **Boss**: Clase abstracta para bosses, con subclases específicas (Robot, Alien, Goblin, Dragon, Kraken, Phoenix, Cube).
- **Bullet**: Proyectiles de jugador y enemigos, animaciones retro.
- **PowerUp**: Tipos, movimiento, efectos y stack.
- **Explosion**: Sistema de partículas para efectos visuales.
- **Background**: Fondo animado, estrellas, nebulosas, agujero negro.
- **SoundManager**: Manejo de efectos y música.
- **ScoreSystem**: Puntuación, combos, highscore.
- **Menu**: Menú principal, botones, starfield.
- **Config**: Constantes globales (tamaños, colores, FPS, etc).

---

## UML de Clases y Relaciones

El diagrama UML de clases y relaciones está en `diagram.puml` y cubre:

- Relaciones de composición y herencia entre Game, Player, Enemy, Bosses, Bullet, PowerUp, Explosion, Background, SoundManager, ScoreSystem, Menu, Config, etc.
- Subclases de Boss para cada jefe especial.
- Sistema de partículas y efectos visuales.

Puedes visualizar el diagrama con PlantUML o en el editor online: [PlantUML Online Editor](http://www.plantuml.com/plantuml/uml/)

---

## Instalación y Ejecución

1. **Clona el repositorio:**
   ```bash
   git clone <url-del-repo>
   cd SpaceDementia
   ```
2. **Crea entorno virtual (opcional):**
   ```bash
   python -m venv env
   env\Scripts\activate  # En Windows
   # o
   source env/bin/activate  # En Linux/Mac
   ```
3. **Instala dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Ejecuta el juego:**
   ```bash
   python src/main.py
   ```

---

## Archivos del Proyecto

```
SpaceDementia/
├── src/
│   ├── main.py        # Punto de entrada
│   ├── config.py      # Constantes globales
│   ├── game.py        # Lógica central
│   ├── player.py      # Jugador
│   ├── enemy.py       # Enemigos
│   ├── boss.py        # Boss base y subclases
│   ├── robot_boss_l1.py
│   ├── alien_boss_l2.py
│   ├── goblin_boss_l3.py
│   ├── dragon_boss_l4.py
│   ├── kraken_boss_l5.py
│   ├── phoenix_boss_l6.py
│   ├── bullet.py      # Proyectiles
│   ├── powerup.py     # Power-ups
│   ├── explosion.py   # Partículas
│   ├── background.py  # Fondo animado
│   ├── sound_manager.py
│   ├── score.py
│   ├── menu.py
│   └── ...
├── diagram.puml       # Diagrama UML
├── requirements.txt   # Dependencias
├── README.md          # Documentación
└── ...
```

---

## Créditos y Licencia

Desarrollado por Juan Navarro y colaboradores. Proyecto libre para uso y distribución, pero para contribuir o modificar, contacta a:

    juannavarro139070@correo.itm.edu.co

¡Tus ideas y sugerencias son bienvenidas!



## Licencia
Este proyecto es de libre uso, pero cualquier modificación requiere aprobación previa. Para más detalles, contacta a los autores.

