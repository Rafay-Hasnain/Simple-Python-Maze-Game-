"""Maze Game: a tile-based maze game built with Python's turtle library.

Why turtle: it is part of Python's standard library (no install needed) and
gives a window, shapes, keyboard input and timers in very little code. This
makes it a good fit for learning game basics (drawing, movement, collisions,
game loop) without a full game engine. pygame is used here only for sound.
"""

import math  # Maths tools, used for the distance formula
import os  # Used to check whether the high score file exists
import random  # Lets enemies pick random directions
import turtle  # Window, shapes, keyboard and timers

import pygame  # Plays the sounds and music
from PIL import Image, ImageDraw  # Draws the wall image

pygame.init()  # Start pygame's sound system

# Sound effects are short clips loaded fully into memory
VictorySound = pygame.mixer.Sound("Victory.wav")  # Load the win sound
LostSound = pygame.mixer.Sound("Lost.wav")  # Load the lose sound
GoldSound = pygame.mixer.Sound("Gold.wav")  # Load the treasure sound
MovementSound = pygame.mixer.Sound("Movement.wav")  # Load the footstep sound
music = pygame.mixer.music.load("Retro Theme.wav")  # Streams from disk; load() returns None, so "music" is unused

MovementSound.set_volume(0.05)  # Volume goes from 0.0 (silent) to 1.0 (full)
VictorySound.set_volume(0.05)  # Same low volume for the win sound
LostSound.set_volume(0.05)  # Same low volume for the lose sound
GoldSound.set_volume(0.05)  # Same low volume for the treasure sound
pygame.mixer.music.set_volume(0.05)  # Music volume (was 0.01, which was too quiet to hear)
pygame.mixer.music.play(-1)  # -1 plays continuously

window = turtle.Screen()  # Generates Screen
window.bgcolor('black')  # Background color
window.title('Maze Game')  # Text shown in the window's title bar
window.setup(625, 625)  # Size of the screen
window.tracer(0)  # To make the game go faster

# Creating a wall gif:-
# Create a 24x24 pixel image with a transparent background:
image = Image.new("RGBA", (24, 24), (210, 180, 140, 255))  # Tan 24x24 image (RGBA = red, green, blue, opacity)
# Create a drawing object
draw = ImageDraw.Draw(image)  # Lets us draw shapes on the image
# Color of the square:
square_color = (210, 180, 140, 255)  # Same tan color as the image
# Draw the 24x24 square:
draw.rectangle([0, 0, 23, 23], fill=square_color)  # Fill the whole 24x24 area
# Save the image as a GIF:
image.save("wall.gif", format="GIF")  # GIF is a format turtle can use as a shape

# Register shapes:
turtle.register_shape("PS.gif")  # Player facing front
turtle.register_shape("PR.gif")  # Player facing right
turtle.register_shape("PL.gif")  # Player facing left
turtle.register_shape("GR.gif")  # Enemy facing right
turtle.register_shape("GL.gif")  # Enemy facing left
turtle.register_shape("wall.gif")  # Wall block


# Create a maze:
class Maze(turtle.Turtle):  # Maze is a child class of the turtle class, so maze class can do everything the turtle class can do
    """Stamps the wall blocks onto the screen."""
    def __init__(self):
        """Set up the stamper: square shape, no trail, fastest speed."""
        turtle.Turtle.__init__(self)  # Initializing the turtle class, every instance is going to be a square and white
        self.shape("square")  # Default shape
        self.color("white")  # Default color
        self.penup()  # Turtle graphics leave a trail if the pen is down, so we keep it up
        self.speed(0)  # Fastest speed of animation


