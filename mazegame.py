import turtle
import pygame
from PIL import Image, ImageDraw
import random
pygame.init()

VictorySound=pygame.mixer.Sound("Victory.wav")
LostSound=pygame.mixer.Sound("Lost.wav")
GoldSound=pygame.mixer.Sound("Gold.wav")
MovementSound=pygame.mixer.Sound("Movement.wav")
music=pygame.mixer.music.load("Retro Theme.wav")

MovementSound.set_volume(0.05)
VictorySound.set_volume(0.05)
LostSound.set_volume(0.05)
GoldSound.set_volume(0.05)
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1) #-1 plays continuously.

window=turtle.Screen() #Generates Screen.
window.bgcolor('black') #Background color.
window.title('Maze Game')
window.setup(625,625) #Size of the screen.
window.tracer(0) #To make the game go faster.

#Creating a wall gif:-
#Create a 24x24 pixel image with a transparent background:
image=Image.new("RGBA", (24, 24), (210, 180, 140, 255)) 
#Create a drawing object
draw=ImageDraw.Draw(image)
#Color of the square:
square_color=(210, 180, 140, 255) 
#Draw the 24x24 square:
draw.rectangle([0, 0, 23, 23], fill=square_color) 
#Save the image as a GIF:
image.save("wall.gif", format="GIF")

#Register shapes:
turtle.register_shape("PS.gif")
turtle.register_shape("PR.gif")
turtle.register_shape("PL.gif")
turtle.register_shape("GR.gif")
turtle.register_shape("GL.gif")
turtle.register_shape("wall.gif")

#Create a maze:
class Maze(turtle.Turtle): #Maze is a child class of the turtle class, so maze class can do everything the turtle class can do.
    def __init__(self):
        turtle.Turtle.__init__(self) #Initializing the turtle class, every instance is going to be a square and white.
        self.shape("square")
        self.color("white")
        self.penup() #Turtle graphics leave a trail if the pen is down, so we keep it up.
        self.speed(0) #Fastest speed of animation.

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("PS.gif")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.gold=0 #Player has zero gold at the start.
    
    def go_up(self): #These are turtle's commands.
        if not is_paused:
            move_to_x=player.xcor()
            move_to_y=player.ycor()+24

            MovementSound.play()

            self.shape("PS.gif")
            
            #Check if the space has a wall:
            if (move_to_x,move_to_y) not in walls:
                self.goto(move_to_x,move_to_y)
    
    def go_down(self):
        if not is_paused:
            move_to_x=player.xcor()
            move_to_y=player.ycor()-24

            MovementSound.play()

            self.shape("PS.gif")
            
            #Check if the space has a wall:
            if (move_to_x,move_to_y) not in walls:
                self.goto(move_to_x,move_to_y)
        
    def go_left(self):
        if not is_paused:
            move_to_x=player.xcor()-24
            move_to_y=player.ycor()

            MovementSound.play()
            
            #Calling the shape method:
            self.shape("PL.gif")
            
            #Check if the space has a wall:
            if (move_to_x,move_to_y) not in walls:
                self.goto(move_to_x,move_to_y)
    
    def go_right(self):
        if not is_paused:
            move_to_x=player.xcor()+24
            move_to_y=player.ycor()

            MovementSound.play()

            self.shape("PR.gif")
            
            #Check if the space has a wall:
            if (move_to_x,move_to_y) not in walls:
                self.goto(move_to_x,move_to_y)
    
    def is_collision(self,other): #Self is the player.
        import math
        a=self.xcor()-other.xcor() 
        b=self.ycor()-other.ycor()
        distance=math.sqrt((a**2) + (b**2))

        if distance<5:
            return True 
        else:
            return False
            

class Treasure(turtle.Turtle):
    def __init__(self,x,y): #This is where we want the treasure to appear.
        turtle.Turtle.__init__(self) #Initializing both child and parent classes.
        self.shape("circle")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold=1
        self.goto(x,y) #Sending the gold to the x and y coordinates.
    
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle() #Removing it off the screen.
        
class VictoryGem(turtle.Turtle):
    def __init__(self,x,y): #This is where we want the treasure to appear.
        turtle.Turtle.__init__(self) #Initializing both child and parent classes.
        self.shape("square")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(x,y) #Sending the gold to the x and y coordinates.
    
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle() #Removing it off the screen.

