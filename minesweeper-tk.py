#! /usr/bin/python3
import time, random, tkinter, tkinter.messagebox, tkinter.simpledialog, tkinter.font

class mineDot:
    isMine = False
    isFlag = False
    isSweeped = False

x = 10
y = 10
mines = 10
flag_attempt = 0

r = tkinter.Tk()
r.withdraw()

menu = 0
pause_b = 0
window = 0
remain_label = 0
time_label = 0
isGame = True
isPause = False
timer = 0
start = 0

x_entry = 0
y_entry = 0
mine_entry = 0

root = tkinter.Tk()
root.title("Select a size")
font1 = tkinter.font.Font(family='Helvetica', size=14)
font2 = tkinter.font.Font(family='Helvetica', size=12)
btn1 = tkinter.Button(root,height = 8, text='10x10 with 10 mines', font=font1, command=lambda: firstTime(10, 10, 10))
btn2 = tkinter.Button(root,height = 8, text='20x20 with 40 mines', font=font1 , command=lambda: firstTime(20, 20, 40))
btn3 = tkinter.Button(root,height = 8, text='25x25 with 100 mines', font=font1, command=lambda: firstTime(25, 25, 100))
btn4 = tkinter.Button(root,height = 8, text='custom size', font=font1, command=lambda: customMenu())
root.rowconfigure((0,1), weight=1)  # make buttons stretch when
root.columnconfigure((0,2), weight=1)  # when window is resized
btn1.grid(row=0, column=0, columnspan=1, sticky='EWNS')
btn2.grid(row=0, column=1, columnspan=1, sticky='EWNS')
btn3.grid(row=1, column=0, columnspan=1, sticky='EWNS')
btn4.grid(row=1, column=1, columnspan=1, sticky='EWNS')

def okay():
    global x, y, mines, menu
    x = int(x_entry.get())
    y = int(y_entry.get())
    mines = int(mine_entry.get())
    menu.destroy()
    if window == 0:
        firstTime(x, y, mines)
    else:
        startGame()

def customMenu():
    global x_entry, y_entry, mine_entry, menu
    menu = tkinter.Tk()
    menu.title("Custom size")
    x_entry = tkinter.Entry(menu)
    y_entry = tkinter.Entry(menu)
    mine_entry = tkinter.Entry(menu)
    tkinter.Label(menu, text = "Number of x: ").grid(row=0, column=0)
    x_entry.grid(row=0, column=1)
    x_entry.focus_set()
    tkinter.Label(menu, text = "Number of y: ").grid(row=1, column=0)
    y_entry.grid(row=1, column=1)
    y_entry.focus_set()
    tkinter.Label(menu, text = "Number of mines: ").grid(row=2, column=0)
    mine_entry.grid(row=2, column=1)
    mine_entry.focus_set()
    b = tkinter.Button(menu,text='okay', command=okay)
    b.grid(row=4, column=1)
    menu.mainloop()

def startGame():
    global x, y, mines, points, buttons, pause_b, flag_attempt, window, remain_label, isGame, time_label, start

    start = time.time()

    isGame = True

    if window != 0 :
        for i in window.winfo_children():
            if type(i) != tkinter.Menu:
                i.destroy()
    else:
        firstTime(x, y, mines)
        return

    buttons = []
    flag_attempt = 0
    points = [[mineDot() for i in range(x)] for j in range(y)]

    # putting mines randomly in points
    counter = 0
    while counter < mines:
        rand_x = random.randint(0, x-1)
        rand_y = random.randint(0, y-1)
        if not points[rand_x][rand_y].isMine:
            points[rand_x][rand_y].isMine = True
            counter = counter + 1

    remain_label = tkinter.Label(window, text="Remained attempts: " + str(mines-flag_attempt))
    remain_label.grid(row=1, column=x+3)
    time_label = tkinter.Label(window, text="Time passed: ")
    time_label.grid(row=2, column=x+3)

    pause_b = tkinter.Button(window, text="pause", width=4, command=lambda : pauseGame())
    pause_b.grid(row=3, column=x+3)

    for i in range(y):
        buttons.append([])
        for j in range(x):
            b = tkinter.Button(window, background="#DADADA", text="", width=1, command=lambda x=i,y=j: leftClick(y, x), font=font2)
            b.bind("<Button-3>", lambda e, x=i, y=j:rightClick(y, x))
            b.grid(row=i+1, column=j, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[i].append(b)
    clock()

def pauseGame():
    global start, isPause, isGame, pause_b
    if not isPause:
        pause_b.config(relief=tkinter.SUNKEN)
        isPause = True
        isGame = False
    else:
        pause_b.config(relief=tkinter.RAISED)
        start = time.time() - timer
        isPause = False
        isGame = True

def clock():
    global start, timer
    if isGame:
        timer = time.time() - start
        time_label.config(text="Time passed: " + str(int(timer)))
    time_label.after(1000,clock)

def customSize():
    global x, y, mines
    x = tkinter.simpledialog.askinteger("Custom size", "Enter number of x:")
    y = tkinter.simpledialog.askinteger("Custom size", "Enter number of y:")
    mines = tkinter.simpledialog.askinteger("Custom size", "Enter number of mines:")
    startGame()
    return

def setPoints(x_, y_, mines_):
    global x, y, mines
    x = x_
    y = y_
    mines = mines_
    startGame()
    return

def firstTime(x_, y_, mines_):
    global x, y, mines, root, window
    window = tkinter.Tk()
    window.title("Minesweeper")
    menubar = tkinter.Menu(window)
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="10x10 with 10 mines", command=lambda: setPoints(10, 10, 10))
    menusize.add_command(label="20x20 with 40 mines", command=lambda: setPoints(20, 20, 40))
    menusize.add_command(label="25x25 with 100 mines", command=lambda: setPoints(25, 25, 100))
    menusize.add_separator()
    menusize.add_command(label="custom", command=lambda: customMenu())

    menubar.add_cascade(label="size", menu=menusize)
    menubar.add_command(label="restart", command=lambda: startGame())
    menubar.add_command(label="exit", command=lambda: window.destroy())
    window.config(menu=menubar)
    x = x_
    y = y_
    mines = mines_
    root.destroy()
    startGame()
    window.mainloop()
    return

