#!/usr/bin/python
# Game

from graphics import *
from blocks import *
from random import *
from time import sleep

def main():

	win = GraphWin("Blocks", 500, 700)
	win.setBackground(color_rgb(32, 32, 32))

	# use later for draw next and later pieces
	nextX = 250
	nextY = 525
	laterX = 50
	laterY = 525

	logo = Image(Point(250, 350), "blocksgraphic.gif")
	logo.draw(win)
	win.getMouse()
	logo.undraw()
	
	# Game grid is 400x400
	border = Rectangle(Point(50, 50), Point(450, 450))
	border.setOutline("white")
	border.draw(win)

	# Draw 8 vertical grid lines
	for i in range(100, 401, 50):
		vertLine = Line(Point(i, 50), Point(i, 450))
		vertLine.setOutline("white")
		vertLine.draw(win)

	for i in range(100, 401, 50):
		horLine = Line(Point(50, i), Point(450, i))
		horLine.setOutline("white")
		horLine.draw(win)

	# waiting area for next pieces
	lobby = Rectangle(Point(0, 500), Point(499, 699))
	lobby.setFill(color_rgb(24, 24, 24))
	lobby.setOutline("white")
	lobby.draw(win)

	# quit button
	quitBox = Rectangle(Point(25, 5), Point(125, 45))
	quitBox.setOutline("white")
	quitText = Text(Point(75, 25), "Quit")
	quitText.setTextColor("white")
	quitBox.draw(win)
	quitText.draw(win)

	instructionString = "To place block, click on box to put top left most square. Fill a row or column to clear it.\nA black block prevents its row and column from being cleared."
	errorString = "Block doesn't fit there."
	instructionText = Text(Point(250, 475), instructionString)
	instructionText.setTextColor("white")
	instructionText.draw(win)
	
	# create list of empty box objects to draw blocks in
	boxes = BoxGrid(win)

	points = 0
	pointsText = Text(Point(250, 25), str(points))
	pointsText.setTextColor("white")
	pointsText.setSize(20)
	pointsText.draw(win)

	# 1 create nextPiece and draw it to center of lobby
	nextType = randrange(0, 2)
	nextSize = randrange(nextType + 1, 5)

	nextBlock = laterBlock(nextSize, nextType, win)
	nextBlock.makeNext()
	nextBlock.drawWaiting()

	# 2 create laterPiece and draw it to left of lobby
	laterType = randrange(0, 2)
	laterSize = randrange(laterType + 1, 5)
	
	later = laterBlock(laterSize, laterType, win)
	later.drawWaiting()

	# playAgain and spaceLeft both begin as true
	playAgain = True
	spaceLeft = True

	# 3 while playAgain and space left for nextPiece
	while playAgain and spaceLeft:
		
		# 3.1 userClick
		userClick = win.getMouse()

		# 3.2 get clickX
		clickX = userClick.getX()

		# 3.3 get clickY
		clickY = userClick.getY()

		if clickY in range(50, 450) and clickX in range(50, 450):

				# 3.4 check which box the click is in assign to clickedBox
				userCol = int(clickX / 50 - 1)
				userRow = int(clickY / 50 - 1)
				
				# 3.5 check emptiness of clickedBox and all other 
					# block spaces
				doesFit = boxes.checkFit(userCol, userRow, nextSize, nextType)

				# 3.6 if click puts blocks in taken boxes
				if doesFit == False:
					# 3.6.1 tell user piece can't fit there
					instructionText.setText(errorString)
					win.getMouse()
					instructionText.setText(instructionString)

				# 3.7 if blocks can fit
				else:

					# 3.7.1 draw blocks to boxes
					if nextType == 2:
						boxes.addBlocked(userCol, userRow)
					else:
						boxes.drawBlocks(userCol, userRow, nextSize, nextType)	

					# 3.7.2 add points to point total
					points += nextSize

					# 3.7.3 nextPiece = laterPiece
					nextBlock.undraw()
					nextSize = laterSize
					nextType = laterType
					nextBlock = later
					nextBlock.makeNext()
					
					# 3.7.4 create new laterPiece
					check_blocked = randrange(0, 30)
					if check_blocked == 20:
						laterType = 2
						laterSize = 1
					else:
						laterType = randrange(0, 2)
						laterSize = randrange(laterType + 1, 5)
					
					later = laterBlock(laterSize, laterType, win)
					
					later.drawWaiting()

					# 3.7.5 change box emptiness statuses to not empty
						# DONE in checkFit function

					# 3.7.6 check all rows and columns for fullness
					linesCleared = boxes.clearLines()

					# 3.7.7.1 if full
					if linesCleared > 0:

						# delete the blocks
						# change box statuses to empty
						# add 8 points to total for each row/col cleared
						lineclearpoints = linesCleared * 8
						points += lineclearpoints

				pointsText.setText(str(points))

				# 3.8 check for space left on board for last piece
				spaceLeft = boxes.findSpace(nextSize, nextType)

				# 3.9 if can't fit
				if spaceLeft == False:
					
					# 3.9.1 tell user the game is over and print final score
					instructionText.setText("Block cannot fit. Game Over.")
					# 3.9.2 wait for mouse click and ensure it's in a button
					clickedButton = False

					playBox = Rectangle(Point(200, 325), \
					Point(300, 375))
					playBox.setOutline("white")
					playBox.setFill("white")
					playText = Text(Point(250, 350), "Play Again?")
					playBox.draw(win)
					playText.draw(win)

					while clickedButton == False:
						
						# 3.9.3 if click on playAgain
						quitClick = win.getMouse()
						quitX = quitClick.getX()
						quitY = quitClick.getY()
					
						# if play again
						if quitX in range(200, 300) and \
						quitY in range(325, 375):
							clickedButton = True

							playBox.undraw()
							playText.undraw()
							nextBlock.undraw()
							later.undraw()
							spaceLeft = True

							points = 0
							pointsText.setText(str(points))
							# reset next and later piece
							nextType = randrange(0, 2)
							nextSize = randrange(nextType + 1, 5)
							nextBlock = laterBlock(nextSize, nextType, win)
							nextBlock.makeNext()
							nextBlock.drawWaiting()

							laterType = randrange(0, 2)
							laterSize = randrange(laterType + 1, 5)
							later = laterBlock(laterSize, laterType, win)
							later.drawWaiting()
							# clear boxes in window and set to empty
							boxes.clearBoard()

							instructionText.setText(instructionString)

						# if quit
						elif quitX in range(25, 125) and \
						quitY in range(5, 45):
							clickedButton = True
							playAgain = False

		elif clickX in range(25, 125) and clickY in range(5, 45):
			playAgain = False


	instructionText.setText("Thanks for playing!")
	sleep(1)
	win.close()

main()
