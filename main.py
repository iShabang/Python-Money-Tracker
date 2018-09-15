from tkinter import *
from pathlib import Path
import numpy as np
import pandas as pd
import datetime
import os

months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


class AccountGui:
    def __init__(self, window):
        self.window = window
        self.window.grid()
        Grid.columnconfigure(self.window, 0, weight=1)
        Grid.rowconfigure(self.window, 0, weight=1)
        self.main_frame = Frame(self.window)
        self.testConfig()
        self.loadConfig()
        self.main_frame.grid(sticky=W+E)
        Grid.columnconfigure(self.main_frame, 0, weight=1)
        Grid.rowconfigure(self.main_frame, 0, weight=1)
        self.homeScreen()

    def homeScreen(self):
        self.home_frame = Frame(self.main_frame)
        btn1 = Button(self.home_frame, text="Add Income", command=lambda: self.switchCurrentFile(True))
        btn2 = Button(self.home_frame, text="Add Expense", command=lambda: self.switchCurrentFile(False))
        btn3 = Button(self.home_frame, text="Summary", command=lambda: self.displaySummary(self.home_frame))
        btn4 = Button(self.home_frame, text="Quit", command = self.window.destroy)

        self.home_frame.grid(sticky=N+S+E+W)
        Grid.rowconfigure(self.home_frame, 0, weight=1)
        for x in range(1):
            Grid.columnconfigure(self.home_frame, x, weight=1)
        btn1.grid(row=0, column=0, sticky=N+S+E+W)
        btn2.grid(row=1, column=0, sticky=N+S+E+W)
        btn3.grid(row=2, column=0, sticky=N+S+E+W)
        btn4.grid(row=3, column=0, sticky=N+S+E+W)


    #switchCurrentFile simply makes the object point to a different type of input file. This done to eliminate the need
    #for separate function every time a different type of data is entered.
    def switchCurrentFile(self, entry_type):
        type_label = StringVar()
        if(entry_type):
            self.current_file = self.income_file
            type_label = "Income"
        else:
            self.current_file = self.expense_file
            type_label = "Expense"
        self.enterData(type_label)
        
    def enterData(self, type_label):
        self.home_frame.destroy()
        entry_frame = Frame(self.main_frame)
        self.ent1 = Entry(entry_frame)
        self.ent2 = Entry(entry_frame)
        self.ent3 = Entry(entry_frame)
        price_label = Label(entry_frame, text="Price")
        name_label = Label(entry_frame, text="Name")
        date_label = Label(entry_frame, text="Date")
        title = Label(entry_frame, text=type_label)
        btn_back = Button(entry_frame, text="Back", command=lambda: self.clearMove(entry_frame))

        self.ent1.bind('<Return>',self.addData)
        self.ent2.bind('<Return>',self.addData)
        self.ent3.bind('<Return>',self.addData)

        entry_frame.grid(row=1, columnspan=2, sticky=N+S+E+W)
        Grid.columnconfigure(entry_frame, 0, weight=1)
        Grid.columnconfigure(entry_frame, 1, weight=1)
        title.grid(row=0, columnspan=2, sticky=W+E)
        self.ent1.grid(row=1, column=1, sticky=W)
        self.ent2.grid(row=2, column=1, sticky=W)
        self.ent3.grid(row=3, column=1, sticky=W)
        price_label.grid(row=1, column=0, sticky=E)
        name_label.grid(row=2, column=0, sticky=E)
        date_label.grid(row=3, column=0, sticky=E)
        btn_back.grid(row=4, column=0, columnspan=2)

        self.ent1.focus()

    def addData(self, event):

        price = self.ent1.get()
        name = self.ent2.get()
        date = self.ent3.get()

        if date == "":
            print("Its empty!")
            now = datetime.datetime.now()
            date = "{}/{}/{}".format(now.month,now.day,now.year)

        f = open(self.current_file,'a')
        f.write('{},{},{}\n'.format(price,name,date))

        self.ent1.delete(0, END)
        self.ent2.delete(0, END)
        self.ent3.delete(0, END)

        self.ent1.focus()

    def clearMove(self, frame):
        frame.destroy()
        self.homeScreen()

    def displaySummary(self, del_frame):
        del_frame.destroy()
        summaryframe = Frame(self.main_frame)
        summaryframe.grid(sticky=N+S+E+W)
        Grid.columnconfigure(summaryframe, 0, weight=1)
        Grid.columnconfigure(summaryframe, 1, weight=1)
        Grid.rowconfigure(summaryframe, 0, weight=1)
        income_data = pd.read_csv(self.income_file)
        expense_data = pd.read_csv(self.expense_file)
        total_income = np.sum(income_data['Price'])
        total_expense = np.sum(expense_data['Price'])
        total_profit = total_income - total_expense

        btn1 = Button(summaryframe,text="Back",command=lambda:self.clearMove(summaryframe)).grid(row=3,columnspan=2,sticky=W+E)

        label1 = Label(summaryframe, text="Total Income").grid(row=0,column=0,sticky=E)
        label2 = Label(summaryframe, text="Total Expense").grid(row=1,column=0,stick=E)
        label3 = Label(summaryframe, text="Total Profit").grid(row=2,column=0,stick=E)
        label4 = Label(summaryframe, text=str(total_income)).grid(row=0,column=1,stick=W)
        label5 = Label(summaryframe, text=str(total_expense)).grid(row=1,column=1,stick=W)
        label6 = Label(summaryframe, text=str(total_profit)).grid(row=2,column=1,stick=W)

    def testConfig(self):
        config_file = Path('config')
        if config_file.is_file() == False:
            self.createConfig()
        
    def createConfig(self):
        date = datetime.datetime.now()
        f = open('config', 'w')
        income_file_name = 'data/{}{}_income'.format(months[date.month],date.year)
        expense_file_name = 'data/{}{}_expense'.format(months[date.month],date.year)
        f.write('{}\n{}\n{}'.format(date.month, income_file_name, expense_file_name))

    def loadConfig(self):
        config_file = open('config', 'r')
        settings = config_file.read().splitlines()
        self.month = settings[0]
        self.income_file = settings[1]
        self.expense_file = settings[2]
        try:
            os.mkdir('data')
        except OSError:
            print("Directory already exists")
        income_file_name = Path(self.income_file)
        expense_file_name = Path(self.expense_file)
        if not income_file_name.is_file():
            self.create_input_file(income_file_name)
        if not expense_file_name.is_file():
            self.create_input_file(expense_file_name)

    def create_input_file(self, filename):
        output_string = "Price,Name,Date\n"
        new_input_file = open(filename, 'w')
        new_input_file.write(output_string)
        

def main():
    root = Tk()
    root.geometry('500x400')
    a = AccountGui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