class Player(turtle.Turtle):
    """The character the player controls."""
    def __init__(self):
        """Create the player facing front with zero gold."""
        turtle.Turtle.__init__(self)  # Set up the turtle part of the player
        self.shape("PS.gif")  # Start facing front
        self.color("blue")  # Fallback color
        self.penup()  # No drawing trail
        self.speed(0)  # No move animation
        self.gold = 0  # Player has zero gold at the start

    def go_up(self):  # These are turtle's commands
        """Move one tile up unless a wall is in the way."""
        if not is_paused:  # Ignore keys while paused
            move_to_x = player.xcor()  # Stay in the same column
            move_to_y = player.ycor() + 24  # One tile up

            MovementSound.play()  # Footstep sound

            self.shape("PS.gif")  # Face front

            # Check if the space has a wall:
            if (move_to_x, move_to_y) not in walls:  # Only move if the tile is not a wall
                self.goto(move_to_x, move_to_y)  # Move only if it's free

    def go_down(self):
        """Move one tile down unless a wall is in the way."""
        if not is_paused:  # Ignore keys while paused
            move_to_x = player.xcor()  # Stay in the same column
            move_to_y = player.ycor() - 24  # One tile down

            MovementSound.play()  # Footstep sound

            self.shape("PS.gif")  # Face front

            # Check if the space has a wall:
            if (move_to_x, move_to_y) not in walls:  # Only move if the tile is not a wall
                self.goto(move_to_x, move_to_y)  # Move only if it's free

    def go_left(self):
        """Move one tile left unless a wall is in the way."""
        if not is_paused:  # Ignore keys while paused
            move_to_x = player.xcor() - 24  # One tile left
            move_to_y = player.ycor()  # Stay in the same row

            MovementSound.play()  # Footstep sound

            # Calling the shape method:
            self.shape("PL.gif")  # Face left

            # Check if the space has a wall:
            if (move_to_x, move_to_y) not in walls:  # Only move if the tile is not a wall
                self.goto(move_to_x, move_to_y)  # Move only if it's free

    def go_right(self):
        """Move one tile right unless a wall is in the way."""
        if not is_paused:  # Ignore keys while paused
            move_to_x = player.xcor() + 24  # One tile right
            move_to_y = player.ycor()  # Stay in the same row

            MovementSound.play()  # Footstep sound

            self.shape("PR.gif")  # Face right

            # Check if the space has a wall:
            if (move_to_x, move_to_y) not in walls:  # Only move if the tile is not a wall
                self.goto(move_to_x, move_to_y)  # Move only if it's free

    def is_collision(self, other):  # Self is the player
        """Return True if the player is touching `other`."""
        a = self.xcor() - other.xcor()  # Horizontal gap
        b = self.ycor() - other.ycor()  # Vertical gap
        distance = math.sqrt((a ** 2) + (b ** 2))  # Straight-line distance (Pythagoras)

        if distance < 5:  # Closer than 5 pixels counts as touching
            return True  # They are touching
        else:  # Otherwise
            return False  # They are not touching


class Treasure(turtle.Turtle):
    """A coin worth one point."""
    def __init__(self, x, y):  # This is where we want the treasure to appear
        """Create a coin at the given x, y position."""
        turtle.Turtle.__init__(self)  # Initializing both child and parent classes
        self.shape("circle")  # Round coin
        self.color("gold")  # Gold color
        self.penup()  # No drawing trail
        self.speed(0)  # No move animation
        self.gold = 1  # Worth 1 point
        self.goto(x, y)  # Sending the gold to the x and y coordinates

    def destroy(self):
        """Remove the coin from the screen."""
        self.goto(2000, 2000)  # Move far off-screen
        self.hideturtle()  # Removing it off the screen


class VictoryGem(turtle.Turtle):
    """The green gem that wins the game when touched."""
    def __init__(self, x, y):  # This is where we want the treasure to appear
        """Create the gem at the given x, y position."""
        turtle.Turtle.__init__(self)  # Initializing both child and parent classes
        self.shape("square")  # Square gem
        self.color("green")  # Green so it stands out
        self.penup()  # No drawing trail
        self.speed(0)  # No move animation
        self.goto(x, y)  # Sending the gold to the x and y coordinates

    def destroy(self):
        """Remove the gem from the screen."""
        self.goto(2000, 2000)  # Move far off-screen
        self.hideturtle()  # Removing it off the screen


