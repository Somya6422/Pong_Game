# Pong Game - AI Edition

## Overview
Pong Game - AI Edition is a desktop arcade game built with Python and Pygame. The project includes:

- Single Player mode against an AI opponent
- Local Multiplayer mode
- Custom winning score selection
- Interactive menu system
- Score tracking and winner screen
- Smooth paddle and ball movement

## Features

### Single Player
Play against a computer-controlled paddle that tracks the ball and reacts in real time.

### Local Multiplayer
Two players can compete on the same keyboard.

### Custom Winning Score
Players can choose the target score before starting a match.

### Controls

#### Player 1
- W → Move Up
- S → Move Down

#### Player 2
- Up Arrow → Move Up
- Down Arrow → Move Down

#### General
- ESC → Quit current game/application

## Technologies Used

- Python
- Pygame

## Installation

1. Clone the repository
2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the game

```bash
python "Pong Game.py"
```

## Build Executable

Example using PyInstaller:

```bash
pyinstaller --onefile --windowed "Pong Game.py"
```

The executable will be generated inside the `dist` folder.

## GitHub Release Download Button

After creating a GitHub Release and uploading the executable:

```markdown
[![Download](https://img.shields.io/badge/Download-Windows%20Executable-blue?style=for-the-badge)](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/releases/latest)
```

Replace:
- YOUR_USERNAME
- YOUR_REPOSITORY

with your actual GitHub information.

## Project Structure

```
.
├── Pong Game.py
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Notes

This project is intended as a beginner-friendly demonstration of game development using Python and Pygame.
