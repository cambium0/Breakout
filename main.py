from turtle import *
from time import sleep
from random import randint, choice
from playsound import playsound
import os
from tkinter import messagebox

class Paddle(Turtle):

    paddle_motion = '', -1
    return_bounce = 180

    def __init__(self):
        super().__init__()
        self.color('#3333ff')
        self.shape('square')
        self.shapesize(0.5, 2.0)
        self.penup()
        self.setposition(0.00, -350.00)

    def move_right(self):
        if -361 < ball.ycor() < -320:
            self.paddle_motion = 'r', ball.heading()
        if self.xcor() < 295:
            self.goto(self.xcor() + 10, self.ycor())

    def move_left(self):
        if -361 < ball.ycor() < -320:
            self.paddle_motion = 'l', ball.heading()
        if self.xcor() > -295:
            self.goto(self.xcor() - 10, self.ycor())


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('circle')
        self.color('#bbbbbb')
        self.shapesize(0.5, 0.5)
        self.setposition(0.0, 0.0)

    def bounce_ball(self, direction):
        if direction == 'top' or direction == 'block':
            new_heading = 360 - self.heading()
        elif direction == 'paddle_left' or direction == 'paddle_right':
            if direction == 'paddle_left':
                if paddle.paddle_motion[0] == 'l':
                    if 180 < self.heading() < 270:
                        new_heading = 360 - self.heading() - 10
                    elif 270 <= self.heading() < 360:
                        new_heading = self.heading() - 190
                elif paddle.paddle_motion[0] == 'r':
                    if 180 < self.heading() <= 270:
                        new_heading = 360 - self.heading() - 10
                    elif 270 < self.heading() < 360:
                        new_heading = self.heading() - 170
                elif paddle.paddle_motion[0] == '':
                    if 180 < self.heading() <= 270:
                        new_heading = 360 - self.heading()
                    elif 270 < self.heading() < 360:
                        new_heading = self.heading() - 180
            if direction == 'paddle_right':
                if paddle.paddle_motion[0] == 'l':
                    if 180 < self.heading() < 270:
                        new_heading = self.heading() - 190
                    elif 270 <= self.heading() < 360:
                        new_heading = 360 - self.heading() - 10
                elif paddle.paddle_motion[0] == 'r':
                    if 180 < self.heading() <= 270:
                        new_heading = self.heading() - 170
                    elif 270 < self.heading() < 360:
                        new_heading = 360 - self.heading() + 10
                elif paddle.paddle_motion[0] == '':
                    if 180 < self.heading() <= 270:
                        new_heading = self.heading() - 180
                    elif 270 < self.heading() < 360:
                        new_heading = 360 - self.heading()
                paddle.paddle_motion = '', -1  # clears is_moving which relates to paddle hits
        elif direction == 'east':
            if self.heading() == 0:
                new_heading = randint(-30, 30)
            if 0 < self.heading() <= 90:
                new_heading = 180 - self.heading()
            elif 359 >= self.heading() > 270:
                new_heading = 540 - self.heading()
        elif direction == 'west':
            if self.heading() == 180:
                new_heading = randint((140, 210))
            elif 90 < self.heading() < 180:
                new_heading = 180 - self.heading()
            elif 180 < self.heading() <= 270:
                new_heading = 540 - self.heading()
        elif direction == 'bottom':
            print("You missed the ball--you lose a guy!!")
            self.bounce_ball('top')
            return
        try:
            self.setheading(new_heading)
        except UnboundLocalError:
            pass

