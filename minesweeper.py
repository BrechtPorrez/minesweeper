import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QAction, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox, QMainWindow, \
    QApplication
from PyQt5.QtCore import QEvent, Qt, QObject
from functools import partial
from random import randint

'''
We create an array of list, every element represents a button on the playing field.
Each element can have the following values:
0: not clicked and no bomb around the element
1-6: not clicked and 1 to six bombs around the elemenent
9: not clicked and bomb
if a button is pressed the value is change
10: clicked and no bomb
11-16: clicked and 1 to six bombs around the elemenent
19: place flag 
29: display bomb 
'''


class Window(QMainWindow):

    def __init__(self):
        super(Window, self).__init__()

        # set title
        self.setWindowTitle("Minesweeper")
        # set icon
        self.setWindowIcon(QtGui.QIcon('favicon.png'))

        # set initial values:
        self.cells = 20
        self.initialArray = []
        # create empty array
        for row in range(self.cells):
            line = [0]*self.cells
            self.initialArray.append(line)

        # create menu bar with menu File=>New to start a new game
        file_action = QAction("New", self)
        file_action.triggered.connect(self.init_game)
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(file_action)

        # load page at startup
        self.main_page()

        # start new game at startup
        self.init_game()

    def main_page(self):
        # create central widget
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        # create all the buttons of the minesweeper game
        self.button = {}

        horizontal_layout = QHBoxLayout(self.centralwidget)
        for column in range(0, self.cells):
            vertical_layout = QVBoxLayout()
            for row in range(0, self.cells):
                self.button[row, column] = QPushButton(self)
                self.button[row, column].setFixedHeight(20)
                self.button[row, column].setFixedWidth(20)
                self.button[row, column].setIcon(QtGui.QIcon('tile_plain.gif'))
                # set filter to detect right mouse click button
                self.button[row, column].installEventFilter(self)
                self.button[row, column].setObjectName(str(row) + ',' + str(column))
                self.button[row, column].clicked.connect(partial(self.button_pressed, row, column))
                vertical_layout.addWidget(self.button[row, column])
            horizontal_layout.addLayout(vertical_layout)
            horizontal_layout.setSpacing(0)
        self.show()
        # set screen to fixed size
        self.setFixedSize(self.size())

    def eventFilter(self, obj, event):
        # right mouse click event
        if event.type() == QEvent.MouseButtonPress:
            if event.button() == Qt.RightButton:
                row, column = obj.objectName().split(',')
                # check for flags
                if self.initialArray[int(row)][int(column)] == 19:
                    # flag present therefore remove flag
                    self.initialArray[int(row)][int(column)] = 9
                else:
                    # no flag present therefore add flag
                    self.initialArray[int(row)][int(column)] = 19
            self.update_display()
        return QObject.event(obj, event)

    def init_game(self):
        # reset counter of turns
        self.counterTurns = 0

        # initialize array with values
        self.initialArray=[[0 for i in range(self.cells)]for j in range(self.cells)]

        # add bombs and adjust surrounding cells
        for column in range(self.cells):
            for row in range(self.cells):
                # it is randomly decided whether a cell has a bomb, therefore the number of bombs is not fixed
                # the change of having a bomb can be adjusted by changing the range of randint
                bomb = randint(0, 6)
                if bomb == 0:
                    # if we have a bomb, we add 1 to the surrounding cells and write 9 to the current cell
                    self.initialArray[row][column] = 9
                    if row - 1 >= 0 and self.initialArray[row - 1][column] != 9:
                        self.initialArray[row - 1][column] += 1
                    if row + 1 <= 9 and self.initialArray[row + 1][column] != 9:
                        self.initialArray[row + 1][column] += 1
                    if column - 1 >= 0 and self.initialArray[row][column - 1] != 9:
                        self.initialArray[row][column - 1] += 1
                    if column + 1 <= 9 and self.initialArray[row][column + 1] != 9:
                        self.initialArray[row][column + 1] += 1
                    if row - 1 >= 0 and column - 1 >= 0 and self.initialArray[row - 1][column - 1] != 9:
                        self.initialArray[row - 1][column - 1] += 1
                    if row + 1 <= 9 and column - 1 >= 0 and self.initialArray[row + 1][column - 1] != 9:
                        self.initialArray[row + 1][column - 1] += 1
                    if row - 1 >= 0 and column + 1 <= 9 and self.initialArray[row - 1][column + 1] != 9:
                        self.initialArray[row - 1][column + 1] += 1
                    if row + 1 <= 9 and column + 1 <= 9 and self.initialArray[row + 1][column + 1] != 9:
                        self.initialArray[row + 1][column + 1] += 1
        # update the display to default
        self.update_display()

    def message_button(self):
        # if the button is pressed on the message box, a new game is started
        self.init_game()

    def button_pressed(self, row, column):
        # change number of turns
        self.counterTurns += 1

        # if the value is 19, a flag is on the button and the button can not be pressed
        if self.initialArray[row][column] != 19:
            # check if the clicked cell has a bomb (value=9)
            if self.initialArray[row][column] == 9:
                self.button[row, column].setIcon(QtGui.QIcon('tile_mine.gif'))
                game_busy = 0
                message = "Game over, better luck next time!"

            else:
                # call method to display all the empty cells (value=0)
                self.display_empty_buttons(row, column)
                self.update_display()

                # check whether all the cells (except bombs) are displayed
                game_busy = 0
                message = "Congratulations, you won!"
                for x in self.initialArray:
                    if any(i in range(9) for i in x):
                        game_busy = 1

            if game_busy == 0:
                # display all remaining cells when the game is finished
                for row in range(self.cells):
                    for column in range(self.cells):
                        if self.initialArray[row][column] < 9:
                            self.initialArray[row][column] += 10
                        elif self.initialArray[row][column] == 9 or self.initialArray[row][column] == 19:
                            self.initialArray[row][column] = 29
                self.update_display()

                # pop-up when the game is finished
                game_finished = QMessageBox()
                game_finished.setIcon(QMessageBox.Information)
                game_finished.setText(message)
                game_finished.setInformativeText("Number of turns: " + str(self.counterTurns))
                game_finished.setWindowTitle("Tetris")
                game_finished.setStandardButtons(QMessageBox.Ok)
                game_finished.buttonClicked.connect(self.message_button)
                game_finished.exec_()

    def display_empty_buttons(self, row, column):
        # the value of initialArray can be 0-8, 9 is for a bomb, 10-16 if it has been opened
        if self.initialArray[row][column] == 0:
            # if it is a bomb check the surrounding areas
            self.initialArray[row][column] += 10
            if row - 1 >= 0:
                self.display_empty_buttons(row - 1, column)
            if row + 1 < self.cells:
                self.display_empty_buttons(row + 1, column)
            if column - 1 >= 0:
                self.display_empty_buttons(row, column - 1)
            if column + 1 < self.cells:
                self.display_empty_buttons(row, column + 1)
            if row - 1 >= 0 and column - 1 >= 0:
                self.display_empty_buttons(row - 1, column - 1)
            if row + 1 < self.cells and column - 1 >= 0:
                self.display_empty_buttons(row + 1, column - 1)
            if row - 1 >= 0 and column + 1 < self.cells:
                self.display_empty_buttons(row - 1, column + 1)
            if row + 1 < self.cells and column + 1 < self.cells:
                self.display_empty_buttons(row + 1, column + 1)
        else:
            # if it is not a bomb just mark it as clicked
            if self.initialArray[row][column] < 9:
                self.initialArray[row][column] += 10

    def update_display(self):
        for column in range(self.cells):
            for row in range(self.cells):
                if self.initialArray[row][column] <= 9:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_plain.gif'))
                elif self.initialArray[row][column] == 10:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_clicked.gif'))
                elif self.initialArray[row][column] == 11:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_1.gif'))
                elif self.initialArray[row][column] == 12:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_2.gif'))
                elif self.initialArray[row][column] == 13:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_3.gif'))
                elif self.initialArray[row][column] == 14:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_4.gif'))
                elif self.initialArray[row][column] == 15:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_5.gif'))
                elif self.initialArray[row][column] == 16:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_6.gif'))
                elif self.initialArray[row][column] == 19:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_flag.gif'))
                elif self.initialArray[row][column] == 29:
                    self.button[row, column].setIcon(QtGui.QIcon('tile_mine.gif'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
