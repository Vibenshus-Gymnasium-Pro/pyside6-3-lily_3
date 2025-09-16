import sys
import os
import random

from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QObject
from PySide6.QtGui import QPixmap

loader = QUiLoader()

class TicTacToe(QObject):
    def __init__(self):
        super().__init__()
        
        # load tic_tac_toe.ui
        basepath = os.path.dirname(__file__)
        uifile = os.path.join(basepath, "tic_tac_toe.ui")
        self.ui = loader.load(uifile, None)

        # title
        self.ui.setWindowTitle("Direkte indlæsning fra ui")

        # game_over variable to use later
        self.game_over = False

        self.button_list = []

        # find all buttons and connect to X O placement function
        for i in range (1, 10):
            button = self.ui.findChild(QPushButton, f"pushButton_{i}")
            self.button_list.append(button)
            button.clicked.connect(lambda _, b=button: self.X_O_placement(b))

        # find reset button and conect to reset function
        self.reset_button = self.ui.findChild(QPushButton, "reset_button")
        self.reset_button.clicked.connect(self.reset_game)

        # find win_label for later use and make it pink
        self.win_label = self.ui.findChild(QLabel, "win_label")
        self.win_label.setStyleSheet("color: pink;")

        # call function do figure out who starts
        self.start_player()

    def start_player(self):
        # randomly choose start player and display who starts
        self.turn_number = random.randint(0, 1)
        if self.turn_number == 0:
            self.win_label.setText("X starts")
        elif self.turn_number == 1:
            self.win_label.setText("O starts")
            
    def X_O_placement(self, button):
        
        # if game is not over and the button you are clicking has X or O is in button.text then dont do anything
        if self.game_over or button.text() != "":
            return

        # when press button make an X or an O depending on whose turn it is
        if button.text() == "" and self.turn_number % 2 == 0:
            button.setText("X")
        if not self.game_over and button.text() == "" and self.turn_number % 2 == 1:
            button.setText("O")
        
        self.turn_number += 1

        # check if someone won
        self.check_win()

        # change label
        self.change_label()

    # change label according to whose turn it is and 
    def change_label(self):
        if not self.game_over and self.turn_number % 2 == 0 and self.turn_number > 0:
            self.win_label.setText("X's turn")
        if not self.game_over and self.turn_number % 2 == 1 and self.turn_number > 0:
            self.win_label.setText("O's turn")

    def check_win(self):
        # list of lists that contains the indices to win
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # check each lines button texts 
        # and if all buttons in a line have the same text that player wins
        for i in wins:
            if all(self.button_list[j].text() == "X" for j in i):
                self.show_win("X")
                
            elif all(self.button_list[j].text() == "O" for j in i):
                self.show_win("O")

            # if all buttons/fields has something in them """but no one won then show a tie"""
            elif all(self.button_list[j].text() != "" for j in range(9)):
                self.show_win("Tie")

    # shows stuff when you win
    def show_win(self, player):
        # disable buttons after someone won
        for button in self.button_list:
            button.setEnabled(False)

        self.game_over = True

        # if it isnt a tie then display who won 
        if player != "Tie":

            # display who won and make label green
            self.win_label.setText(f"{player} Won!!!")
            self.win_label.setStyleSheet("color: green;")

            # create messagebox with who won
            msg = QMessageBox(self.ui)
            msg.setWindowTitle("Game Over")
            msg.setText(f"Player {player} Won!!!")

            # display image as the icon in the messagebox
            pixmap = QPixmap("img/yayy.jfif")
            msg.setIconPixmap(pixmap)

            msg.setStyleSheet("QLabel { font-size: 30px; color: Green; }")
            msg.exec()

        else:
            #set label to it 
            self.win_label.setText(f"It is a {player}")

    def reset_game(self):
        # remove all X and O's 
        for button in self.button_list:
            button.setText("")
            button.setEnabled(True)

        # reset game_over variable
        self.game_over = False

        # turn number and win label reset
        self.start_player()
        
        # reset win_label 
        self.win_label.setStyleSheet("color: pink;")

program = QApplication.instance()
if program == None:
    program = QApplication(sys.argv)
roeversprogsoversaetter = TicTacToe()
roeversprogsoversaetter.ui.show()
program.exec()