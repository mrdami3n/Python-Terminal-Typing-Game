# Typing Boss Game
A fast-paced, terminal-based typing game written in Python. Face off against 25 unique ASCII art bosses, defeat them by typing words correctly, and see how high you can score before you run out of lives!

## Features
Real-Time Countdown: A live timer keeps the pressure on!

25 Unique Bosses: Each level features a new, hand-crafted ASCII art boss with a unique name.

Progressive Difficulty: Words get longer and more complex as you advance through the levels.

Live Score and Stats: A clean HUD keeps you updated on your level, score, lives, and progress.

Cross-Platform: Works on Windows, macOS, and Linux terminals.

Highly Customizable: Easily change game parameters, bosses, and word lists directly in the code.

## How to Play
Prerequisites: You need to have Python 3 installed on your system.

Download: Save the typing_game.py script to your computer.

Open a Terminal:

Windows: Open Command Prompt or PowerShell.

macOS/Linux: Open your Terminal application.

Navigate to the File: Use the cd command to go to the directory where you saved the file.

`cd path/to/your/folder`

Run the Game: Execute the script using Python.

`python typing_game.py`

Follow the on-screen instructions and start typing!

## Customizing the Game
You can easily tweak the game's mechanics and content by editing the configuration variables at the top of the typing_game.py file.

### Game Mechanics
To change the core rules, modify these variables:

```
--- Game Configuration ---
TOTAL_LEVELS = 25       # Change the total number of levels
STARTING_LIVES = 3        # Set the number of lives the player starts with
TIME_PER_LEVEL = 60       # Set the time limit (in seconds) for each level
WORDS_PER_BOSS = 10     # The number of words required to defeat a boss
POINTS_PER_BOSS = 100   # Points awarded for defeating a boss
```

### Bosses
You can edit, replace, or add new bosses by modifying the BOSSES list. Each boss is a tuple containing its name (a string) and its ASCII art (a multi-line string).

```
--- ASCII Art for Bosses ---
BOSSES = [
    ("Slime Blob", """
      .--.
      / oo \\
     | |  | |
      \\ -- /
       `--'
    """),
    # ... more bosses here ...
    ("Your New Boss", """
    +-------+
    | (o_o) |
    +-------+
    """)
 ]
```

Word Lists
The words for each difficulty level are stored in the WORDS dictionary. You can add, remove, or change any of the words in the lists.