# get number of the mines around the point
def getValue(x_, y_):
    counter = 0
    range = [-1, 0, +1]
    for i in range:
        for j in range:
            x_tmp = x_ + i
            y_tmp = y_ + j
            if not (y_tmp >= y or x_tmp >= x or y_tmp < 0 or x_tmp < 0):
                if points[x_tmp][y_tmp].isMine:
                    counter = counter + 1
    return counter

def isWon():
    global isGame
    condition1 = True
    condition2 = True
    for i in range(x):
        for j in range(y):
            if points[i][j].isMine != points[i][j].isFlag:
                condition1 = False
            if points[i][j].isMine == points[i][j].isSweeped:
                condition2 = False
            if not(condition1 or condition2):
                return
    isGame = False
    tkinter.messagebox.showinfo("You won !", "You won !")
    startGame()

def sweepPoint(x_, y_):
    points[x_][y_].isSweeped = True
    points[x_][y_].isFlag = False
    buttons[y_][x_].config(relief=tkinter.SUNKEN)
    buttons[y_][x_]['state'] = 'disabled'
    buttons[y_][x_].config(disabledforeground="#000000")
    buttons[y_][x_].config(background="#E9E9E9")
    value = getValue(x_, y_)
    if value == 0:
        range = [-1, 0, 1]
        for i in range:
            for j in range:
                x_tmp = x_ + i
                y_tmp = y_ + j
                if not (y_tmp >= y or x_tmp >= x or y_tmp < 0 or x_tmp < 0 or points[x_tmp][y_tmp].isSweeped == 1):
                    buttons[y_][x_]["text"] = ""
                    sweepPoint(x_tmp, y_tmp)
    else:
        buttons[y_][x_]["text"] = value
    return

def leftClick(x_, y_):
    global isGame
    if not isGame:
        return
    if points[x_][y_].isMine:
        for i in range(x):
            for j in range(y):
                if points[i][j].isMine:
                    buttons[j][i]["text"] = "x"
                    buttons[j][i].config(foreground="#CD0000")
        isGame = False
        tkinter.messagebox.showinfo("Boom !", "Game Over")
        startGame()
        return
    if not points[x_][y_].isSweeped:
        sweepPoint(x_, y_)
        isWon()

def rightClick(x_, y_):
    global flag_attempt
    if not isGame:
        return
    if not points[x_][y_].isSweeped:
        if not points[x_][y_].isFlag:
            if flag_attempt < mines:
                buttons[y_][x_]["text"] = "?"
                buttons[y_][x_].config(foreground="#FF3300")
                points[x_][y_].isFlag = True
                flag_attempt = flag_attempt + 1
                remain_label.config(text="Remained attempts: " + str(mines-flag_attempt))
            else:
                tkinter.messagebox.showinfo("Sorry", "You are out of attempts!")
        else:
            buttons[y_][x_]["text"] = ""
            points[x_][y_].isFlag = False
            isWon()

root.mainloop()
