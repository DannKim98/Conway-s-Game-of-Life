from tkinter import *

deadColor, aliveColor = 'black', 'green'
cellSize = 10
width, height = 1000, 770
numRows, numCols = height//cellSize, width//cellSize
table = [[None for j in range(numCols)] for i in range(numRows)]
stop = False

def born(i, j):
	if (numRows > i >= 0 and numCols > j >= 0):
		canvas.itemconfig(table[i][j], fill = aliveColor, tags = 'alive')

def die(i, j):
	if (numRows > i >= 0 and numCols > j >= 0):
		canvas.itemconfig(table[i][j], fill = deadColor, tags = 'dead')

def shouldBorn(i, j):
	if (numRows > i >= 0 and numCols > j >= 0):
		canvas.itemconfig(table[i][j], tags = 'should_born')

def shouldDie(i, j):
	if (numRows > i >= 0 and numCols > j >= 0):
		canvas.itemconfig(table[i][j], tags = 'should_die')

def draw(pos):
	i = (pos.y)//cellSize
	j = (pos.x)//cellSize
	born(i, j)

def erase(pos):
	i = (pos.y)//cellSize
	j = (pos.x)//cellSize
	die(i, j)

def isAlive(i, j):
	if (numRows > i >= 0 and numCols > j >= 0):
		return canvas.itemcget(table[i][j], "fill") == aliveColor

def step():
	for i in range(numRows):
		for j in range(numCols):
			neighbors = 0
			for iShift in range(-1, 2):
				for jShift in range(-1, 2):
					if (iShift == 0 and jShift == 0): continue
					if (isAlive(i + iShift, j + jShift)): neighbors += 1
			if(neighbors == 3 and not isAlive(i, j)): shouldBorn(i, j)
			elif((neighbors <= 1 or neighbors >= 4) and isAlive(i, j)): shouldDie(i, j)

	for i in range(numRows):
		for j in range(numCols):
			if canvas.gettags(table[i][j])[0] == 'should_born':
				born(i, j)
			elif canvas.gettags(table[i][j])[0] == 'should_die':
				die(i, j)

def killAll():
	for i in range(numRows):
		for j in range(numCols):
			die(i, j)

def pause():
	global stop
	stop = True

def evolve():
	global stop
	stop = False
	while(not stop):
		step()
		window.update_idletasks()
		window.update()		


window = Tk()
window.title("Conway's Game of Life")
window.geometry(str(width) + 'x' + str(height+30))

canvas = Canvas(window, height = height)
canvas.pack(fill = BOTH)

for i in range(numRows):
	for j in range(numCols):
		cell = canvas.create_rectangle(cellSize * j, cellSize * i,
			cellSize + cellSize * j, cellSize + cellSize *i, fill = deadColor, tags = 'dead')
		table[i][j] = cell

frame1 = Frame(window)
btnStep = Button(frame1, text = 'One Step', bg = 'green', fg = 'white', command = step)
btnEvolve = Button(frame1, text = 'Evolve', bg = 'green', fg = 'white', command = evolve)
btnStep.pack(side = 'left')
btnEvolve.pack(side = 'right')
frame1.pack(side = 'left')

frame2 = Frame(window)
btnPause = Button(frame2, text = 'Pause', bg = 'red', fg = 'white', command = pause)
btnKillAll = Button(frame2, text = 'Kill All', bg = 'red', fg = 'white', command = killAll)
btnPause.pack(side = 'left')
btnKillAll.pack(side = 'right')
frame2.pack(side = 'right')

canvas.bind('<Button-1>', draw)
canvas.bind('<B1-Motion>', draw)
canvas.bind('<Button-3>', erase)
canvas.bind('<B3-Motion>', erase)
window.mainloop()