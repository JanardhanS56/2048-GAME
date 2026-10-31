# 2048 Game

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)](https://github.com/JanardhanS56/2048-GAME)

A Python implementation of the popular **2048** puzzle game, created as a college assignment project. This project demonstrates core programming concepts including game logic, data structures, and user interaction handling.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Gameplay Controls](#gameplay-controls)
- [Author](#author)
- [License](#license)

## Overview

This is a fully functional implementation of the classic 2048 puzzle game. Players combine numbered tiles to reach the 2048 tile and beyond. The game features a responsive board, score tracking, and game-over detection. This project serves as an educational demonstration of game development fundamentals in Python.

## Features

- 🎮 **Interactive 4x4 Game Board** - Classic 2048 gameplay mechanics
- 🏆 **Score Tracking** - Real-time score updates and high score management
- 🎯 **Win/Lose Detection** - Automatic game state management
- ⌨️ **Keyboard Controls** - Smooth and responsive arrow key controls
- 🔄 **Random Tile Generation** - Proper implementation of tile spawning mechanics
- 🎨 **Clean User Interface** - Easy-to-understand game board display
- 📊 **Game Statistics** - Track your progress and performance

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/JanardhanS56/2048-GAME.git
cd 2048-GAME
```

2. Install required dependencies (if any):
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python game.py
```

## Usage

Simply run the main game file and follow the on-screen instructions:

```bash
python game.py
```

The game will start with a new 4x4 board with two initial tiles. Use the controls to move and combine tiles.

## Game Rules

- **Objective**: Combine tiles to create a 2048 tile and reach the highest possible score
- **Movement**: Move tiles in four directions (up, down, left, right)
- **Combination**: When two tiles with the same number touch, they merge into one tile with their sum
- **New Tiles**: After each move, a new tile (either 2 or 4) appears randomly on an empty square
- **Game Over**: The game ends when no more moves are possible
- **Win Condition**: Reaching the 2048 tile (optional: continue playing for a higher score)

## Project Structure

```
2048-GAME/
├── README.md                 # Project documentation
├── game.py                   # Main game implementation
├── requirements.txt          # Python dependencies
└── [other project files]     # Additional project files
```

## Technologies Used

- **Language**: Python 3.7+
- **Concepts**: Object-Oriented Programming, Data Structures, Game Logic
- **Focus Areas**: 
  - Algorithm implementation
  - State management
  - User input handling
  - Data structure manipulation

## Gameplay Controls

| Key | Action |
|-----|--------|
| ⬆️ Arrow Up | Move tiles up |
| ⬇️ Arrow Down | Move tiles down |
| ⬅️ Arrow Left | Move tiles left |
| ➡️ Arrow Right | Move tiles right |
| `Q` / `ESC` | Quit game |

## How to Play

1. Start the game - you'll see a board with two random tiles
2. Use arrow keys to move all tiles in a direction
3. When two tiles with the same number collide, they merge into one
4. A new tile appears after each move
5. Keep combining tiles to reach 2048
6. The game ends when the board is full and no moves are possible
7. Try to achieve the highest score possible!

## Learning Outcomes

This project demonstrates proficiency in:
- Game development basics
- Python programming fundamentals
- Algorithmic problem-solving
- User interface design (console-based)
- State management and game logic

## Future Enhancements

Potential improvements for future versions:
- [ ] GUI implementation using Tkinter or Pygame
- [ ] Undo functionality
- [ ] Multiple difficulty levels
- [ ] Sound and animations
- [ ] Online leaderboard
- [ ] Mobile app version

## Author

**Janardhan S**  
- GitHub: [@JanardhanS56](https://github.com/JanardhanS56)
- Created: May 2026

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Note**: This project was created as part of a college assignment to demonstrate programming fundamentals and game development concepts.
