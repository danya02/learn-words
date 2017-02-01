#!/usr/bin/python3
import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QCoreApplication
import random
import json


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("quiz.ui", self)

        self.__set_properties()
        self.conf = json.load(open("config.json"))
        self.quiz = self.conf["quizzes"][0]
        self.show()

    def __set_properties(self):
        self.ui.button_1.clicked.connect(self.ask_question)
        self.ui.button_2.clicked.connect(self.ask_question)
        self.ui.button_3.clicked.connect(self.ask_question)
        self.ui.button_4.clicked.connect(self.ask_question)

    def right_answer(self, null):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("You answered the question correctly!")
        msg.setWindowTitle("Correct answer!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
        for i in [self.ui.button_1, self.ui.button_2, self.ui.button_3, self.ui.button_4]:
            i.setText("RESTART")
            i.clicked.disconnect()
            i.clicked.connect(self.ask_question)
        self.ui.label_1.setText("Press any of the buttons to ask another question.")

    def wrong_answer(self, null):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("You gave an incorrect answer!")
        msg.setWindowTitle("Wrong answer!")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def ask_question(self, null):
        buttons = [self.ui.button_1, self.ui.button_2, self.ui.button_3, self.ui.button_4]
        str_question = random.choice(list(self.quiz["questions"].keys()))
        str_answer = self.quiz["questions"][str_question]
        str_question = self.quiz["question_form"].format(str_question)
        print(str_question, str_answer)
        false_answers = []
        for i in range(3):
            a = random.choice(list(self.quiz["questions"].values()))
            if not a == str_answer and a not in false_answers:
                false_answers += [a]
        random.shuffle(buttons)
        true_button = buttons.pop(random.randint(0, len(buttons)-1))
        false_buttons = buttons
        self.ui.label_1.setText(str_question)
        true_button.setText(str_answer)
        true_button.clicked.disconnect()
        true_button.clicked.connect(self.right_answer)
        for i, j in zip(false_answers, false_buttons):
            j.setText(i)
            j.clicked.disconnect()
            j.clicked.connect(self.wrong_answer)

app = QApplication(sys.argv)
top = App()
sys.exit(app.exec_())
