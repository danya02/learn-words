#!/usr/bin/python3
import wx
import random
import json


class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        wx.Frame.__init__(self, *args, **kwds)
        self.label_1 = wx.StaticText(self, wx.ID_ANY, (
            "Press any of the buttons to begin."))
        self.button_1 = wx.Button(self, wx.ID_ANY, ("START"))
        self.button_2 = wx.Button(self, wx.ID_ANY, ("START"))
        self.button_3 = wx.Button(self, wx.ID_ANY, ("START"))
        self.button_4 = wx.Button(self, wx.ID_ANY, ("START"))

        self.__set_properties()
        self.__do_layout()
        self.conf = json.load(open("config.json"))
        self.quiz = self.conf["quizzes"][0]

    def __set_properties(self):
        self.SetTitle(("Quiz"))
        self.SetFocus()
        self.button_1.Bind(wx.EVT_BUTTON, self.ask_question)
        self.button_2.Bind(wx.EVT_BUTTON, self.ask_question)
        self.button_3.Bind(wx.EVT_BUTTON, self.ask_question)
        self.button_4.Bind(wx.EVT_BUTTON, self.ask_question)

    def __do_layout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(2, 2, 0, 0)
        sizer_1.Add(self.label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.EXPAND, 0)
        grid_sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_2, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_3, 0, wx.ALIGN_CENTER, 0)
        grid_sizer_1.Add(self.button_4, 0, wx.ALIGN_CENTER, 0)
        sizer_1.Add(grid_sizer_1, 1, 0, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def right_answer(self):
        c = wx.MessageBox("You answered the question correctly!", "Correct answer!")
        c.ShowModal()
        c.destroy()
        for i in [self.button_1, self.button_2, self.button_3, self.button_4]:
            i.SetValue("RESTART")
            i.Bind(wx.EVT_BUTTON, self.ask_question)
        self.label_1.SetValue("Press any of the buttons to ask another question.")

    def wrong_answer(self):
        c = wx.MessageBox("You gave an incorrect answer!", "Wrong answer!", wx.ICON_ERROR)
        c.ShowModal()
        c.destroy()

    def ask_question(self):
        buttons = [self.button_1, self.button_2, self.button_3, self.button_4]
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
        self.label_1.SetValue(str_question)
        true_button.SetValue(str_answer)
        true_button.Bind(wx.EVT_BUTTON, self.right_answer)
        for i, j in zip(false_answers, false_buttons):
            j.SetValue(i)
            j.Bind(wx.EVT_BUTTON, self.wrong_answer)

app = wx.App(redirect=True)
top = MyFrame()
top.Show()
app.MainLoop()
