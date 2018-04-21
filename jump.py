#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import random
from tkinter import*

'''declaration of class Ball, Obstacle and Background'''


class Ball:
    def __init__(self, canvas, obstacle):  # attributes of ball object
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 50, 50, fill='black', outline='black')
        self.canvas.move(self.id, 0, 350)
        self.y = 0
        self.canvas.bind_all('<Button-1>', self.jump)
        self.canvas_height = self.canvas.winfo_height()
        self.obstacle = obstacle

    def jump(self, event):  # function change ball's position
        if canvas_live is True:
            position = self.canvas.coords(self.id)
            if position[3] == self.canvas_height:
                self.y = -10

    def draw(self):  # draw ball at canvas
        self.canvas.move(self.id, 0, self.y)
        position = self.canvas.coords(self.id)
        if position[1] <= 0:
            self.y = 10
        if position[3] >= self.canvas_height:
            self.y = 0

    def hit(self):  # if ball hit obstacle return True
        position = self.canvas.coords(self.id)
        obstacle_position = self.canvas.coords(self.obstacle.id)
        if position[2] >= obstacle_position[0]:
            if position[3] >= obstacle_position[1]:
                return True
        return False


class Obstacle:
    def __init__(self, canvas, score):  # attributes of obstacle object
        self.canvas = canvas
        self.id = self.canvas.create_rectangle(0, 0, 25, 100, fill='black', outline='black')
        self.canvas.move(self.id, 400, 300)
        self.x = -4
        self.canvas_width = self.canvas.winfo_width()
        self.score = score

    def draw(self):  # draw obstacle at canvas
        self.canvas.move(self.id, self.x, 0)
        position = self.canvas.coords(self.id)
        colour_list = ['darkgreen', 'grey', 'red', 'blue', 'magenta', 'orange', 'yellow', 'green', 'black']
        colour = random.choice(colour_list)
        speed_list = 2*[-5, -4, -3, -2]+[-6]
        if position[2] <= 0:
            self.canvas.move(self.id, self.canvas_width, 0)
            self.canvas.itemconfig(self.id, fill=colour, outline=colour)
            self.x = random.choice(speed_list)
            self.score = self.score + 1


class Background:
    def __init__(self, canvas):  # attributes of background object
        self.canvas = canvas
        self.bg = PhotoImage(file='graphics\\background_800x400.png')
        self.bg_2 = PhotoImage(file='graphics\\background2_800x400.png')
        self.bg_id = self.canvas.create_image(0, 0, image=self.bg, anchor='nw')
        self.bg_2_id = self.canvas.create_image(800, 0, image=self.bg_2, anchor='nw')
        self.x = -2
        self.x_2 = -2

    def draw(self):  # draw background at canvas
        position = self.canvas.coords(self.bg_id)
        position_2 = self.canvas.coords(self.bg_2_id)
        if position[0] == -800:
            self.x = 1598
        else:
            self.x = -2
        if position_2[0] == -800:
            self.x_2 = 1598
        else:
            self.x_2 = -2
        self.canvas.move(self.bg_id, self.x, 0)
        self.canvas.move(self.bg_2_id, self.x_2, 0)

'''declaration of menu's function and game's mainloop'''


