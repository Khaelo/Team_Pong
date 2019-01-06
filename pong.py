from tkinter import *
import random

root = Tk()
root.title("Team Pong !")
root.resizable(0, 0)

BASE = PhotoImage(file="images/draw.gif")
WIN = PhotoImage(file="images/win.gif")
START = PhotoImage(file="images/surtitle.gif")
BUT1 = PhotoImage(file="images/Quit.gif")
BUT2 = PhotoImage(file="images/newgame.gif")
H3 = PhotoImage(file="images/hearts3.gif")
H2 = PhotoImage(file="images/hearts2.gif")
H1 = PhotoImage(file="images/hearts.gif")
H0 = PhotoImage(file="images/hearts0.gif")
PADDLE = PhotoImage(file="images/paddle.gif")
GAME_OVER = PhotoImage(file="images/go.gif")
WIDTH = 700  # Width of the canvas
HEIGHT = 500  # Height of the canvas
RAD = 20  # Ball's radius
CIRCLE = [WIDTH / 2 - RAD, HEIGHT / 2 - RAD, WIDTH / 2 + RAD, HEIGHT / 2 + RAD]  # The position of the circle on the canvas.


PADS_H = 120  # The height of the pad
PADS_W = 20  # The width of the pad
PAD_VEL = 15  # Paddle velocity


# Global values
SPEEDS = [-1, 1, -1, 1]
count = 0
level = 0
respawncounter = 0
accel = 0
x1 = 1*SPEEDS[1]  # Direction|speed of the ball on the canvas (x axe)
y2 = 1*SPEEDS[0]  # Direction|speed of the ball on the canvas (y axe)
levellab = StringVar()

# Describes canvas's parameters and objects on the canvas
Surface = Canvas(master=root, width=WIDTH, height=HEIGHT, borderwidth=0)
Surface.pack(fill=BOTH, expand=YES)  # the pack geometry is used
Surface.create_image(350, 250, image=START, tag="photostart")


def quits():
    root.quit()


def new_game():
    global level, count, x1, y2, itemlp, itemrp, respawncounter, accel
    global timerevent, padcl, padcr, ballco
    Surface.delete("ball", "game_over", "photostart", "win", "phototitl", "itemrp", "itemlp", "padleft", "padright")
    accel = 1
    count = 0
    level = 0
    respawncounter = 0
    random.shuffle(SPEEDS)
    x1 = 1*SPEEDS[1]*accel
    y2 = 1*SPEEDS[0]*accel

    Surface.create_image(350, 250, image=BASE, tag="phototitl")
    Surface.create_oval(CIRCLE, tag="ball", fill="Yellow", outline="White")
    Surface.create_rectangle([2, 2, PADS_W, PADS_H], tag="padleft")
    Surface.create_rectangle([WIDTH-PADS_W+2, 2, WIDTH, PADS_H], tag="padright")
    itemlp = Surface.create_image(10, 60, image=PADDLE, tag="itempl")
    itemrp = Surface.create_image(692, 60, image=PADDLE, tag="itemrp")
    labelh = Label(master=root, image=H3, bg="black").place(x=485, y=7)
    padcl = Surface.coords("padleft")
    padcr = Surface.coords("padright")
    ballco = Surface.coords("ball")

    root.after_cancel(timerevent)
    drawcirc()


def respawn():
    # Respawn the ball in the middle
    global respawncounter
    Surface.delete("ball")
    Surface.create_oval(CIRCLE, tag="ball", fill="Yellow", outline="White")

    if respawncounter == 1:
        labelh = Label(master=root, image=H2, bg="black")
        labelh.place(x=485, y=7)
    elif respawncounter == 2:
        labelh = Label(master=root, image=H1, bg="black")
        labelh.place(x=485, y=7)
    elif respawncounter == 3:
        Surface.delete("ball")
        labelh = Label(master=root, image=H0, bg="black")
        labelh.place(x=485, y=7)
        Surface.create_image(350, 250, image=GAME_OVER, tag="game_over")
    else:
        new_game()


