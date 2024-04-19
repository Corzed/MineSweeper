# Pygame Minesweeper :bomb:

Welcome to the GitHub repository for a classic Minesweeper game implemented in Python using the Pygame library. Designed to run on a 10x10 board with 15 hidden mines, this project is perfect for those looking to brush up on their puzzle-solving skills or delve into game development with Pygame.

## :sparkles: Features

- **Customizable Board Size**: Easily modify the board size and number of mines by changing the constants.
- **Colorful UI**: The game features a simple yet attractive user interface with distinct colors for each cell state.
- **Interactive Gameplay**: Players can open cells, flag mines, and use chords to reveal areas of the board, increasing interaction and complexity.

## :hammer_and_wrench: Installation

To get started with this Minesweeper game, follow these steps:

1. Ensure that Python and Pygame are installed on your machine. If not, you can download Python from [python.org](https://www.python.org/) and install Pygame via pip:

   ```bash
   pip install pygame
   ```

2. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/pygame-minesweeper.git
   ```

3. Navigate to the cloned repository:

   ```bash
   cd pygame-minesweeper
   ```

4. Run the game:

   ```bash
   python minesweeper.py
   ```

## :video_game: How to Play

- **Left Click** on a cell to open it.
- **Right Click** on a cell to flag it or unflag it.
- **Middle Click** on an opened cell to use the chord action, which opens adjacent cells if the number of flags around it matches the number of adjacent mines.

The game ends when all non-mine cells are opened or a mine is triggered.

## :open_file_folder: Project Structure

The project files are structured as follows:

- `minesweeper.py`: Contains the main game logic, Pygame window setup, and event handling.

## :handshake: Contributing

Contributions to the Minesweeper project are welcome! Here are some ways you can contribute:

- Submit bugs and feature requests.
- Review code and improve code quality.
- Add new features or enhancements.

Before contributing, please review the CONTRIBUTING.md file for guidelines on how to make a pull request and propose feature changes.

