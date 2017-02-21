#!/usr/bin/python
# Blocks.py

from graphics import *

class Box:

	empty = True
	blocked = False
	
	def __init__(self, x, y, window):
		self.x = x
		self.y = y
		self.window = window
		self.location = Point(x, y)
		self.col = int(x / 50 - 1)
		self.row = int(y / 50 - 1)
		self.block = Rectangle(Point(x - 25, y - 25), Point(x + 25, y + 25))

	def isEmpty(self):
		return self.empty

	def isBlocked(self):
		return self.blocked

	def makeEmpty(self):
		self.empty = True
		self.blocked = False
		self.block.undraw()

	def makeBlocked(self):
		self.blocked = True
		self.empty = False
		self.block.setOutline("white")
		self.block.setFill("black")
		self.block.draw(self.window)

	def makeFull(self, color):
		self.empty = False
		self.block.setOutline("white")
		self.block.setFill(color)
		self.block.draw(self.window)

	def undrawBlock(self):
		self.block.undraw()
		self.empty = True
		self.blocked = False

class BoxGrid:

	numberFull = 0
	fullColumns = []
	fullRows = []
	
	def __init__(self, window):
		self.boxes = [[Box(75+50*i, 75+50*j, window) for j in range(8)] \
		for i in range(8)]

	def checkFit(self, col, row, blockNumber, blockType):
		
		fit = True
		outofrange = False

		col1 = col
		row1 = row

		for i in range(blockNumber):
			if col1 > 7 or row1 > 7:
				outofrange = True
			if blockType == 0:
				if i == 0:
					row1 += 1
				elif i == 1:
					col1 += 1
				elif i == 2:
					row1 += 1
			elif blockType == 1:
				col1 += 1
			''' add bigger pieces here '''
			
		if outofrange == False:
			for i in range(blockNumber):
				isEmpty = self.boxes[col][row].isEmpty()
				if isEmpty == False:
					fit = False
				if blockType == 0:
					if i == 0:
						row += 1
					elif i == 1:
						col += 1
					elif i == 2:
						row += 1
				elif blockType == 1:
					col += 1
				''' add bigger pieces here'''

		if outofrange == True:
			fit = False

		return fit

	def addBlocked(self, col, row):
		
		self.boxes[col][row].makeBlocked()

	def drawBlocks(self, col, row, blockNumber, blockType):

		if blockType == 0:
			if blockNumber == 1:
				color = "hot pink"
			elif blockNumber == 2:
				color = "yellow"
			elif blockNumber == 3:
				color = "blue"
			elif blockNumber == 4:
				color = "red"

		elif blockType == 1:
			if blockNumber == 1:
				color = "hot pink"
			elif blockNumber == 2:
				color = "sky blue"
			elif blockNumber == 3:
				color = "purple"
			elif blockNumber == 4:
				color = "green"
		''' add bigger pieces here '''
		
		for i in range(blockNumber):
			self.boxes[col][row].makeFull(color)
			if blockType == 0:
				if i == 0:
					row += 1
				elif i == 1:
					col += 1
				elif i == 2:
					row += 1

			elif blockType == 1:
				col += 1

			''' add bigger pieces here '''

	# checks all the columns, rows to see if any are full and 
		# increases numberFull by however many are full and adds
		# the first box of each row, col to respective lists to be
		# cleared by clearLines functions
	def checkFullLines(self):
		
		# check all 8 columns for fullness
		for col in range(8):
			full = True
			for row in range(8):
				box = self.boxes[col][row]
				if box.isEmpty():
					full = False
				if box.isBlocked():
					full = False
			if full:
				self.numberFull += 1
				self.fullColumns.append(col)

		# check all 8 rows for fullness
		for row in range(8):
			full = True
			for col in range(8):
				box = self.boxes[col][row]
				if box.isEmpty():
					full = False
				if box.isBlocked():
					full = False
			if full:
				self.numberFull += 1
				self.fullRows.append(row)

	# makes empty all the full lines in the grid and returns the number
		# of lines cleared for score keeping purposes
	def clearLines(self):

		# call class function to find full cols, rows
		self.checkFullLines()

		# clear the full columns
		for col in self.fullColumns:
			for row in range(8):
				self.boxes[col][row].makeEmpty()

		# clear the full rows
		for row in self.fullRows:
			for col in range(8):
				self.boxes[col][row].makeEmpty()

		numFull = self.numberFull
		
		# reset numberFull to zero and full lists
		self.numberFull = 0
		self.fullColumns = []
		self.fullRows = []

		# return how many lines were cleared
		return numFull

	def findSpace(self, blockSize, blockType):
		
		spaceLeft = False
		
		boxesChecked = 0
		col = 0
		row = 0

		while spaceLeft == False and boxesChecked < 64:
		
			if blockType == 0:
				if self.boxes[col][row].isEmpty():
					if blockSize == 1:
						spaceLeft = True

					elif blockSize == 2 and row + 1 <= 7:
						if self.boxes[col][row+1].isEmpty():
							spaceLeft = True

					elif blockSize == 3 and row + 1 <= 7 and col + 1 <= 7:
						if self.boxes[col][row+1].isEmpty() and \
						self.boxes[col+1][row+1].isEmpty():
							spaceLeft = True

					elif blockSize == 4 and row + 2 <= 7 and col + 1 <= 7:
						if self.boxes[col][row+1].isEmpty() and \
						self.boxes[col+1][row+1].isEmpty() and \
						self.boxes[col+1][row+2].isEmpty():
							spaceLeft = True

			elif blockType == 1 or blockType == 2:
				space = True
				for i in range(blockSize):
					if col + i <= 7:
						if self.boxes[col+i][row].isEmpty() == False:
							space = False
					else:
						space = False
				spaceLeft = space
			''' add bigger pieces here '''

			boxesChecked += 1
			row += 1

			if row == 8:
				row = 0
				col += 1

		return spaceLeft

	def clearBoard(self):

		for i in range(8):
			for j in range(8):
				self.boxes[i][j].undrawBlock()