class Score(turtle.Turtle):
    """Tracks, shows and saves the score and the high score."""

    def __init__(self):
        """Load the high score and draw both score labels."""
        # Keeping scores:
        self.player_score = 0  # Score starts at zero
        self.high_score = self.get_high_score()  # Load the saved best score
        # Displaying scores:
        self.score_display = turtle.Turtle()  # Separate turtle for score text
        self.score_display.speed(0)  # No animation
        self.score_display.color("white")  # White text
        self.score_display.penup()  # No drawing trail
        self.score_display.hideturtle()  # Hide the arrow, show only text
        self.score_display.goto(180, 280)  # Top-right area
        self.score_display.write(f"Player Score:", align="center", font=("Courier", 16, "normal"))  # Draw the label
        self.update_score()  # Show the starting score

        # Displaying high scores:
        self.high_score_display = turtle.Turtle()  # Separate turtle for high score text
        self.high_score_display.speed(0)  # No animation
        self.high_score_display.color("white")  # White text
        self.high_score_display.penup()  # No drawing trail
        self.high_score_display.hideturtle()  # Hide the arrow, show only text
        self.high_score_display.goto(193, 260)  # Just below the score
        self.high_score_display.write(f"High Score:", align="center", font=("Courier", 16, "normal"))  # Draw the label
        self.update_high_score()  # Show the saved high score

    def get_high_score(self):
        """Read the saved high score, creating the file if needed."""
        # Create the file with a score of 0 if it is missing (for example after
        # cloning the repo), otherwise open() below would crash
        if not os.path.exists("High Score File.txt"):  # Is the file missing?
            file = open("High Score File.txt", 'w')  # 'w' creates the file
            file.write("0")  # Starting high score
            file.close()  # Save and close

        file = open("High Score File.txt", 'r')  # Open for reading
        high_score = file.readline()  # Read the first line (text)
        file.close()  # Close the file
        return int(high_score)  # Convert the text to a number

    def increment_score(self, value):
        """Add points and save a new high score if it is beaten."""
        # Incrementing the score and calling the update method:
        self.player_score += value  # Add the points

        if self.player_score > self.high_score:  # New record?
            self.high_score = self.player_score  # Remember it
            self.save_high_score()  # Write it to the file

        self.update_score()  # Redraw the score
        self.update_high_score()  # Redraw the high score

    def update_score(self):
        """Redraw the current score."""
        # Clear the previous score and write the updated score on the window or the score text will overlap:
        self.score_display.clear()  # Erase the old text
        self.score_display.write(f"Player Score:{self.player_score}", align="center", font=("Courier", 16, "normal"))  # Draw the new score

    def update_high_score(self):
        """Redraw the high score."""
        self.high_score_display.clear()  # Erase the old text
        self.high_score_display.write(f"High Score:{self.high_score}", align="center", font=("Courier", 16, "normal"))  # Draw the new high score

    def save_high_score(self):
        """Write the high score to the file."""
        file = open("High Score File.txt", 'w')  # Open for writing (replaces old content)
        file.write(str(self.high_score))  # Files store text, so convert the number
        file.close()  # Save and close


class Enemy(turtle.Turtle):
    """A roaming enemy that walks randomly; touching it ends the game."""
    def __init__(self, x, y):
        """Create an enemy at the given x, y position."""
        turtle.Turtle.__init__(self)  # Set up the turtle part of the enemy
        self.shape("GL.gif")  # Start facing left
        self.color("red")  # Fallback color
        self.penup()  # No drawing trail
        self.speed(0)  # No move animation
        self.gold = 25  # Not used anywhere in the game right now
        self.goto(x, y)  # Place the enemy at its starting tile
        self.direction = random.choice(["up", "down", "left", "right"])  # Pick a random first direction

    def move(self):
        """Take one step in the current direction, then schedule the next step."""
        if not is_paused:  # Enemies freeze while paused
            if self.direction == "up":  # Choose the step size from the direction
                dx = 0  # Delta is d which means change
                dy = 24  # One tile up
            elif self.direction == "down":  # Moving down
                dx = 0  # No sideways movement
                dy = -24  # One tile down
            elif self.direction == "left":  # Moving left
                dx = -24  # One tile left
                dy = 0  # No vertical movement
                self.shape("GL.gif")  # Face left
            elif self.direction == "right":  # Moving right
                dx = 24  # One tile right
                dy = 0  # No vertical movement
                self.shape("GR.gif")  # Face right
            else:  # Fallback that should never be reached
                dx = 0  # No horizontal change

            # Calculate the spot to move to:
            move_to_x = self.xcor() + dx  # Target column
            move_to_y = self.ycor() + dy  # Target row

            # Check if the space has a wall:
            if (move_to_x, move_to_y) not in walls:  # Only step if the tile is not a wall
                self.goto(move_to_x, move_to_y)  # Free tile, so step into it

            else:  # A wall is in the way
                # Select a different direction:
                self.direction = random.choice(["up", "down", "left", "right"])  # Hit a wall, so pick again

        # Set timer to move next time:
        if not game.is_game_over:  # Stop scheduling once the game ends
            turtle.ontimer(self.move, t=random.randint(100, 300))  # Call move again in 0.1-0.3 seconds

    def destroy(self):
        """Remove the enemy from the screen."""
        self.goto(2000, 2000)  # Move far off-screen
        self.hideturtle()  # Hide it


