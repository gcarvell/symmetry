import tkinter as tk
import random as r
import time
from patterns import *
import csv

# define particulars
timer = 400
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

order = [list(range(66)), list(range(66)), list(range(66)), list(range(66))]
for block in order:
	r.shuffle(block)

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
	mask.pack(fill='both', expand=True, anchor='n')
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
	grid.after(1500, pause)
	# log response
	# pause then next trial

def save_data(result):
	data = [currBlock, trial, total, order[currBlock][trial]]
	# flatten result
	flat_result = [item for row in result for item in row]
	# add trial number and pattern number
	data.extend(flat_result)
	with open(filename, 'a', newline='') as output:
		writer = csv.writer(output)
		writer.writerow(data)
	output.close()

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
	
	total +=1
	trial += 1
	if trial < 66:
		run_trial(patterns[order[currBlock][trial]])
	elif currBlock < 3:
		currBlock +=1
		trial = 0
		break_screen()
	else:
		endText = tk.Label(win, text=display_text('end.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 18))
		endText.pack()

	#  trial += 1
	# if trial < len(patterns):
	# 	run_trial(patterns[trial])
	# else:
		# endText = tk.Label(win, text=display_text('end.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 18))
		# endText.pack()

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
	for i in range(0, gridSize):
		for j in range(0, gridSize):
			k += 1
			if pattern[i][j] == 0:
				grid.itemconfig(k, fill = "white")
				trialGridStatus[i][j] = "white"
			else:
				grid.itemconfig(k, fill = "black")
				trialGridStatus[i][j] = "black"
	global timer
	# pattern is displayed for a specified duration (ms), then hidden
	grid.after(timer, hide_pattern)

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


	for i in range(0, gridSize):
		row = []
		userRow = []
		for j in range(0, gridSize):
			row.append("white")
			userRow.append("white")
		trialGridStatus.append(row)
		userGridStatus.append(userRow)

	# Get patterns


	# for each pattern
		# run tr
		# ial:
	global trial
	global patterns
	run_trial(patterns[trial])


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
header = [["Participant", randID], ["Block", "Trial", "Total", "Pattern",  "1,1", "1,2", "1,3", "1,4", "2,1", "2,2", "2,3", "2,4", "3,1", "3,2", "3,3", "3,4", "4,1", "4,2", "4,3", "4,4"]]
filename = "Sym{}.csv".format(randID)
with open(filename, 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerows(header)
output.close()
# create grid
grid = draw_grid()

# add START button
startBtn = tk.Button(win, text="START", command=start)
startBtn.pack()
# prepare noise mask
img = tk.PhotoImage(file='mask.gif')
mask = tk.Label(win, image=img)

# prepare submit button
submitBtn = tk.Button(win, text = "Submit",command=submit)
submitBtn.config(state="disabled")
# prepare feedback
feedback_cor = tk.Label(win, height = 100, width = 100, bg = 'green', text=display_text('feedback_correct.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 50))
feedback_incor = tk.Label(win, height = 100, width = 100, bg = 'red', text=display_text('feedback_incorrect.txt'), justify=tk.CENTER, pady = 200, font=("Helvetica", 50))

try:
	win.mainloop() #Open window
except (KeyboardInterrupt, SystemExit):
	raise

