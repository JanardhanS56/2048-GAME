# Advanced 2048

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-brightgreen.svg)](https://github.com/JanardhanS56/2048-GAME)

An enhanced Python GUI implementation of the classic **2048** puzzle game built with Tkinter. Features configurable board sizes, custom difficulty modifiers, obstacles, animated transitions, AI move hints, and session persistence.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements & Installation](#requirements--installation)
- [Usage](#usage)
- [Gameplay Controls](#gameplay-controls)
- [Game Modes & Mechanics](#game-modes--mechanics)
- [Achievements](#achievements)
- [Project Structure](#project-structure)
- [Author](#author)
- [License](#license)

## Overview

This project provides an interactive desktop implementation of 2048 with advanced gameplay variants and real-time statistics. Players merge matching numbered tiles to achieve the target tile (1024 on 3x3, 2048 on 4x4, 4096 on 5x5) while navigating challenges such as rock obstacles and tile-degrading zombies.

## Features

- 🎮 **Dynamic Grid Sizing**: Play on 3x3, 4x4, or 5x5 boards with scaled win targets.
- ✨ **Animated Tile Movement**: Smooth interpolated slide animations.
- 🌓 **Full-Window Dark & Light Theme**: Toggle complete dark mode with keyboard or checkbox.
- 🪨 **Rock Obstacles & Demolition**: Immovable rock tiles that can be crushed with adjacent merges >= 64.
- 🧟 **Zombie Mode**: A zombie degrades a random tile every 5 moves.
- 🌶️ **Hard Mode**: Exclusively spawns 4-tiles instead of 2-tiles.
- 🔥 **Heatmap Tracking**: Visual color heatmap highlighting high-traffic board cells.
- 💡 **AI Hint System**: Evaluates and suggests the move yielding the highest score gain.
- 📊 **Real-time Statistics**: Tracks moves, total merges, most merged tile, and merge streaks.
- 🏆 **High Score Table**: Saves top 5 scores with player initials, grid size, and active game modes.
- 💾 **Automatic State Persistence**: Prompts to resume ongoing games on startup.

## Requirements & Installation

### Prerequisites

- Python 3.7 or higher
- Tkinter (included by default in standard Python installations on Windows and macOS)

On Debian/Ubuntu Linux (if Tkinter is not pre-installed):
```bash
sudo apt-get install python3-tk
```

No external `pip` dependencies are required.

### Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/JanardhanS56/2048-GAME.git
cd 2048-GAME
```

2. Run the game:
```bash
python advanced_2048.py
```

## Usage

Run the main game file directly:

```bash
python advanced_2048.py
```

If an unfinished game exists from a previous session, you will be prompted to resume or start a new game.

## Gameplay Controls

| Key | Action |
|---|---|
| ⬆️ Arrow Up | Move tiles up |
| ⬇️ Arrow Down | Move tiles down |
| ⬅️ Arrow Left | Move tiles left |
| ➡️ Arrow Right | Move tiles right |
| `D` or `T` | Toggle Dark Mode |
| `H` | Toggle Hard Mode |
| `Z` | Toggle Zombie Mode |
| `R` | Toggle Rock Obstacles |
| `M` | Toggle Audio Mute |
| `C` | Refresh AI Hint |
| `Q` or `Esc` | Save game & quit |

## Game Modes & Mechanics

- **Grid Sizes**:
  - `3x3`: Target tile is 1024.
  - `4x4`: Target tile is 2048 (classic).
  - `5x5`: Target tile is 4096.
- **Rock Obstacles**: Spawns non-mergeable rocks (`-1`). When an adjacent merge produces a tile of `64` or higher, the shockwave destroys the rock.
- **Zombie Mode**: Every 5 moves, a random board tile is halved (2s are consumed).
- **Hard Mode**: Eliminates 2-tile spawns, spawning only 4-tiles.
- **Heatmap**: Displays warm-to-hot overlays on cells that frequently host tiles >= 32.
- **Combos**: Merging 2 or more tile pairs in a single move generates a bonus tile.

## Achievements

- 🏆 **First Merge**: Complete your first tile merge.
- 🏆 **Over 9000**: Reach a score exceeding 9,000 points.
- 🏆 **Snake**: Assemble tiles 4, 8, 16, 32, and 64 on the board simultaneously.
- 🏆 **Rock Crusher**: Destroy at least one rock obstacle with a 64+ merge.
- 🏆 **Pacifist**: Reach the win target with 10 or fewer 2-merges, or without crushing any rocks.

## Project Structure

```
2048-GAME/
├── .gitignore            # Git exclusion rules
├── README.md             # Project documentation
├── advanced_2048.py      # Main game executable and GUI logic
└── highscores.json       # Persistent top scores record
```

## Author

**Janardhan S**  
- GitHub: [@JanardhanS56](https://github.com/JanardhanS56)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