class Game:
    """Holds the game state and the win, lose, restart and quit logic."""
    def __init__(self):
        """Start in the playing state and prepare the message displays."""
        self.is_game_over = False  # Game starts in the playing state
        # Displaying the game over message:
        self.game_over_display = turtle.Turtle()  # Turtle used for the game over text
        self.game_over_display.hideturtle()  # Hide the arrow, show only text
        self.game_over_display.penup()  # No drawing trail
        self.game_over_display.color("white")  # White text

        # Displaying the victory message:
        self.victory_display = turtle.Turtle()  # Turtle used for the win text
        self.victory_display.hideturtle()  # Hide the arrow, show only text
        self.victory_display.penup()  # No drawing trail
        self.victory_display.color("white")  # White text

    def victory(self):
        """Show the win screen and stop the game."""
        self.victory_display.goto(0, 0)  # Center of the screen
        self.victory_display.write("You Won!", align="center", font=("Courier", 40, "bold"))  # Show the win message

        # Display restart and quit options:
        self.game_over_display.goto(0, -40)  # Just below the win message
        self.game_over_display.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Courier", 20, "bold"))  # Show the options

        # Set the flag to indicate game over:
        self.is_game_over = True  # Stops enemies and collision checks

        # Disable movement keys:
        window.onkey(None, "Left")  # Unbind left arrow
        window.onkey(None, "Right")  # Unbind right arrow
        window.onkey(None, "Up")  # Unbind up arrow
        window.onkey(None, "Down")  # Unbind down arrow

        # Pause the music:
        pygame.mixer.music.pause()  # Silence the music

        # Binding restart and quit options but not calling the methods:
        window.onkey(self.restart_game, "r")  # R restarts
        window.onkey(self.quit_game, "q")  # Q quits

    def game_over(self):
        """Show the lose screen and stop the game."""
        self.game_over_display.goto(0, 0)  # Center of the screen
        self.game_over_display.write("Game over!", align="center", font=("Courier", 40, "bold"))  # Show the lose message

        # Display restart and quit options:
        self.game_over_display.goto(0, -40)  # Just below the lose message
        self.game_over_display.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Courier", 20, "bold"))  # Show the options

        # Set the flag to indicate game over:
        self.is_game_over = True  # Stops enemies and collision checks

        # Disable movement keys:
        window.onkey(None, "Left")  # Unbind left arrow
        window.onkey(None, "Right")  # Unbind right arrow
        window.onkey(None, "Up")  # Unbind up arrow
        window.onkey(None, "Down")  # Unbind down arrow

        # Pause the music:
        pygame.mixer.music.pause()  # Silence the music

        # Binding restart and quit options but not calling the methods:
        window.onkey(self.restart_game, "r")  # R restarts
        window.onkey(self.quit_game, "q")  # Q quits

    def restart_game(self):
        """Reset everything and start a new round."""
        if not self.is_game_over:  # Check the game isn't over
            return  # Do not restart if the game is still ongoing

        # Clear pause message if the game was paused:
        pause_display.clear()  # Erase "Paused" text

        # Clear the restart and quit message:
        self.game_over_display.clear()  # Erase the game over text

        # Clear the win message:
        self.victory_display.clear()  # Erase the win text

        # Reset game variables and clear the screen:
        player.goto(-288, 288)  # Reset player position
        player.shape("PS.gif")  # Reset shape
        player.gold = 0  # Reset gold
        score.player_score = 0  # Reset score
        score.update_score()  # Redraw the score

        # Clear any remaining enemies and treasures:
        for enemy in enemies:  # Go through every enemy
            enemy.destroy()  # Remove it from the screen
        for treasure in treasures:  # Go through every treasure
            treasure.destroy()  # Remove it from the screen

        treasures.clear()  # Empty the treasure list
        enemies.clear()  # Empty the enemy list
        walls.clear()  # Empty the wall list

        # Set up the maze level again:
        setup_maze(mazes_list[1])  # Rebuild level 1

        # Re-enable the movement keys:
        window.onkey(player.go_left, "Left")  # Rebind left arrow
        window.onkey(player.go_right, "Right")  # Rebind right arrow
        window.onkey(player.go_up, "Up")  # Rebind up arrow
        window.onkey(player.go_down, "Down")  # Rebind down arrow

        # Restart the enemy movements:
        for enemy in enemies:  # Go through the new enemies
            turtle.ontimer(enemy.move, t=250)  # Start each one's movement timer

        # Reset the game over flag:
        self.is_game_over = False  # Back to the playing state

        # Clear once again:
        pause_display.clear()  # Make sure no text is left
        self.game_over_display.clear()  # Erase the game over text
        self.victory_display.clear()  # Erase the win text

        # Unpause the music:
        pygame.mixer.music.unpause()  # Music plays again

    def quit_game(self):
        """Ask the main loop to stop."""
        # Only stop the main loop here. Destroying the window directly would
        # crash the loop's next window.update(); the window is closed after the loop ends.
        global running  # Edit the global flag, not a local copy
        running = False  # Tells the main loop to stop


