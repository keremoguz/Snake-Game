import tkinter as tk
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 150
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#0000FF"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"



class Snake:
     def __init__(self):
         self.body_size= BODY_PARTS
         self.coordinates = []
         self.squares = []

         for i in range(0,BODY_PARTS):
             self.coordinates.append([0,0]) #initially starts from top-left
         
         for x, y in self.coordinates:
             
             square = canvas.create_rectangle(x, y, x +SPACE_SIZE,y + SPACE_SIZE,fill= SNAKE_COLOR,tag = "snake") #represents the coordinates of snake as rectangle boxes by filling it with its color
             self.squares.append(square) # stores the squares

class Food:
    
    def __init__(self):
        # spot amount: width/space_size,height/space_size
        x = random.randint(0,(GAME_WIDTH/SPACE_SIZE-1))*SPACE_SIZE #random x coordinate for food
        y = random.randint(0,(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE #random y coordinate for food
        self.coordinates = [x,y]

        canvas.create_oval(x,y,x+SPACE_SIZE,y + SPACE_SIZE, fill=FOOD_COLOR, tag = "food")

def next_turn(snake, food):
    """
    changes coordinates of the head of the snake , 
    fills the screen with the  the changed coordinates,
    deletes the rearmost part if the head didn't encounter
    to food and displays at SPEED speed. When head encounters with
    a border program terminates with game over func.
    """
    global SPEED
    global direction
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score
        
        score += 1
        SPEED -= 3 # snake gets faster when it eats snake

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]
    
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_direction):
    """
    changes directions if it is opposite to the current direction
    it isn't executed in order to prevent conflicts(180 degree turn)
    """
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction

    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction

    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    

    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    
def check_collisions(snake):
    """
    if head of the snake collapses with borders or 
    itself return true specifies that collusion has occured
    """
    x, y = snake.coordinates[0]

    if x< 0 or x>= GAME_WIDTH:
         return True
    elif y<0 or y >= GAME_HEIGHT:
        return True
    
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False
def game_over():
    """
    deletes board and inform user that game is ended.
    """
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,font=('consolas',70),text = "GAME IS OVER", fill = "red",tag = "gg")

window = tk.Tk()
window.title("Snake Game")
window.resizable(False,False)


score = 0
direction = 'down'


label = tk.Label(window, text= "Info: Snake gets faster as the score increases. Score:{}".format(score),font = ('consolas',30)) #creates a box at the top to show score
label.pack()

canvas = tk.Canvas(window, bg = BACKGROUND_COLOR, height=GAME_HEIGHT,width=GAME_WIDTH) # creates a game screen with its respective features
canvas.pack()

window.update() # to center the board 
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) -(window_width/2))
y = int((screen_height/2)-(window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# matches keybord controls with the function change direction to move snake
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
next_turn(snake,food)

window.mainloop()