# game/powerups.py

import pygame
import random

POWERUPS = ["Laser", "Explosion", "Double Ball", "Slowdown", "Bouncewall"]
POWERUP_LETTERS = {
    "Laser": "L",
    "Explosion": "E",
    "Double Ball": "D",
    "Slowdown": "S",
    "Bouncewall": "B"
}

def spawn_powerup():
    powerup_type = random.choice(POWERUPS)
    new_powerup = {
        "type": powerup_type,
        "rect": pygame.Rect(random.randint(0, WIDTH - POWERUP_SIZE), 0, POWERUP_SIZE, POWERUP_SIZE)
    }
    powerups.append(new_powerup)
    powerup_spawn_sound.play()

def animate_powerup(powerup):
    if "animation" not in powerup:
        powerup["animation"] = {
            "scale": 1,
            "direction": 1
        }
    scale = powerup["animation"]["scale"]
    direction = powerup["animation"]["direction"]
    if scale >= 1.2:
        direction = -1
    elif scale <= 1:
        direction = 1
    scale += direction * 0.02
    powerup["animation"]["scale"] = scale
    powerup["animation"]["direction"] = direction
    return pygame.transform.scale(powerup_texture, (int(POWERUP_SIZE * scale), int(POWERUP_SIZE * scale)))
