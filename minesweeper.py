import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from functools import partial
from random import randint


class Window(QMainWindow):

	def __init__(self):
		super(Window,self).__init__()
		#set title
		self.setWindowTitle("Minesweeper")
		#set icon
		self.setWindowIcon(QtGui.QIcon('favicon.png'))

		#create menubar with menu File=>New to start a new game
		fileAction = QAction("New", self)
		fileAction.triggered.connect(self.init_game)
		mainMenu = self.menuBar()
		fileMenu = mainMenu.addMenu('&File')
		fileMenu.addAction(fileAction)

		#load page at startup
		self.main_page()

		#start new game at startup
		self.init_game()
	
	def main_page(self):		
		#create central widget
		self.centralwidget = QWidget()
		self.setCentralWidget(self.centralwidget)

		#create all the buttons of the minesweeper game
		self.button={}
		horizontalLayout=QHBoxLayout(self.centralwidget)
		for column in range (0,10):
			verticalLayout=QVBoxLayout()
			verticalLayout.setSpacing(0)
			for row in range (0,10):
				self.button[row,column]=QPushButton(self)
				self.button[row,column].setFixedHeight(20)
				self.button[row,column].setFixedWidth(20)
				self.button[row,column].setIcon(QtGui.QIcon('tile_plain.gif'))
				#set filter to detect right mouse click button
				self.button[row,column].installEventFilter(self)
				self.button[row,column].setObjectName(str(row)+','+str(column))
				self.button[row,column].clicked.connect(partial(self.button_pressed,row,column))
				verticalLayout.addWidget(self.button[row,column])
			horizontalLayout.addLayout(verticalLayout)
			horizontalLayout.setSpacing(0)
		self.show()
	
	def eventFilter(self,obj,event):
		if event.type() == QEvent.MouseButtonPress:
			if event.button() == Qt.RightButton:
				name_button=obj.objectName()
				if self.initialArray[int(name_button[0])][int(name_button[2])]==19:
					self.initialArray[int(name_button[0])][int(name_button[2])]=9
					self.button[int(name_button[0]),int(name_button[2])].setIcon(QtGui.QIcon('tile_plain.gif'))
				else:
					self.initialArray[int(name_button[0])][int(name_button[2])]=19
					self.button[int(name_button[0]),int(name_button[2])].setIcon(QtGui.QIcon('tile_flag.gif'))
		return QObject.event(obj, event)

	def init_game(self):
		#reset counter of turns
		self.counterTurns=0
		
		#set initial array to zero
		self.initialArray=[[0 for i in range(10)]for j in range(10)]
		#add bombs and adjust surrounding cells
		for column in range (0,10):
			for row in range (0,10):
				#it is randomly decided whether a cell has a bomb, therefore the number of bombs is not fixed
				#the change of having a bomb can be adjusted by changing the range of randint
				bomb=randint(0,6)
				if bomb==0:
					self.initialArray[row][column]=9
					if row-1>=0 and self.initialArray[row-1][column]!=9:
						self.initialArray[row-1][column]+=1
					if row+1<=9 and self.initialArray[row+1][column]!=9:
						self.initialArray[row+1][column]+=1
					if column-1>=0 and self.initialArray[row][column-1]!=9:
						self.initialArray[row][column-1]+=1
					if column+1<=9 and self.initialArray[row][column+1]!=9:
						self.initialArray[row][column+1]+=1
					if row-1>=0 and column-1>=0 and self.initialArray[row-1][column-1]!=9:
						self.initialArray[row-1][column-1]+=1
					if row+1<=9 and column-1>=0 and self.initialArray[row+1][column-1]!=9:
						self.initialArray[row+1][column-1]+=1
					if row-1>=0 and column+1<=9 and self.initialArray[row-1][column+1]!=9:
						self.initialArray[row-1][column+1]+=1
					if row+1<=9 and column+1<=9 and self.initialArray[row+1][column+1]!=9:
						self.initialArray[row+1][column+1]+=1
				#reset icons of buttons to default
				self.button[row,column].setIcon(QtGui.QIcon('tile_plain.gif'))
		#for debugging purposes the initial array is printed
		for row in self.initialArray:
			print (row)

	def message_button(self):
		self.init_game()

	def button_pressed(self,row,column):
		#change number of turns
		self.counterTurns+=1

		#if the value is 19, a flag is on the button and the button can not be pressed
		if self.initialArray[row][column]!=19:
			#check if the clicked cell has a bomb (value=9)
			if self.initialArray[row][column]==9:
				self.button[row,column].setIcon(QtGui.QIcon('tile_mine.gif'))
				gameover = QMessageBox()
				gameover.setIcon(QMessageBox.Information)
				gameover.setText("Game over, better luck next time!")
				gameover.setInformativeText("Number of turns: "+str(self.counterTurns))
				gameover.setWindowTitle("Game over")
				gameover.setStandardButtons(QMessageBox.Ok)
				gameover.buttonClicked.connect(self.message_button)
				gameover.exec_()

			else:
				#call method to display all the empty cells (value=0)
				self.display_empty_buttons(row,column)


				#check whether all the cells (exept bombs) are displayed
				game_busy=0
				values=[1,2,3,4,5,6,7,8]
				for x in self.initialArray:
					if any(i in values for i in x):
						game_busy=1
				if game_busy==0:
					gamewon = QMessageBox()
					gamewon.setIcon(QMessageBox.Information)
					gamewon.setText("Congratulations, you won!")
					gamewon.setInformativeText("Number of turns: "+str(self.counterTurns))
					gamewon.setWindowTitle("Congratulations")
					gamewon.setStandardButtons(QMessageBox.Ok)
					gamewon.buttonClicked.connect(self.message_button)
					gamewon.exec_()

		#for debugging purposes the initial array is printed
		for row in self.initialArray:
			print (row)
		print('\n')

			
	def display_empty_buttons(self,row,column):
		#the value of initialArray can be 0-8, 9 is for a bomb, 10 if it has been opened
		if self.initialArray[row][column]!=0:
			if self.initialArray[row][column]!=10:
				if self.initialArray[row][column]==0:
					self.button[row,column].setIcon(QtGui.QIcon('tile_clicked.gif'))
				elif self.initialArray[row][column]==1:
					self.button[row,column].setIcon(QtGui.QIcon('tile_1.gif'))	
				elif self.initialArray[row][column]==2:
					self.button[row,column].setIcon(QtGui.QIcon('tile_2.gif'))
				elif self.initialArray[row][column]==3:
					self.button[row,column].setIcon(QtGui.QIcon('tile_3.gif'))	
				elif self.initialArray[row][column]==4:
					self.button[row,column].setIcon(QtGui.QIcon('tile_4.gif'))	
				elif self.initialArray[row][column]==5:
					self.button[row,column].setIcon(QtGui.QIcon('tile_5.gif'))
				elif self.initialArray[row][column]==6:
					self.button[row,column].setIcon(QtGui.QIcon('tile_6.gif'))	
				elif self.initialArray[row][column]==7:
					self.button[row,column].setIcon(QtGui.QIcon('tile_7.gif')) 
				elif self.initialArray[row][column]==8:
					self.button[row,column].setIcon(QtGui.QIcon('tile_8.gif'))
				elif self.initialArray[row][column]==9:
					self.button[row,column].setIcon(QtGui.QIcon('tile_mine.gif'))
			if self.initialArray[row][column]!=9:
				self.initialArray[row][column]=10
		else:
			if self.initialArray[row][column]!=10:
				if self.initialArray[row][column]==0:
					self.button[row,column].setIcon(QtGui.QIcon('tile_clicked.gif'))
			self.initialArray[row][column]=10
			if row-1>=0:
				self.display_empty_buttons(row-1,column)
			if row+1<=9:
				self.display_empty_buttons(row+1,column)
			if column-1>=0:
				self.display_empty_buttons(row,column-1)
			if column+1<=9:
				self.display_empty_buttons(row,column+1)
			if row-1>=0 and column-1>=0:
				self.display_empty_buttons(row-1,column-1)
			if row+1<=9 and column-1>=0:
				self.display_empty_buttons(row+1,column-1)
			if row-1>=0 and column+1<=9:
				self.display_empty_buttons(row-1,column+1)
			if row+1<=9 and column+1<=9:
				self.display_empty_buttons(row+1,column+1)


if __name__ == '__main__':
	app = QApplication(sys.argv)
	ex = Window()
	sys.exit(app.exec_())




