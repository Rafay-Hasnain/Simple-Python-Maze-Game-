# Maze Game

A little maze game I built in Python. You walk through the maze, grab treasure, dodge the enemies wandering around, and try to reach the green gem at the end.

This was one of my first proper programming projects. I came back to it later to fix its bugs, clean up the code and finally share it.

## What's in the game

- A maze drawn from a simple text map, so changing the level is as easy as editing some letters
- Treasure to collect, which raises your score
- Enemies that wander around randomly. Touch one and it's game over
- A green gem at the end of the maze. Reach it and you win
- A high score that is saved, so it is still there next time you play
- Background music and sound effects
- Pause, restart and quit

## Controls

- **Arrow keys**: move around the maze
- **P**: pause or resume
- **R**: restart (after you win or lose)
- **Q**: quit (after you win or lose)

## How to run it

1. Install Python 3 from [python.org](https://www.python.org/downloads/) if you don't have it.
2. Clone this repository and open the folder:
   ```
   git clone https://github.com/Rafay-Hasnain/Python-Maze-Game.git
   cd Python-Maze-Game
   ```
3. Install the two packages the game needs:
   ```
   pip install -r requirements.txt
   ```
4. Start the game:
   ```
   python mazegame.py
   ```

A couple of things to know:
- Run the game from inside the project folder. It loads its images and sounds from there, so it won't find them otherwise.
- On some Linux systems you may also need to install Tkinter, which `turtle` depends on: `sudo apt install python3-tk`.

## What's in the folder

- **mazegame.py**: the whole game lives here
- **The .gif files**: the player, enemy and wall images
- **The .wav files**: the background music and sound effects
- **High Score File.txt**: where your best score is saved. The game creates it for you if it's missing
- **requirements.txt**: the Python packages the game needs

## How it works

- **turtle** draws the window and the characters, and handles key presses and timers. I picked it because it comes with Python and is a simple way to learn how games work.
- **pygame** is only used for the music and sound effects.
- **Pillow** creates the wall image when the game starts.
- The game is built from a few classes: `Player`, `Enemy`, `Treasure`, `VictoryGem`, `Score` and `Game`. The level itself is just a list of text rows.
- A main loop keeps running and checks whether the player has touched treasure, an enemy or the gem.

## What I learned

- How to organise a program with classes, and how inheritance works (every character builds on `turtle.Turtle`)
- How collision detection works, using the distance between two objects
- How a game loop runs, and how simple flags like `running` and `is_game_over` control it
- How to read and write files to save a high score
- How to track down real bugs. Fixing this project meant dealing with music that was too quiet to hear, a sound that replayed on every pass of the loop, an error when quitting, and a crash when the high score file was missing

## What could be better

- There is only one level
- Enemies wander randomly instead of chasing you
- Ideas for later: more levels, lives, a start menu and smarter enemies
