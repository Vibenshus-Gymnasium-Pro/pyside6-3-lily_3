import sys
import os
import random

from PySide6.QtWidgets import QApplication, QLabel, QPushButton
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QObject

loader = QUiLoader()

class TicTacToe(QObject):
    def __init__(self):
        super().__init__()
        
        basepath = os.path.dirname(__file__)
        uifile = os.path.join(basepath, "tic_tac_toe.ui")
        self.ui = loader.load(uifile, None)
        # title
        self.ui.setWindowTitle("Direkte indlæsning fra ui")

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
            
    # when press button make an X or an O depending on whose turn it is
    def X_O_placement(self, button):
        if button.text() == "" and self.turn_number % 2 == 0:
            button.setText("X")
        if button.text() == "" and self.turn_number % 2 == 1:
            button.setText("O")
        self.turn_number += 1

        #check if someone won
        self.check_win()

    def check_win(self):
        # list of lists that contains the indices to win
        wins = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

        # check each lines button texts 
        # and if all buttons in a line have the same text that player wins
        for i in wins:
            if all(self.button_list[j].text() == "X" for j in i):
                self.win_label.setText("X Won!!!")
                
                # disable buttons after someone won
                for button in self.button_list:
                    button.setEnabled(False)

                # make label green
                self.win_label.setStyleSheet("color: green;")

            elif all(self.button_list[j].text() == "O" for j in i):
                self.win_label.setText("O Won!!!")

                # disable buttons after someone won
                for button in self.button_list:
                    button.setEnabled(False)

                # make label green
                self.win_label.setStyleSheet("color: green;")

    def reset_game(self):
        # remove all X and O's 
        for button in self.button_list:
            button.setText("")
            button.setEnabled(True)

        # turn number and win label reset
        self.start_player()

        self.win_label.setStyleSheet("color: pink;")

program = QApplication.instance()
if program == None:
    program = QApplication(sys.argv)
roeversprogsoversaetter = TicTacToe()
roeversprogsoversaetter.ui.show()
program.exec()
