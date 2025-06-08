# OpenAI Roo Code: Offline Pygame Tic-Tac-Toe (Human vs. Local Python AI)

This project uses a Python virtual environment for dependency management.

**Game Mode:**  
Fully offline — the human player competes against a locally implemented Python algorithm.  
_No online or API components are used._

---

## Setup and Gameplay Instructions

### 1. Project Overview

This is an offline Tic-Tac-Toe game built with Pygame. You play as a human against a local Python AI agent. The game does not require any internet connection or external APIs; all logic and AI are implemented locally.

### 2. Setting Up the Python Virtual Environment

**Windows:**
```sh
python -m venv venv
venv\Scripts\activate
```

**Unix/macOS/Linux:**
```sh
python3 -m venv venv
source venv/bin/activate
```

### 3. Installing Dependencies

After activating the virtual environment, install the required dependencies:
```sh
pip install -r requirements.txt
```

### 4. Running the Game

From the `openai_roo_code` directory (with the virtual environment activated), run:
```sh
python main.py
```

### 5. Gameplay Instructions

- **Controls:** Use your mouse to click on an empty cell to place your mark (X or O).
- **Turn Order:** The game alternates turns between the human player and the AI.
- **Resetting:** After a game ends (win, lose, or draw), click anywhere on the board to reset and start a new game.
- **Winning:** The first player to align three of their marks horizontally, vertically, or diagonally wins. If all cells are filled without a winner, the game ends in a draw.

### 6. Offline and Local AI

This game is fully offline. The AI opponent is implemented in Python and runs locally on your machine. No data is sent or received over the internet.