class Block(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape('square')
        self.shapesize(0.6, 2)


player_1 = '000'
player_2 = '000'
game_on = True
num_games = 1
r_balls_used = 1


def draw_screen():
    drawer = Turtle()
    drawer.shape('square')
    drawer.color('#ccccdc')
    drawer.penup()
    drawer.goto(-310.00, 455.00)
    drawer.pensize(7)
    drawer.right(90)
    drawer.pendown()
    drawer.forward(900)
    drawer.penup()
    drawer.goto(306.00, 455.00)
    drawer.pendown()
    drawer.forward(900)
    drawer.penup()
    drawer.goto(-304, 350.00)
    drawer.pensize(25)
    drawer.left(90)
    drawer.pendown()
    drawer.forward(620)
    drawer.penup()


def set_blocks():
    colors = ['red', 'orange', 'green', 'yellow']
    block_start_x = -332
    block_start_y = 250
    for pigment in colors:
        for m in range(0, 2):
            for i in range(1, 15):
                block = Block()
                block.color(pigment)
                block.goto(block_start_x + i*44, block_start_y)
                blocks.append(block)
            block_start_y -= 17


def ball_loc(side):
    # halving these values form 20->10, 10->5 since they are based on a 21x21 turtle, I shapesized this ball to 11x11
    if side == "right":
        return ball.xcor() + 10, ball.ycor() - 5
    elif side == "left":
        return ball.xcor(), ball.ycor() - 5
    elif side == "top":
        return ball.xcor() + 5, ball.ycor()
    elif side == "bottom":
        return ball.xcor() + 5, ball.ycor() - 10


def game_status(condition):
    ball_num = 0
    global pauser, game_on, high_score
    if condition == 'lose_ball' or condition == 'board_cleared':
        ball.hideturtle()
        ball.goto(0, 0)
        ball.setheading(randint(230, 310))
        ball_num = int(cv.itemcget(right_balls, 'text'))
        if condition == 'lose_ball':
            ball_num += 1
        if ball_num == 4 or condition == 'board_cleared':
            total_games = int(cv.itemcget(game_num, 'text'))
            if total_games == 2 or ball_num == 4:
                this_score = int(cv.itemcget(left_score, 'text'))
                cv.itemconfig(game_over, text="GAME OVER")
                if this_score > int(high_score):
                    with open('high_score.txt', 'w') as f:
                        f.write(str(this_score))
                    high_score = this_score
                if total_games == 2:
                    messagebox.showinfo("You win!", "Congratulations! You won the game!")
                if ball_num == 4:
                    cv.itemconfig(right_balls, text="4")
                game_on = False
                return
            else:
                messagebox.showinfo("Screen Completed!", f"Well done! You must complete a second screen to win. You have {ball_num} balls remaining.")
                cv.itemconfig(game_num, text="2")
                for block in blocks:
                    block.showturtle()
                cv.itemconfig(left_score, text="000")
        cv.itemconfig(right_balls, text=str(ball_num))
        paddle.goto(0, -350)
        pauser = 6


def check_blocks():
    global left_score, destroyed_blocks, pauser
    for block in blocks:
        if block.isvisible():
            if block.distance(ball.xcor(), ball.ycor()) < 21:
                # playsound(choice(sounds))
                os.system('beep -f 2000 -l 1500')
                current_score = int(cv.itemcget(left_score, 'text'))
                current_score += color_points[block.pencolor()]
                if block.pencolor() == 'red':
                    pauser = 0
                block.hideturtle()
                destroyed_blocks += 1
                if destroyed_blocks == 112:
                    game_status('board_cleared')
                    return
                cv.itemconfig(left_score, text=str(current_score))
                ball.bounce_ball('block')



color_points = {'yellow': 1, 'green': 3, 'orange': 4, 'red': 7}
blocks = []
destroyed_blocks = 0
ball = Ball()
ball.setheading(randint(200, 340))
paddle = Paddle()
brick_coords = {"bottoms": [123, 140, 157, 174, 191, 208, 225, 242], "tops": [257, 240, 223, 206, 189, 172, 155, 138],
                 "lefts": [-309, -265, -221, -177, -133, -89, -45, -1, 43, 87, 131, 175, 219, 263, 307, 351],
                 "rights": [-267, -223, -179, -135, -92, -47, -3, 41, 85, 129, 173, 217, 261, 305, 349, 393]}
sounds = ['coin-upaif-14631.mp3', 'blip-131856.mp3', 'jump_c_02-102843.mp3']
high_score = 0
with open('high_score.txt') as f:
    high_score = f.read()
screen = Screen()
screen.setup(width=630, height=900)
screen.onkeypress(paddle.move_left, "Left")
screen.onkeypress(paddle.move_right, "Right")
screen.title("BreakOut!")
screen.bgcolor("#000000")
cv = screen.getcanvas()
highscore_display = cv.create_text(0, -400, text=f"High Score: {high_score}", font=('Arial', 22, 'bold'), fill="red")
game_num = cv.create_text(-290, -315, text=f"{num_games}", font=('courier', 32, 'bold'), fill='#ccccdc')
right_balls = cv.create_text(78, -315, text=f"{r_balls_used}", font=('courier', 32, 'bold'), fill='#ccccdc')
left_score = cv.create_text(-248, -280, text=f"{player_1}", font=('courier', 28, 'bold'), fill='white')
right_score = cv.create_text(117, -280, text=f"{player_2}", font=('courier', 28, 'bold'), fill='white')
game_over = cv.create_text(0, 0, text=f"", font=('Arial', 36, 'bold'), fill='yellow')
screen.tracer(1, 0)
screen.listen()
draw_screen()
set_blocks()
pauser = 0.001


while game_on:
    screen.update()
    ball.forward(1)
    pauser = 0
    ball.showturtle()
    # detect top collision
    if ball_loc("top")[1] >= 440:
        ball.bounce_ball('top')
    # detect bottom collision
    if ball_loc("bottom")[1] <= -445:
        game_status('lose_ball')
        # ball.bounce_ball('bottom')
    # detect right side collision
    if ball_loc('right')[0] >= 308:
        ball.bounce_ball('east')
    # detect left side collision
    if ball_loc('left')[0] <= -308:
        ball.bounce_ball('west')
    # detect paddle impact
    if -347 < ball.ycor() <= -340:
        if (paddle.xcor() - 20) <= ball.xcor() < paddle.xcor():
            ball.bounce_ball('paddle_left')
        elif (paddle.xcor() + 20) > ball.xcor() >= paddle.xcor():
            ball.bounce_ball('paddle_right')
    # detect brick impact
    if 120 < ball.ycor() <= 260:
        check_blocks()
    sleep(pauser)


screen.exitonclick()
