import tkinter as tk
import random as r
import time
from patterns import patterns, pracPatterns
import csv

# define particulars
timer = 250
wait = 2000
gridSize = 4
cellSize = 100
canvasSize = cellSize*(gridSize)+200
userBlackCount = 0
userWhiteCount = gridSize**2
userResult=[]
userGridStatus=[]
trialGridStatus=[]
total = 0
trial = 0
currBlock = 0

order = [list(range(len(pracPatterns))),list(range(len(patterns))), list(range(len(patterns)))]


def printy():
	try:
		print("Trial Grid Status:")
		for i in range(0, gridSize):
			row = []
			for j in range(0, gridSize):
				row.append(trialGridStatus[i][j])
			print(row)
		print("_______________")
	except IndexError:
		pass
	try:
		print("User Grid Status:")
		for i in range(0, gridSize):
			row = []
			for j in range(0, gridSize):
				row.append(userGridStatus[i][j])
			print(row)
		print("_______________")
	except IndexError:
		pass
	try:
		print("User result:")
		for i in range(0, gridSize):
			row = []
			for j in range(0, gridSize):
				row.append(userResult[i][j])
			print(row)
		print("_______________")
	except IndexError:
		pass


# Start App - open Tk window
def open_window():
	win = tk.Tk()
	win.title('Sym Experiment')
	win.attributes('-fullscreen', True)
	win.bind('<Escape>',lambda e: win.destroy())
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
			grid.create_oval(x1, y1, x2, y2, fill = "white", outline = "grey")
	return grid
	
def allow_click(allow):
	if allow:
		grid.bind("<Button-1>", swap_colour)
	else:
		grid.unbind("<Button-1>")

def hide_pattern():
	grid.pack_forget()
	mask.pack(anchor='n') #fill='both', expand=True, anchor='n'
	global wait
	grid.after(wait, get_response)

def get_response():
	mask.pack_forget()
	allow_click(True)
	blank_grid()
	grid.pack()
	submitBtn.pack()

def blank_grid():
	for k in range(0, gridSize**2+1):
		grid.itemconfig(k, fill = "white")

def submit():
	global userGridStatus
	global userResult
	grid.pack_forget()
	submitBtn.pack_forget()
	submitBtn.config(state="disabled")	
	# check!
	check=0
	for i in range(0, gridSize):
		row = []
		for j in range(0, gridSize):			
			if trialGridStatus[i][j]==userGridStatus[i][j]:
				row.append(("correct"))
				check += 1
			else:
				row.append(("incorrect"))
		userResult.append(row)
	# if all correct, give positive feedback, else give negative feedback
	if check == gridSize**2:
		feedback_cor.pack()
	else:
		feedback_incor.pack()

	# Save output data
	save_data(userGridStatus)

	# reset userGrid to all white and result to empty strings
	for i in range(0, gridSize):
		for j in range(0, gridSize):
			userGridStatus[i][j]="white"
			userResult[i][j]= ""
	# pause then next trial
	grid.after(1500, pause)

def save_data(result):
	data = [currBlock, trial, total, order[currBlock][trial]]
	# flatten result
	flat_result = [item for row in result for item in row]
	# add trial number and pattern number
	data.extend(flat_result)
	# with open(filename, 'a', newline='') as output:
	# 	writer = csv.writer(output)
	# 	writer.writerow(data)
	# output.close()

def pause():
	feedback_cor.pack_forget()
	feedback_incor.pack_forget()
	grid.after(1000, next_trial)