class laterBlock:

	x1 = 30
	x2 = 70
	y1 = 510
	y2 = 550
	blockList = []
	
	def __init__(self, blockNumber, blockType,  window):
		
		self.blockNumber = blockNumber
		self.window = window
		self.blockType = blockType

	def drawWaiting(self):
		
		if self.blockType == 0:
			if self.blockNumber == 1:
				color = "hot pink"
			elif self.blockNumber == 2:
				color = "yellow"
			elif self.blockNumber == 3:
				color = "blue"
			elif self.blockNumber == 4:
				color = "red"

		elif self.blockType == 1:
			if self.blockNumber == 1:
				color = "hot pink"
			elif self.blockNumber == 2:
				color = "sky blue"
			elif self.blockNumber == 3:
				color = "purple"
			elif self.blockNumber == 4:
				color = "green"
		
		# blockBlock
		elif self.blockType == 2:
			color = "black"
		''' add bigger blocks here '''

		tempx1 = self.x1
		tempx2 = self.x2
		tempy1 = self.y1
		tempy2 = self.y2

		for i in range(self.blockNumber):
			block = Rectangle(Point(tempx1, tempy1), Point(tempx2, tempy2))
			block.setOutline("white")
			block.setFill(color)
			block.draw(self.window)
			self.blockList.append(block)
			
			if self.blockType == 0:
				if i == 0:
					tempy1 += 40
					tempy2 += 40
				if i == 1:
					tempx1 += 40
					tempx2 += 40
				if i == 2:
					tempy1 += 40
					tempy2 += 40

			elif self.blockType == 1:
				tempx1 += 40
				tempx2 += 40
			''' add bigger blocks here '''

	def undraw(self):
		for block in self.blockList:
			block.undraw()

	def makeNext(self):

		self.undraw()
		self.x1 += 200
		self.x2 += 200

		self.drawWaiting()


