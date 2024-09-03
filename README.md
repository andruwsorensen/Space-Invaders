# Space Invaders

A classic Space Invaders game implemented in Python using the Pygame library.

## Description

This Space Invaders game is a modern take on the classic arcade game. Players control a spaceship at the bottom of the screen, shooting at alien invaders while dodging their attacks. The game features multiple rounds with increasing difficulty, a scoring system, and lives for the player.

## Features

- Player-controlled spaceship with left and right movement
- Multiple enemy ships with random movement and shooting patterns
- Increasing difficulty with each round
- Scoring system
- Lives system for the player
- Start menu and game over screen with play again option
- Collision detection using hitboxes

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Ensure you have Python installed on your system.
2. Install Pygame by running:
   ```
   pip install pygame
   ```
3. Clone this repository or download the source code.

## How to Play

1. Run the `main.py` file:
   ```
   python main.py
   ```
2. Use the left and right arrow keys to move your spaceship.
3. Press the spacebar to shoot at the enemy ships.
4. Avoid enemy bullets and prevent the aliens from reaching the bottom of the screen.
5. Clear all enemies to advance to the next round.

## Game Controls

- Left Arrow: Move left
- Right Arrow: Move right
- Spacebar: Shoot

## Game Elements

- Player Ship: Controlled by the player, can move left and right and shoot bullets.
- Enemy Ships: Move across and down the screen, shooting at the player.
- Bullets: Both player and enemies can shoot bullets.
- Rounds: The game progresses through rounds, with each round spawning more enemies.
- Lives: The player starts with 3 lives and loses one when hit by an enemy bullet.
- Score: Players earn points for destroying enemy ships.

## Code Structure

The game is structured into several classes:

- `Player`: Represents the player's spaceship.
- `Enemy`: Represents an enemy ship.
- `Bullet`: Represents bullets shot by the player.
- `EnemyBullet`: Represents bullets shot by enemies.
- `Button`: Used for UI elements in menus.

The main game loop is contained in the `game()` function, while `start_menu()` and `game_over_menu()` handle the respective screens.

## Customization

You can customize various aspects of the game by modifying constants and values in the code:

- Screen size: Modify `width` and `height` variables.
- Game speed: Adjust the `FPS` constant.
- Player and enemy attributes: Modify values in their respective class initializations.
- Difficulty scaling: Adjust the enemy spawning and speed increase in the `spawn_enemies()` function.

## Assets

The game uses custom images for the player ship, enemy ships, and bullets. Ensure all image files are in the correct directories as specified in the code.

## Contributing

Feel free to fork this project and submit pull requests with improvements or bug fixes.