class Score(turtle.Turtle):
    
    def __init__(self):
        #Keeping scores:
        self.player_score=0
        self.high_score=self.get_high_score()
        #Displaying scores:
        self.score_display=turtle.Turtle()
        self.score_display.speed(0)
        self.score_display.color("white")
        self.score_display.penup()
        self.score_display.hideturtle()
        self.score_display.goto(180, 280)
        self.score_display.write(f"Player Score:", align="center", font=("Courier", 16, "normal"))
        self.update_score()
        
        #Displaying high scores:
        self.high_score_display=turtle.Turtle()
        self.high_score_display.speed(0)
        self.high_score_display.color("white")
        self.high_score_display.penup()
        self.high_score_display.hideturtle()
        self.high_score_display.goto(193, 260)
        self.high_score_display.write(f"High Score:", align="center", font=("Courier", 16, "normal"))
        self.update_high_score() 
    
    def get_high_score(self):
        file=open("High Score File.txt",'r')
        high_score=file.readline()
        file.close()
        return int(high_score)
        
    def increment_score(self,value):
        #Incrementing the score and calling the update method:
        self.player_score+=value

        if self.player_score>self.high_score:
            self.high_score=self.player_score
            self.save_high_score()

        self.update_score()
        self.update_high_score()
    
    def update_score(self):
        #Clear the previous score and write the updated score on the window or the score text will overlap:
        self.score_display.clear()
        self.score_display.write(f"Player Score:{self.player_score}",align="center",font=("Courier", 16, "normal"))
       
    def update_high_score(self):
        self.high_score_display.clear()
        self.high_score_display.write(f"High Score:{self.high_score}",align="center",font=("Courier", 16, "normal"))

    def save_high_score(self):
        file=open("High Score File.txt",'w')
        file.write(str(self.high_score))
        file.close()

class Enemy(turtle.Turtle):
    def __init__(self,x,y):
        turtle.Turtle.__init__(self)
        self.shape("GL.gif")
        self.color("red")
        self.penup()
        self.speed(0)
        self.gold=25
        self.goto(x,y)
        self.direction=random.choice(["up","down","left","right"])
    
    def move(self):
        if not is_paused:
            if self.direction=="up":
                dx=0 #Delta is d which means change.
                dy=24
            elif self.direction=="down":
                dx=0
                dy=-24
            elif self.direction=="left":
                dx=-24
                dy=0
                self.shape("GL.gif")
            elif self.direction=="right":
                dx=24
                dy=0
                self.shape("GR.gif")
            else:
                dx=0
        
            #Calculate the spot to move to:
            move_to_x=self.xcor() + dx
            move_to_y=self.ycor() + dy

            #Check if the space has a wall:
            if (move_to_x,move_to_y) not in walls:
                self.goto(move_to_x,move_to_y)
            
            else:
                #Select a different direction:
                self.direction=random.choice(["up","down","left","right"])
            
        #Set timer to move next time:
        if not game.is_game_over:
            turtle.ontimer(self.move, t=random.randint(100, 300))
    
    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

class Game:
    def __init__(self):
        self.is_game_over=False
        #Displaying the game over message:
        self.game_over_display=turtle.Turtle()
        self.game_over_display.hideturtle()
        self.game_over_display.penup()
        self.game_over_display.color("white")
        
        #Displaying the victory message:
        self.victory_display=turtle.Turtle()
        self.victory_display.hideturtle()
        self.victory_display.penup()
        self.victory_display.color("white")
    
    def victory(self):
        self.victory_display.goto(0,0)
        self.victory_display.write("You Won!", align="center", font=("Courier", 40, "bold"))
        
        #Display restart and quit options:
        self.game_over_display.goto(0,-40)
        self.game_over_display.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Courier", 20, "bold"))

        #Set the flag to indicate game over:
        self.is_game_over=True
        
        #Disable movement keys:
        window.onkey(None,"Left")
        window.onkey(None,"Right")
        window.onkey(None,"Up")
        window.onkey(None,"Down")
        
        #Pause the music:
        pygame.mixer.music.pause()

        #Binding restart and quit options but not calling the methods:
        window.onkey(self.restart_game,"r")
        window.onkey(self.quit_game,"q")
    
    def game_over(self):
        self.game_over_display.goto(0,0)
        self.game_over_display.write("Game over!", align="center", font=("Courier", 40, "bold"))
        
        #Display restart and quit options:
        self.game_over_display.goto(0,-40)
        self.game_over_display.write("Press 'R' to Restart or 'Q' to Quit", align="center", font=("Courier", 20, "bold"))
        
        #Set the flag to indicate game over:
        self.is_game_over=True
        
        #Disable movement keys:
        window.onkey(None,"Left")
        window.onkey(None,"Right")
        window.onkey(None,"Up")
        window.onkey(None,"Down")
        
        #Pause the music:
        pygame.mixer.music.pause()
        
        #Binding restart and quit options but not calling the methods:
        window.onkey(self.restart_game,"r")
        window.onkey(self.quit_game,"q")

    def restart_game(self):
        if not self.is_game_over: #Check the game isn't over.
            return #Do not restart if the game is still ongoing.
        
        #Clear pause message if the game was paused:
        pause_display.clear()

        #Clear the restart and quit message:
        self.game_over_display.clear()

        #Clear the win message:
        self.victory_display.clear()

        #Reset game variables and clear the screen:
        player.goto(-288, 288) #Reset player position.
        player.shape("PS.gif") #Reset shape.
        player.gold = 0
        score.player_score = 0
        score.update_score()

        #Clear any remaining enemies and treasures:
        for enemy in enemies:
            enemy.destroy()
        for treasure in treasures:
            treasure.destroy()

        treasures.clear()
        enemies.clear()
        walls.clear()
        
        #Set up the maze level again:
        setup_maze(mazes_list[1])

        #Re-enable the movement keys:
        window.onkey(player.go_left, "Left")
        window.onkey(player.go_right, "Right")
        window.onkey(player.go_up, "Up")
        window.onkey(player.go_down, "Down")

        #Restart the enemy movements:
        for enemy in enemies:
            turtle.ontimer(enemy.move, t=250)
        
        #Reset the game over flag:
        self.is_game_over=False
        
        #Clear once again:
        pause_display.clear()
        self.game_over_display.clear()
        self.victory_display.clear()
        
        #Unpause the music:
        pygame.mixer.music.unpause()

    def quit_game(self):
           window.bye()  
           pygame.quit()

