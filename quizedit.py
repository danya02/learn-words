#!/usr/bin/python3
from tkinter import *
from tkinter import filedialog
import json

class ScrollCanvas(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)
        self.canvas = Canvas(root)
        self.canvas.pack(side=LEFT)
        #self.canvas.grid(row=0, column=0)

        self.scrollbar = Scrollbar(root, command=self.canvas.yview)
        self.scrollbar.pack(side=LEFT, fill="y")
        #self.scrollbar.grid(row=0, column=1)

        self.canvas.configure(yscrollcommand = self.scrollbar.set)

        self.canvas.bind('<Configure>', self.onFrameConfigure)
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')


    def onFrameConfigure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.scanvas = ScrollCanvas(self)
        self.scanvas.place()
        self.loadbutton = Button(self.scanvas.frame, text="Load...", command=self.load_data)
        self.loadbutton.grid(row=0, column=0)
        self.savebutton = Button(self.scanvas.frame, text="Save...", command=self.save_data)
        self.savebutton.grid(row=0, column=1)
        self.addbutton = Button(self.scanvas.frame, text=" "*10 + "+" + " "*10, command=self.add_row)
        self.addbutton.grid(row=1, column=0, columnspan=2)
        self.bind("<Motion>", self.scanvas.onFrameConfigure)
        self.objects = []
        self.config = {}
        self.max_row = 0

    def load_data(self):
        self.config = json.load(filedialog.askopenfile(mode="r"))["quizzes"][0]["questions"]
        self.load_fields2()
    def save_data(self):
        json.dump({"quizzes": [{"questions": self.config}]}, filedialog.asksaveasfile(mode="w"), sort_keys=True, indent=4)
    def update_values(self, *args):
        self.config.clear()
        for i in self.objects:
            self.config.update({i[4].get(): i[5].get()})
    def delete_row(self, row):
        for i in self.objects:
            if i[0] == row:
                i[1].destroy()
                i[2].destroy()
                i[3].destroy()
                self.objects.remove(i)
                break
        self.scanvas.onFrameConfigure(None)
    def add_row(self):
        self.addbutton.destroy()
        n = StringVar()
        n.trace("w", self.update_values)
        o = StringVar()
        o.trace("w", self.update_values)
        k = Entry(self.scanvas.frame, textvariable=n)
        l = Entry(self.scanvas.frame, textvariable=o)
        row = max(len(self.objects), self.max_row)+1
        self.max_row = row
        k.grid(column=0, row=row)
        l.grid(column=1, row=row)
        m = Button(self.scanvas.frame, text="X", command=lambda:self.delete_row(row))
        m.grid(column=2, row=row)
        self.objects += [(row, k, l, m, n, o)]
        self.addbutton = Button(self.scanvas.frame, text=" "*10 + "+" + " "*10, command=self.add_row)
        self.addbutton.grid(column=0, row=self.max_row+1, columnspan=2)
        self.scanvas.onFrameConfigure(None)

    def load_fields(self):
        self.addbutton.destroy()
        for i in self.objects:
            i[1].destroy()
            i[2].destroy()
            i[3].destroy()
        self.objects.clear()
        for i, j in zip(self.config.keys(), self.config.values()):
            k = Entry(self.scanvas.frame)
            k.insert(0, i)
            l = Entry(self.scanvas.frame)
            l.insert(0, j)
            row = max(len(self.objects), self.max_row)+1
            self.max_row = row
            k.grid(column=0, row=row)
            l.grid(column=1, row=row)
            m = Button(self, text="X", command=lambda:self.delete_row(row))
            m.grid(column=2, row=row)
            self.objects += [(row, k, l, m)]
        self.addbutton = Button(self.scanvas.frame, text="+", command=self.add_row)
        self.addbutton.grid(column=0, row=self.max_row+1, columnspan=2)
    def load_fields2(self):
        self.addbutton.destroy()
        for i in self.objects:
            i[1].destroy()
            i[2].destroy()
            i[3].destroy()
        self.objects.clear()
        self.objects.clear()
        for i, j in zip(self.config.keys(), self.config.values()):
            self.add_row()
            self.objects[-1][1].insert(0, i)
            self.objects[-1][2].insert(0, j)


root = App()
root.mainloop()