def game(event):
    global canvas, canvas_live  # declaration of game's canvas
    global break_loop, pause
    destroy_menu()
    break_loop = False
    pause = False
    canvas = Canvas(tk, width=400, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    canvas_live = True
    tk.update()

    background = Background(canvas)
    text1 = canvas.create_text(200, 130, text='', font=('Arial', 30))
    obstacle = Obstacle(canvas, 0)
    ball = Ball(canvas, obstacle)

    while 1:  # mainloop of game
        if ball.hit() is False:
            background.draw()
            obstacle.draw()
            ball.draw()
        else:
            break
        '''higher score - higher speed of game'''
        if obstacle.score == 10 or obstacle.score == 25 or obstacle.score == 50 or obstacle.score == 100:
            canvas.itemconfig(text1, text='ACCELERATION')
        else:
            canvas.itemconfig(text1, text=str(obstacle.score))
        tk.update()
        if obstacle.score >= 0 and obstacle.score < 10:
            time.sleep(0.016)
        elif obstacle.score >= 10 and obstacle.score < 25:
            time.sleep(0.014)
        elif obstacle.score >= 25 and obstacle.score < 50:
            time.sleep(0.012)
        elif obstacle.score >= 50 and obstacle.score < 100:
            time.sleep(0.010)
        else:
            time.sleep(0.008)

        while pause is True:
            if break_loop is True:
                break
            canvas.itemconfig(text1, text='PAUSE')
            tk.update()
            time.sleep(0.01)
        if break_loop is True:
            break

    while 1:  # end of game, write score if is high on scores' list
        if break_loop is True:
            break
        global player_name
        canvas_live = False
        scores_download = open('scores\\scores.txt', 'rt')
        scores_download.seek(0)
        scores_read = scores_download.read().split(',')
        copy_scores_read = scores_read.copy()
        scores_download.close()
        for i in [1, 3, 5]:
            if int(scores_read[i]) < obstacle.score:
                scores_read[i-1] = player_name
                scores_read[i] = str(obstacle.score)
                scores_read[i+1] = copy_scores_read[i-1]
                scores_read[i+2] = copy_scores_read[i]
                scores_read[i+3] = copy_scores_read[i+1]
                scores_read[i+4] = copy_scores_read[i+2]
                obstacle.score = 0
        scores_download = open('scores\\scores.txt', 'wt')
        scores_download.write(','.join(scores_read))
        scores_download.close()

        canvas_live = True
        canvas.itemconfig(text1, text='GAME OVER')
        tk.mainloop()
        if break_loop is True:
            break


def menu():  # open menu
    global canvas_live
    global button_start, button_exit, button_scores, button_help
    global label_1, label_2, label_3, label_4
    canvas_live = False
    button_start = Button(tk, text='START', font=('Arial', 24), background='white', relief='solid', width=10)
    button_exit = Button(tk, text='EXIT', font=('Arial', 24), background='white', relief='solid', width=10)
    button_scores = Button(tk, text='SCORES', font=('Arial', 24), background='white', relief='solid', width=10)
    button_help = Button(tk, text='HELP', font=('Arial', 24), background='white', relief='solid', width=10)
    label_1 = Label(tk, text='', font=('Arial', 15))
    label_2 = Label(tk, text='', font=('Arial', 15))
    label_3 = Label(tk, text='', font=('Arial', 15))
    label_4 = Label(tk, text='', font=('Arial', 15))
    button_start.bind('<Button-1>', game)
    button_exit.bind('<Button-1>', destroy_tk)
    button_scores.bind('<Button-1>', scores_list)
    button_help.bind('<Button-1>', help_key)
    label_1.pack()
    button_start.pack()
    label_2.pack()
    button_scores.pack()
    label_3.pack()
    button_help.pack()
    label_4.pack()
    button_exit.pack()
    tk.mainloop()


def scores_list(event):  # open scores' list
    global scores_live, scores_download
    global label_first, label_second, label_third
    destroy_menu()
    scores_download = open('scores\\scores.txt', 'rt')
    scores_read = scores_download.read().split(',')
    label_first = Label(tk, text=scores_read[0] + ': ' + scores_read[1], font=('Arial', 30), pady=40)
    label_first.pack()
    label_second = Label(tk, text=scores_read[2] + ': ' + scores_read[3], font=('Arial', 30), pady=40)
    label_second.pack()
    label_third = Label(tk, text=scores_read[4] + ': ' + scores_read[5], font=('Arial', 30), pady=40)
    label_third.pack()
    scores_live = True
    tk.mainloop()


def help_key(event):  # open help about keys
    global label_help
    global help_live
    destroy_menu()
    label_help = Label(tk, text='\n\nESC - BACK TO MENU\n\n\nSPACE - PAUSE\n\n\nLEFT MOUSE BUTTON - JUMP', font=('Arial', 20))
    label_help.pack()
    help_live = True
    tk.mainloop()


def destroy_tk(event):  # destroy tk = Tk() object
    tk.quit()
    tk.destroy()


def destroy_canvas(event):  # destroy canvas or scores or help
    global canvas_live
    global scores_live
    global help_live
    global break_loop
    break_loop = True
    if canvas_live is True:
        canvas.quit()
        canvas.destroy()
        canvas_live = False
        menu()
    elif scores_live is True:
        label_first.quit()
        label_second.quit()
        label_third.quit()
        label_first.destroy()
        label_second.destroy()
        label_third.destroy()
        scores_download.close()
        scores_live = False
        menu()
    elif help_live is True:
        label_help.quit()
        label_help.destroy()
        help_live = False
        menu()
    else:
        pass


def destroy_menu():  # it destroys menu buttons
    button_start.quit()
    button_exit.quit()
    button_scores.quit()
    button_help.quit()
    button_start.destroy()
    button_exit.destroy()
    button_scores.destroy()
    button_help.destroy()
    label_1.quit()
    label_2.quit()
    label_3.quit()
    label_4.quit()
    label_1.destroy()
    label_2.destroy()
    label_3.destroy()
    label_4.destroy()


def entry_get():  # remember player name
    global button, label, entry
    global player_name
    if len(entry.get()) > 0 and len(entry.get()) < 11:
        player_name = entry.get()
        button.quit()
        label.quit()
        entry.quit()
        button.destroy()
        label.destroy()
        entry.destroy()
        menu()
    else:
        pass


def pause_init(event):  # pause game
    global pause
    if pause is False:
        pause = True
    elif pause is True:
        pause = False

'''declaration of global variables and game's window'''


canvas_live = False  # canvas exist or not
break_loop = False  # break mainloop or not
scores_live = False  # scores exist or not
help_live = False  # help exist or not
pause = False  # if True game are paused

tk = Tk()  # declaration of game's window
tk.title('Jump through obstacles')
tk.resizable(0, 0)
tk.wm_attributes('-topmost', 1)
tk.geometry('400x400')
tk.bind_all('<Escape>', destroy_canvas)
tk.bind_all('<space>', pause_init)

label = Label(tk, text='ENTER YOUR NAME:', font=('Arial', 20))  # enter player name at the begining of game
entry = Entry(tk, relief='solid', font=('Arial', 20))
button = Button(tk, text='CONFIRM', font=('Arial', 20), command=entry_get)
label.place(x=10, y=50)
entry.place(x=10, y=100)
button.place(x=10, y=150)

tk.mainloop()
