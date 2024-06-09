# Kian's Powerful, Deadly Pong!

Welcome to Kian's Powerful, Deadly Pong! This is an advanced version of the classic Pong game, featuring various power-ups, leaderboards, and more exciting gameplay elements.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Controls](#controls)
- [Power-ups](#power-ups)
- [Assets](#assets)
- [Credits](#credits)

## Features
- Classic Pong gameplay with enhanced mechanics
- Multiple power-ups to spice up the game
- Persistent leaderboard to track high scores
- ASCII art display
- Sound effects and background music

## Installation
1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install the required dependencies:**
Ensure you have Python 3 installed. Then, install Pygame using pip:

```bash

    pip install pygame
```


3. **Place your assets:**
    Sound files should be placed in the sound directory.
    Ensure the following files are present:

    ```  
    hit_sound.wav
    score_sound.wav
    game_over_sound.wav
    powerup_spawn.wav
    powerup_claim.wav
    explosion_sound.wav
    laser_sound.wav
    background_music.wav
    ```

## How to launch

Run the game:
```bash
python main.py
```

Select your control method:

    Press 1 for scroll wheel control.
    Press 2 for mouse control.

Enjoy the game!

## Controls

Scroll Wheel Control:

    Use the scroll wheel to move the paddle up and down.
Mouse Control:

    Move the mouse up and down to control the paddle.
Keyboard:

    Press SPACE to add a ball.
    Press R to restart the game after a game over.
    Press L to display the leaderboard.
    Left Mouse Button: Claim a power-up.
    Right Mouse Button: Use a power-up.

## Power-ups

Power-ups are generated with a 20% chance when the ball hits the paddle. 

Power-ups include:
```
[Rocket]: Fires a laser that destroys all balls in its path.
[Explosion]: Clears all balls on the screen.
[Double Ball]: Doubles the number of balls for 5 seconds.
[Slowdown]: Slows down the game speed by 50% for 10 seconds.
[Bouncewall]: Extends the paddle to cover the entire height of the screen for 10 seconds.
```

## Assets

Ensure you have the following assets in place:

Sounds: Place all sound files in the sound directory.

Textures: Textures are generated programmatically, but you can customize them in the script.