mazes_list = [""]  # Levels list

level_1 = [  # X to represent wall and space to represent path
    "XXXXXXXXXXXXXXXX        ",
    "XP    XT    X  X        ",
    "X   XXE  XXX X XXXXXXXXX",
    "X     X      X  X  XT  X",
    "X  XXX  XXXT    XE XXX X",
    "X    X  X    X   XT    X",
    "X  XXXX    XE   XE XXX X",
    "X  XT  X  X    XT   X  X",
    "X  XX   X X    X  XXXE X",
    "X  X    XT   X   X  X  X",
    "X  XE XXX  XE  XX    X X",
    "X  X     X  X  XE   X  X",
    "X    X  X  XXX   XT  X X",
    "X  XXE   X    X   XX   X",
    "X  XXX  XT  XE  X   X  X",
    "X  X     X  X    X  TX X",
    "X  XXXXT   X   XE    X X",
    "X  XT   X    X  X   XX X",
    "X  X     XT XXE   X    X",
    "X  X   X  X    XX   X EX",
    "X   XE    XE   X   XE  X",
    "X  XXXX  XX  XT  X    GX",
    "XXXXXXXXXXXXXXXXXXXXXXXX",
]

# Add mazes to the maze list:
mazes_list.append(level_1)  # Level 1 is at index 1


# Create level setup function:
def setup_maze(level):
    """Build the level from text: walls, player, treasures, enemies, gem."""
    for y in range(len(level)):  # For rows
        for x in range(len(level[y])):  # This inputs the rows starting from row zero

            # Get the character at each x,y coordinate:
            # Note the order of y and x in the next line:
            character = level[y][x]  # Row first, then column

            # Calculate the x,y coordinates of the screen:-
            # Top left block:-288,288
            # Top right block:288,288
            # Bottom left block:-288,-288
            # Bottom right block:288,-288
            screen_x = -288 + (x * 24)  # Each tile is 24 pixels wide
            screen_y = 288 - (y * 24)  # Screen y goes up, rows go down

            # Check if it is an X representing a wall:
            if character == "X":  # X means wall
                maze.goto(screen_x, screen_y)  # Move the stamper here
                maze.shape("wall.gif")  # Use the wall image
                maze.stamp()  # Puts it on the screen

                # Add coordinates to wall list:
                walls.append((screen_x, screen_y))  # Remember it so nobody walks through

            if character == 'P':  # P means player start
                player.goto(screen_x, screen_y)  # Put the player at the start

            if character == 'T':  # T means treasure
                treasures.append(Treasure(screen_x, screen_y))  # Location is initialized in the treasure class

            if character == 'E':  # E means enemy
                enemies.append(Enemy(screen_x, screen_y))  # Create an enemy here

            if character == 'G':  # G means victory gem
                victory_gem.append(VictoryGem(screen_x, screen_y))  # Create the win gem here


