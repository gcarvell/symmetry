import csv
import copy
import os
import patterns as p

filename = "Sym633.csv"

def analyse(filename):
	subj = filename[3:6]
	# import data
	results = []
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for i, row in enumerate(csv_reader):
			if i > 1:

				newRow = []
				for j, value in enumerate(row):
					if j == 3:
						chunked = [value]
					if j > 3:
						if value == "black":
							num = 1
						else:
							num = 0
						newRow.append(num)
				# chunks = [newRow[i:i + 4] for i in range(0, len(newRow)-1, 4)]
				chunked.append([newRow[i:i + 4] for i in range(0, len(newRow)-1, 4)])
				results.append(chunked)

	# import patterns 
	pracPatternList = dict(enumerate(p.pracPatterns))
	patternList = dict(enumerate(p.patterns))
	scores = []
	block = 1
	# calculate result
	for x, result in enumerate(results):
		if x > 74:
			block = 2
		if x > 7:
			patternNum = int(result[0])
			curResponse = result[1]
			curPattern = patternList[patternNum]
			outcome = []
	#   for each dot compare user response and pattern
			for i in range(0, 4):
				check = []
				for j in range(0, 4):			
					if curResponse[i][j]==curPattern[i][j]:
						check.append(1)
					else:
						check.append(0)
				outcome.append(check)
			flatOutcome = [y for x in outcome for y in x]
	#   sum incorrect values (divide by 2)
			scores.append([block, patternNum+1,  int(sum(flatOutcome)/2)])
	scores.sort(key=lambda tup: tup[1]) 


	blockOne = scores[0::2]
	blockTwo = scores[1::2]
	b1 = 0
	b2 = 0
	for i, t in enumerate(blockTwo):
		blockOne[i].append(t[2])
		blockOne[i].pop(0)
		b1 += blockOne[i][1]
		b2 += blockOne[i][2]
	print(blockOne)
	scoreB1 = b1/66/8*100
	scoreB2 = b2/66/8*100
	print("{:.1f}".format(scoreB1))
	print("{:.1f}".format(scoreB2))


# Export results
	with open("Output{}.csv".format(subj), 'w', newline='') as csv_file:
		writer = csv.writer(csv_file)
		writer.writerow(["stim","block1","block2"])
		for row in blockOne:
			writer.writerow(row)

#"subject" "stim" "block" "result"
	with open("concat.csv", "a", newline="") as concat:
		writer = csv.writer(concat)
		for row in blockOne:
			row.append(subj)
			writer.writerow(row)


# Later: positions of incorrect values


for root, dirs, files in os.walk(".", topdown=False):
	for name in files:
		if str(name).startswith("Sym"):
			print(str(name))
			analyse(str(name))
	