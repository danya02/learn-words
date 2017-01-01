#!/usr/bin/python3
from tkinter import *
from tkinter import messagebox
import random
import json
conf = json.load(open("config.json"))
quiz = conf["quizzes"][0]
root = Tk()
text = Text(root, wrap=WORD, height=1)
text.grid(row=0, column=0, columnspan=2)
button1 = Button(root, text="START", width=32)
button1.grid(row=1, column=0)
button2 = Button(root, text="START", width=32)
button2.grid(row=1, column=1)
button3 = Button(root, text="START", width=32)
button3.grid(row=2, column=0)
button4 = Button(root, text="START", width=32)
button4.grid(row=2, column=1)


def update_text(field, newtext):
    if isinstance(field, Text):
        field.config(state=NORMAL)
        field.delete("0.0", END)
        field.insert(END, newtext)
        field.config(state=DISABLED)
    else:
        field.config(text=newtext)

update_text(text, "Press any of the buttons to begin.")


def right_answer():
    global button1
    global button2
    global button3
    global button4
    global text
    messagebox.showinfo("Correct answer!",
                        "You answered the question correctly!")
    for i in [button1, button2, button3, button4]:
        update_text(i, "RESTART")
        i.config(command=ask_question)
    update_text(text, "Press any of the buttons to ask another question.")


def wrong_answer():
    messagebox.showerror("Wrong answer!",
                         "You gave an incorrect answer!")


def ask_question():
    global quiz
    global text
    global button1
    global button2
    global button3
    global button4
    buttons = [button1, button2, button3, button4]
    str_question = random.choice(list(quiz["questions"].keys()))
    str_answer = quiz["questions"][str_question]
    str_question = quiz["question_form"].format(str_question)
    print(str_question, str_answer)
    false_answers = []
    for i in range(3):
        a = random.choice(list(quiz["questions"].values()))
        if not a == str_answer and a not in false_answers:
            false_answers += [a]
    random.shuffle(buttons)
    true_button = buttons.pop(random.randint(0, len(buttons)-1))
    false_buttons = buttons
    update_text(text, str_question)
    update_text(true_button, str_answer)
    true_button.config(command=right_answer)
    for i, j in zip(false_answers, false_buttons):
        update_text(j, i)
        j.config(command=wrong_answer)
    true_button.flash()

button1.config(command=ask_question)
button2.config(command=ask_question)
button3.config(command=ask_question)
button4.config(command=ask_question)

root.mainloop()