# Create class instances:
maze = Maze()  # The wall stamper
player = Player()  # The player
score = Score()  # The score keeper
game = Game()  # The game state

# Create wall list to store the coordinates of the wall blocks:
walls = []  # Coordinates of every wall tile

# Create a treasure list:
treasures = []  # Every treasure still on the map

# Create enemies list:
enemies = []  # Every enemy in the game

# Victory gem:
victory_gem = []  # The win gem (a list so it uses the same checks)

# Set up the level:
setup_maze(mazes_list[1])  # Build level 1

# Keyboard Binding:-
# We need to tell turtle to follow the commands:
turtle.listen()  # Start listening for key presses
turtle.onkey(player.go_left, "Left")  # Left arrow moves left
turtle.onkey(player.go_right, "Right")  # Right arrow moves right
turtle.onkey(player.go_up, "Up")  # Up arrow moves up
turtle.onkey(player.go_down, "Down")  # Down arrow moves down

# Start moving enemies:
for enemy in enemies:  # Go through every enemy
    turtle.ontimer(enemy.move, t=250)  # Start its movement timer

# Pausing the game:
pause_display = turtle.Turtle()  # Turtle used for the "Paused" text
pause_display.hideturtle()  # Hide the arrow, show only text
pause_display.penup()  # No drawing trail
pause_display.color("white")  # White text
is_paused = False  # Game starts unpaused
# Controls the main loop; quit_game() sets it to False so the loop can exit cleanly
running = True  # The main loop keeps going while this is True


def toggle_pause():
    """Pause or resume the game and the music."""
    global is_paused  # Change the global variable, not a local copy
    if is_paused == True:  # Currently paused, so resume
        is_paused = False  # Resume
        pause_display.clear()  # Remove "Paused" text
        pygame.mixer.music.unpause()  # Music plays again
    else:  # Not paused, so pause
        is_paused = True  # Pause
        pause_display.goto(0, 0)  # Center of the screen
        pause_display.write("Paused", align="center", font=("Courier", 40, "bold"))  # Show "Paused"
        pygame.mixer.music.pause()  # Silence the music


window.listen()  # Make sure the window receives key presses
window.onkeypress(toggle_pause, "p")  # P toggles pause

# Main:
while running:  # Game loop: runs until the player quits
    # Skip collision checks once the game is over, otherwise the lost sound
    # restarts on every pass of the loop
    if not is_paused and not game.is_game_over:  # Only check collisions during active play
        # Check for player collision with treasure iterating through the treasure list:
        for treasure in treasures:  # Check every treasure
            if player.is_collision(treasure):  # Player touched this treasure

                GoldSound.play()  # Coin sound

                # Add the treasure gold to the player gold:
                player.gold += treasure.gold  # Add its value to the player's gold

                # Update the score using the Score class:
                score.increment_score(treasure.gold)  # Add points and update the high score

                # Destroy the treasure:
                treasure.destroy()  # Hide it off-screen
                # Remove the treasure from the treasure list:
                treasures.remove(treasure)  # Forget it so it can't be collected twice

        # Iterate through the enemy list to see if the player collided:
        for enemy in enemies:  # Check every enemy
            if player.is_collision(enemy):  # Player touched an enemy

                game.game_over()  # Show the lose screen
                LostSound.play()  # Lose sound
                break  # No need to check other enemies

        for gem in victory_gem:  # Check the win gem
            if player.is_collision(gem):  # Player reached the gem
                gem.destroy()  # Remove the gem
                game.victory()  # Show the win screen
                VictorySound.play()  # Win sound
                break  # Stop checking

    # Update screen:
    window.update()  # Redraw the screen (tracer is off, so we do it ourselves)

# Runs once the loop has ended: shut down the sound system, then close the window
pygame.quit()  # Shut down the sound system
window.bye()  # Close the game window