def next_trial():
	global userBlackCount
	global userWhiteCount
	global trial
	global patterns
	global total
	global currBlock
	userBlackCount = 0
	userWhiteCount = gridSize**2
	breakText.pack_forget()
	contBtn.pack_forget()

	trial += 1
	if trial < len(order[currBlock]):
		total +=1
		if currBlock == 0:
			run_trial(pracPatterns[order[currBlock][trial]])
		else:
			run_trial(patterns[order[currBlock][trial]])
	elif currBlock < len(order)-1:
		currBlock +=1
		trial = -1
		break_screen()
	else:
		endText = tk.Label(win, text=display_text('end.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 18))
		endText.pack()

def break_screen():
	breakText.pack()
	contBtn.pack()

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
		row = 0
		column = 0
		for k in range(0, gridSize):
			if loc < (k+1)*gridSize+1:
				row = k
				break
		if loc % gridSize == 0:
			column = gridSize-1
		else:
			column = loc % gridSize-1
		userGridStatus[row][column] = newCol
	except IndexError:
		pass

# display pattern for trial
def display_pattern(pattern):
	k=0
	grid.pack()
	test = 0
	for i in range(0, gridSize):
		for j in range(0, gridSize):
			k += 1
			if pattern[i][j] == 0 or pattern[i][j] == "white":
				grid.itemconfig(k, fill = "white")
				trialGridStatus[i][j] = "white"
			else:
				test += 1
				grid.itemconfig(k, fill = "black")
				trialGridStatus[i][j] = "black"
	global trial
	patternLabel.config(text="Pattern: {}".format(trial+1))
	patternLabel.pack()
	# global timer
	# pattern is displayed for a specified duration (ms), then hidden
	# grid.after(timer, hide_pattern)

def run_trial(pattern):
	global trialGridStatus
	trialGridStatus = pattern
	global userBlackCount
	userBlackCount = 0
	global userWhiteCount
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

	#initialize trial and user grid status
	for i in range(0, gridSize):
		trialRow = []
		userRow = []
		for j in range(0, gridSize):
			trialRow.append("white")
			userRow.append("white")
		trialGridStatus.append(trialRow)
		userGridStatus.append(userRow)

	global trial
	global pracPatterns

	run_trial(pracPatterns[order[currBlock][trial]])


win = open_window()

# Display start text
txt = tk.Label(win, text=display_text('start.txt'), justify=tk.CENTER, padx = 100, pady = 50, font=("Helvetica", 12))
txt.pack()
# Generate and display random ID number
randID = r.randint(100,999)
rID = tk.Label(win, text = "Please record your ID number: {}".format(randID), pady = 10, font=("Helvetica", 12))
rID.pack()
# log randID
# prepare file for saving
# header = [["Participant", randID], ["Block", "Trial", "Total", "Pattern",  "1,1", "1,2", "1,3", "1,4", "2,1", "2,2", "2,3", "2,4", "3,1", "3,2", "3,3", "3,4", "4,1", "4,2", "4,3", "4,4"]]
# filename = "Sym{}.csv".format(randID)
# with open(filename, 'w', newline='') as output:
# 	writer = csv.writer(output)
# 	writer.writerows(header)
# output.close()
# create grid
grid = draw_grid()

# add START button
startBtn = tk.Button(win, text="Start", command=start, font=("Helvetica", 18))
startBtn.pack()
# add NEXT button
nextBtn = tk.Button(win, text="Next", command=next_trial, font=("Helvetica", 18))
nextBtn.pack()
# add pattern label
patternLabel = tk.Label(win, text= "Pattern:")
# prepare noise mask
img = tk.PhotoImage(file='mask.png', height=canvasSize, width=canvasSize)
mask = tk.Label(win, image=img)

# prepare submit button
submitBtn = tk.Button(win, text = "Submit",command=submit, font=("Helvetica", 18))
submitBtn.config(state="disabled")
# prepare feedback
feedback_cor = tk.Label(win, height = 100, width = 100, bg = '#4cbc53', text=display_text('feedback_correct.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 50))
feedback_incor = tk.Label(win, height = 100, width = 100, bg = '#bc534c', text=display_text('feedback_incorrect.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 50))
# prepare breakscreen
breakText = tk.Label(win, text=display_text('break.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 18))
contBtn = tk.Button(win, text="Continue", command=next_trial, font=("Helvetica", 18))

try:
	win.mainloop() #Open window
except (KeyboardInterrupt, SystemExit):
	raise

