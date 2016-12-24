#!/usr/bin/python3
from tkinter import *
import json
import re
conf = json.load(open("config.json"))
top = Tk()
text = Text(top, wrap=WORD)
text.pack(side=LEFT, fill=Y)
scrollbar = Scrollbar(top, command=text.yview)
scrollbar.pack(side=RIGHT, fill=Y)
text.config(yscrollcommand=scrollbar.set)
button = Button(top, text="Swap")
button.pack(side=BOTTOM, fill=X)
swapped = False
init_text = conf["texts"][0]


def subst(inp_text, subst_char, subst_str, split_symb=" ", out_split_symb=" "):
    sp_text = inp_text.split(split_symb)
    for i in range(len(sp_text)):
        if subst_char in sp_text[i]:
            sp_text[i] = subst_str
    return out_split_symb.join(sp_text)


def update_text_field(field, text):
    field.config(state=NORMAL)
    field.delete("0.0", END)
    field.insert(END, text)
    field.config(state=DISABLED)


def swap_text():
    global init_text
    global swapped
    global text
    textst = init_text["text"]
    for i in init_text["substs"]:
        textst = textst.replace(i[0], "") if swapped else subst(
            textst, i[0], i[1])
    swapped = not swapped
    update_text_field(text, textst)

button.config(command=swap_text)

if __name__ == '__main__':
    top.mainloop()
