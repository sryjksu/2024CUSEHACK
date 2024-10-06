from tkinter import *
import tkinter.messagebox
import numpy as np


root = Tk()
root.title("Wuziqi Game")
background = Canvas(root, width=600, height=600, background='chocolate')
background.pack()

for current_x in range(0, 15):
    background.create_line(current_x * 40 + 20, 20, current_x * 40 + 20, 580)
    background.create_line(20, current_x * 40 + 20, 580, current_x * 40 + 20)
background.create_oval(135, 135, 145, 145,fill='black')
background.create_oval(295, 135, 305, 145,fill='black')
background.create_oval(135, 295, 145, 305,fill='black')
background.create_oval(135, 455, 145, 465,fill='black')
background.create_oval(465, 135, 455, 145,fill='black')
background.create_oval(455, 455, 465, 465,fill='black')
background.create_oval(295, 295, 305, 305,fill='black')
background.create_oval(455, 295, 465, 305,fill='black')
background.create_oval(295, 455, 305, 465,fill='black')

step=0
Placed=np.full((15,15),0)
Board=np.full((15,15),'')
game_finished = False
move_history = []

def reset():
    global step, Placed, Board, game_finished, move_history, background
    step=0
    Placed=np.full((15,15),0)
    Board=np.full((15,15),'')
    game_finished = False
    move_history = []

    background.create_rectangle(0, 0, 600, 600, fill='chocolate', outline='chocolate')
    for current_x in range(0, 15):
        background.create_line(current_x * 40 + 20, 20, current_x * 40 + 20, 580)
        background.create_line(20, current_x * 40 + 20, 580, current_x * 40 + 20)
    background.create_oval(135, 135, 145, 145,fill='black')
    background.create_oval(295, 135, 305, 145,fill='black')
    background.create_oval(135, 295, 145, 305,fill='black')
    background.create_oval(135, 455, 145, 465,fill='black')
    background.create_oval(465, 135, 455, 145,fill='black')
    background.create_oval(455, 455, 465, 465,fill='black')
    background.create_oval(295, 295, 305, 305,fill='black')
    background.create_oval(455, 295, 465, 305,fill='black')
    background.create_oval(295, 455, 305, 465,fill='black')

def place_a_piece(event):
    global step, Placed, Board, game_finished, move_history
    if game_finished:
        return
    for current_y in range (0,15):
        for current_x in range (0,15):
            if (event.x - 20 - 40 * current_x) ** 2 + (event.y - 20 - 40 * current_y) ** 2 <= 2 * 10 ** 2:
                break
        if (event.x - 20 - 40 * current_x) ** 2 + (event.y - 20 - 40 * current_y) ** 2 <= 2 * 10 ** 2:
            break
    if (event.x - 20 - 40 * current_x) ** 2 + (event.y - 20 - 40 * current_y) ** 2 > 2 * 10 ** 2:
        return

    if step % 2 == 0 and Placed[current_x][current_y] != 1:
        background.create_oval(40*current_x+5, 40*current_y+5, 40*current_x+35, 40*current_y+35,fill='black')
        Placed[current_x][current_y] = 1
        Board[current_x][current_y] = 'b'
        step += 1
        move_history.append((current_x, current_y, 'b'))

    if step % 2 != 0 and Placed[current_x][current_y] != 1 :
        background.create_oval(40*current_x+5, 40*current_y+5, 40*current_x+35, 40*current_y+35,fill='white')
        Placed[current_x][current_y] = 1.
        Board[current_x][current_y] = 'w'
        step += 1
        move_history.append((current_x, current_y, 'w'))

    f = [[-1, 0], [-1, 1], [0, 1], [1, 1]]
    for z in range(0, 4):
        a, b = f[z][0], f[z][1]
        count1, count2 = 0, 0
        x, y = current_x, current_y

        while Board[x][y] == Board[current_x][current_y]:
            count1 += 1
            if x + a >= 0 and y + b >= 0 and x + a < 15 and y + b < 15 and Board[x + a][y + b] == Board[current_x][current_y]:
                [x, y] = np.array([x, y]) + np.array([a, b])
            else:
                x, y = current_x, current_y
                break

        while Board[x][y] == Board[current_x][current_y]:
            count2 += 1
            if x - a < 15 and y - b < 15 and x - a >= 0 and y - b >= 0 and Board[x - a][y - b] == Board[current_x][current_y]:
                [x, y] = np.array([x, y]) - np.array([a, b])
            else:
                break

        if count1 + count2 >= 6:
            game_finished = True
            if Board[current_x][current_y] == 'b':
                tkinter.messagebox.showinfo('', 'Black wins!')
            else:
                tkinter.messagebox.showinfo('', 'White wins!')

def regret(event):
    global step, Placed, Board, move_history
    if move_history:
        current_x, current_y, color = move_history.pop()
        Placed[current_x][current_y] = 0
        Board[current_x][current_y] = ''
        step -= 1

        # Redraw the grid over the piece to clear it visually
        background.create_rectangle(40 * current_x + 1, 40 * current_y + 1, 40 * current_x + 39, 40 * current_y + 39, fill='chocolate', outline='chocolate')
        background.create_line(current_x * 40 + 20, current_y * 40, current_x * 40 + 20, current_y * 40 + 40)
        background.create_line(40 * current_x, current_y * 40 + 20, 40 * current_x + 40, current_y * 40 + 20)

background.bind("<Button -1>", place_a_piece)
root.bind("<space>", regret)
background.pack()

def quit():
    root.quit()

reset_button=Button(root, text="Reset", width=10, height=1, command=reset, font=('Times New Roman',15))
reset_button.pack()
quit_button=Button(root, text="Quit", width=10, height=1, command=quit, font=('Times New Roman',15))
quit_button.pack()

mainloop()