def drawcirc():
    # Ball mobility
    global x1, y2, count, respawncounter, padcl, padcr, ballco
    global accel, level, timerevent
    if 0 <= count <= 1:
        accel = 0.08
        level = 0
        Surface.move("ball", x1*accel, y2*accel)
    if 2 <= count <= 4:
        accel = 0.1
        level = 1
        Surface.move("ball", x1*accel, y2*accel)
    if 5 <= count <= 8:
        accel = 0.2
        level = 2
        Surface.move("ball", x1*accel, y2*accel)
    if 8 <= count <= 12:
        accel = 0.28
        level = 3
        Surface.move("ball", x1*accel, y2*accel)
    if count >= 20:
        Surface.create_image(350, 250, image=WIN, tag="win")

    if Surface.find_overlapping(0, HEIGHT, WIDTH, HEIGHT):
        y2 = -y2
    if Surface.find_overlapping(0, 0, WIDTH, 0):
        y2 = -y2

    padcl = Surface.coords("padleft")
    padcr = Surface.coords("padright")
    ballco = Surface.coords("ball")
    if ballco[0] < padcl[2]:
        if padcl[3] + RAD >= ballco[3] and padcl[1] - RAD <= ballco[1]:
            x1 = -x1
            count += 1
    if ballco[0] <= 0:
            respawncounter += 1
            respawn()
    if ballco[2] > padcr[0]:
        if padcr[3] + RAD >= ballco[3] and padcr[1] - RAD <= ballco[1]:
            x1 = -x1
            count += 1
    if ballco[2] >= 700:
            respawncounter += 1
            respawn()

    levellab.set(str(level))
    timerevent = root.after(1, drawcirc)
timerevent = root.after(1, drawcirc)


# Describes the logic of the pads mobility.

# The mobility of the left pad
def keypress(a):
    global itemlp, itemrp
    Surface.move("padleft", 0, -PAD_VEL)
    Surface.move(itemlp, 0, -PAD_VEL)
    if Surface.find_overlapping(0, 0, WIDTH, 0):  # Stop's pad on the border
        Surface.move("padleft", 0, PAD_VEL)
        Surface.move(itemlp, 0, PAD_VEL)
    Surface.update()
def keypress2(q):
    global itemlp, itemrp
    Surface.move("padleft", 0, PAD_VEL)
    Surface.move(itemlp, 0, PAD_VEL)
    if Surface.find_overlapping(0, 500, 700, 500):  # Stop's pad on the border
        Surface.move("padleft", 0, -PAD_VEL)
        Surface.move(itemlp, 0, -PAD_VEL)
    Surface.update()
# The mobility of the right pad
def keypress3(Up):
    global itemlp, itemrp
    Surface.move("padright", 0, -PAD_VEL)
    Surface.move(itemrp, 0, -PAD_VEL)
    if Surface.find_overlapping(0, 0, WIDTH, 0):  # Stop's pad on the border
        Surface.move("padright", 0, PAD_VEL)
        Surface.move(itemrp, 0, PAD_VEL)
    Surface.update()
def keypress4(Down):
    global itemlp, itemrp
    Surface.move("padright", 0, PAD_VEL)
    Surface.move(itemrp, 0, PAD_VEL)
    if Surface.find_overlapping(0, 502, 700, 502):  # Stop's pad on the border
        Surface.move("padright", 0, -PAD_VEL)
        Surface.move(itemrp, 0, -PAD_VEL)
    Surface.update()


label_level = Label(master=root, textvariable=levellab, bg="green", font=("Helvetica", 15), fg="#EC3572")
label_level.place(x=262, y=7)
label_level2 = Label(master=root, text="Level: ", bg="green", font=("Helvetica", 15), fg="#EC3572")
label_level2.place(x=190, y=7)
button_1 = Button(master=root, image=BUT2, command=new_game)
button_1.place(x=268, y=500)
button_2 = Button(master=root, image=BUT1, command=quits)
button_2.place(x=613, y=517)

frame = Frame(master=root, width=0, height=65)
frame.bind("<KeyPress-a>", keypress)
frame.bind("<KeyPress-q>", keypress2)
frame.bind("<KeyPress-Up>", keypress3)
frame.bind("<KeyPress-Down>", keypress4)
frame.pack()
frame.focus_set()

root.mainloop()