mazes_list=[""] #Levels list.

level_1=[ #X to represent wall and space to represent path.
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

#Add mazes to the maze list:
mazes_list.append(level_1)

#Create level setup function:
def setup_maze(level):
    for y in range(len(level)): #For rows.
        for x in range(len(level[y])): #This inputs the rows starting from row zero.
            
            #Get the character at each x,y coordinate:
            #Note the order of y and x in the next line:
            character=level[y][x]
            
            #Calculate the x,y coordinates of the screen:-
            #Top left block:-288,288.
            #Top right block:288,288.
            #Bottom left block:-288,-288.
            #Bottom right block:288,-288.
            screen_x= -288 + (x*24) 
            screen_y= 288 - (y*24)

            #Check if it is an X representing a wall:
            if character=="X":
                maze.goto(screen_x,screen_y)
                maze.shape("wall.gif")
                maze.stamp() #Puts it on the screen.
                
                #Add coordinates to wall list:
                walls.append((screen_x,screen_y))

            if character=='P':
                player.goto(screen_x,screen_y)

            if character=='T':
                treasures.append(Treasure(screen_x,screen_y)) #Location is initialized in the treasure class.

            if character=='E':
               enemies.append(Enemy(screen_x,screen_y))
            
            if character=='G':
                victory_gem.append(VictoryGem(screen_x,screen_y))

#Create class instances:
maze=Maze()
player=Player()
score=Score()
game=Game()

#Create wall list to store the coordinates of the wall blocks:
walls=[]

#Create a treasure list:
treasures=[]

#Create enemies list:
enemies=[]

#Victory gem:
victory_gem=[]

#Set up the level:
setup_maze(mazes_list[1])

#Keyboard Binding:-
#We need to tell turtle to follow the commands:
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")

#Start moving enemies:
for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

#Pausing the game:
pause_display = turtle.Turtle()
pause_display.hideturtle()
pause_display.penup()
pause_display.color("white")
is_paused=False

def toggle_pause():
    global is_paused
    if is_paused==True:
        is_paused=False
        pause_display.clear()
        pygame.mixer.music.unpause()
    else:
        is_paused=True
        pause_display.goto(0,0)
        pause_display.write("Paused", align="center", font=("Courier", 40, "bold"))
        pygame.mixer.music.pause()

window.listen()
window.onkeypress(toggle_pause,"p")

#Main:
while True:
    if not is_paused:
        #Check for player collision with treasure iterating through the treasure list:
        for treasure in treasures:
            if player.is_collision(treasure):

                GoldSound.play()
                
                #Add the treasure gold to the player gold:
                player.gold+=treasure.gold
                
                #Update the score using the Score class:
                score.increment_score(treasure.gold)

                #Destroy the treasure:
                treasure.destroy()
                #Remove the treasure from the treasure list:
                treasures.remove(treasure)
    
        #Iterate through the enemy list to see if the player collided:
        for enemy in enemies:
            if player.is_collision(enemy):
                
                game.game_over()
                LostSound.play()
                break
        
        for gem in victory_gem:
            if player.is_collision(gem):
                gem.destroy()
                game.victory()
                VictorySound.play()
                break
    
    #Update screen:
    window.update()


    