import tkinter as tk
import random as r
import time

# define particulars
gridSize = 4
cellSize = 100
canvasSize = cellSize*(gridSize)+200
userBlackCount = 0
userWhiteCount = gridSize**2
trial = 0
pattern1 = [[0,1,0,1],[1,1,0,0],[0,0,0,0],[1,1,1,1]]
pattern2 = [[1,1,1,1],[1,0,0,1],[1,0,0,1],[0,0,0,0]]
patterns = [pattern1, pattern2]

# Start App - open Tk window
def open_window():
	win = tk.Tk()
	win.title('Sym Experiment')
	win.geometry("700x700") #Setthe size of the app to be 500x500
	win.resizable(0, 0) #Don't allow resizing in the x or y direction
	return win

# Get text from file
def display_text(file):
	with open(file, "r") as f:
		return f.read()

def draw_grid():
	grid = tk.Canvas(width = canvasSize, height = canvasSize)
	for i in range(0, gridSize):
		for j in range(0, gridSize):
			x1 = cellSize*(j+1)
			x2 = x1 + cellSize
			y1 = cellSize*(i+1)
			y2 = y1 + cellSize
			grid.create_rectangle(x1, y1, x2, y2, fill = "white", outline = "grey")
	return grid
	
def allow_click(allow):
	if allow:
		grid.bind("<Button-1>", swap_colour)
	else:
		grid.unbind("<Button-1>")

def hide_pattern():
	grid.pack_forget()
	grid.after(1000, get_response)

def get_response():
	allow_click(True)
	blank_grid()
	grid.pack()
	submitBtn.pack()

def blank_grid():
	for k in range(0, gridSize**2+1):
		grid.itemconfig(k, fill = "white")

def submit():
	grid.pack_forget()
	submitBtn.pack_forget()
	submitBtn.config(state="disabled")	
	
	feedback_cor.pack()
	grid.after(1000, next_trial)
	# log response
	# pause then next trial
def next_trial():
	global userBlackCount
	global userWhiteCount
	global trial
	global patterns
	userBlackCount = 0
	userWhiteCount = gridSize**2
	feedback_cor.pack_forget()
	trial += 1
	if trial < len(patterns):
		run_trial(patterns[trial])
	else:
		endText = tk.Label(win, text=display_text('end.txt'))
		endText.pack()

# change colour of square on click
def swap_colour(loc):
	global userBlackCount
	global userWhiteCount
	try:
		if grid.find_withtag("current")[0]:
			loc=grid.find_withtag("current")[0]
		else:
			return
		#get fill colour for canvas item rect
		col = grid.itemcget(loc,"fill")
		# if black, swap to white, vice versa
		if col=="black":
			userWhiteCount +=1
			userBlackCount -=1
			newCol="white"
		else:
			if userBlackCount >= gridSize**2/2:
				newCol = "white"
			else:
				userBlackCount +=1
				userWhiteCount -=1
				newCol="black"
		grid.itemconfig(loc,fill = newCol)
		if userBlackCount >= gridSize**2/2:
			submitBtn.config(state="normal")
		else:
			submitBtn.config(state="disabled")
	except IndexError:
		pass

# display pattern for trial
def display_pattern(pattern):
	k=0
	grid.pack()
	for i in range(0, gridSize):
		for j in range(0, gridSize):
			k += 1
			x1 = cellSize*(j+1)
			x2 = x1 + cellSize
			y1 = cellSize*(i+1)
			y2 = y1 + cellSize
			if pattern[i][j] == 0:
				grid.itemconfig(k, fill = "white")
			else:
				grid.itemconfig(k, fill = "black")
	grid.after(1000, hide_pattern)

def run_trial(pattern):
	userBlackCount = 0
	userWhiteCount = gridSize**2
	# don't allow subject to click grid
	allow_click(False)
	# display pattern for this trial
	grid.pack()
	display_pattern(pattern)


# Start experiment when START button is clicked
def start():
	# remove start text
	txt.pack_forget()
	rID.pack_forget()
	# remove start button
	startBtn.pack_forget()

	# Get patterns


	# for each pattern
		# run tr
		# ial:
	global trial
	global patterns
	run_trial(patterns[trial])
	

		# save subject responses
		# check subject performance against correct pattern
		# display feedback

win = open_window()

# Display start text
txt = tk.Label(win, text=display_text('start.txt'))
txt.pack()
# Generate and display random ID number
randID = r.randint(100,999)
rID = tk.Label(win, text = "Please record your ID number: {}".format(randID))
rID.pack()
# log randID

# create grid
grid = draw_grid()

# add START button
startBtn = tk.Button(win, text="START", command=start)
startBtn.pack()

# prepare submit button
submitBtn = tk.Button(win, text = "Submit",command=submit)
submitBtn.config(state="disabled")
# prepare feedback
feedback_cor = tk.Label(win, text=display_text('feedback_correct.txt'))

try:
	win.mainloop() #Open window
except (KeyboardInterrupt, SystemExit):
	raise

