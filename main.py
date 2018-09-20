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
        self.main_frame = Frame(self.window)
        Grid.columnconfigure(self.window, 0, weight=1)
        Grid.columnconfigure(self.main_frame, 0, weight=1)
        Grid.rowconfigure(self.window, 0, weight=1)
        Grid.rowconfigure(self.main_frame, 0, weight=1)
        self.main_frame.grid(sticky=W+E)
        self.window.grid()
        self.makeDirectories()
        if not self.testConfig():
            self.createConfig()
            self.createTimeList('year')
            self.createTimeList('month')
        self.loadConfig()
        self.yearScreen()

    def homeScreen(self):
        self.current_income_file = Path("files/{}{}_income.csv".format(months[int(self.current_month)],self.current_year))
        self.current_expense_file = Path("files/{}{}_expense.csv".format(months[int(self.current_month)],self.current_year))
        self.home_frame = Frame(self.main_frame)
        btn1 = Button(self.home_frame, text="Add Income", command=lambda: self.switchCurrentFile("Income"))
        btn2 = Button(self.home_frame, text="Add Expense", command=lambda: self.switchCurrentFile("Expense"))
        btn3 = Button(self.home_frame, text="Summary", command=lambda: self.displaySummary(self.home_frame))
        btn4 = Button(self.home_frame, text="Quit", command = self.window.destroy)
        btn5 = Button(self.home_frame, text="Display Income", command=lambda: self.displayFileContents(self.current_income_file,self.home_frame))
        btn6 = Button(self.home_frame, text="Display Expense", command=lambda: self.displayFileContents(self.current_expense_file,self.home_frame))

        self.home_frame.grid(sticky=N+S+E+W)
        Grid.rowconfigure(self.home_frame, 0, weight=1)
        for x in range(1):
            Grid.columnconfigure(self.home_frame, x, weight=1)
        btn1.grid(row=0, column=0, sticky=N+S+E+W)
        btn2.grid(row=1, column=0, sticky=N+S+E+W)
        btn3.grid(row=2, column=0, sticky=N+S+E+W)
        btn4.grid(row=5, column=0, sticky=N+S+E+W)
        btn5.grid(row=3, column=0, sticky=N+S+E+W)
        btn6.grid(row=4, column=0, sticky=N+S+E+W)

    def yearScreen(self):
        self.year_frame = Frame(self.main_frame)
        self.year_frame.grid(sticky=N+S+E+W)
        Grid.columnconfigure(self.year_frame, 0, weight=1)
        self.loadYearList()
        i = 0
        for year in self.year_list:
            btn = Button(self.year_frame, text=year, command=lambda: self.yearButtonFunctions(year))
            btn.grid(row=i, column=0, sticky=N+S+E+W)
            i = i+1
        quit_button = Button(self.year_frame, text="Quit", command=self.window.destroy)
        quit_button.grid(row=i, column=0, sticky=N+S+E+W)

    def changeCurrentYear(self, year):
        self.current_year = year

    def yearButtonFunctions(self, year):
        self.year_frame.destroy()
        self.changeCurrentYear(year)
        self.monthScreen()

    def monthScreen(self):
        self.month_frame = Frame(self.main_frame)
        self.month_frame.grid(sticky=N+S+E+W)
        Grid.columnconfigure(self.month_frame, 0, weight=1)
        self.loadMonthList()
        i=0
        for month in self.month_list:
            btn = Button(self.month_frame, text=months[int(month)], command=lambda :self.monthButtonFunctions(month))
            btn.grid(row=i,column=0,sticky=N+S+E+W)
            i=i+1
        quit_button = Button(self.month_frame, text="Quit", command=self.window.destroy)
        quit_button.grid(row=i, column=0, sticky=N+S+E+W)

    def monthButtonFunctions(self,month):
        self.month_frame.destroy()
        self.changeCurrentMonth(month)
        self.homeScreen()

    def changeCurrentMonth(self,month):
        self.current_month = month

    def switchCurrentFile(self, entry_type):
        if(entry_type=="Income"):
            self.current_file = self.current_income_file
        elif(entry_type=="Expense"):
            self.current_file = self.current_expense_file
        self.enterData(entry_type)
        
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
            now = datetime.datetime.now()
            date = "{}/{}/{}".format(now.month,now.day,now.year)
        if not self.current_file.is_file():
            self.createInputFile(self.current_file)
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
        summary_frame = Frame(self.main_frame)
        summary_frame.grid(sticky=N+S+E+W)
        Grid.columnconfigure(summary_frame, 0, weight=1)
        Grid.columnconfigure(summary_frame, 1, weight=1)
        Grid.rowconfigure(summary_frame, 0, weight=1)
        total_income = 0
        total_expense = 0
        total_profit = 0
        try:
            income_data = pd.read_csv(self.current_income_file)
            expense_data = pd.read_csv(self.current_expense_file)
            total_income = np.sum(income_data['Price'])
            total_expense = np.sum(expense_data['Price'])
        except OSError:
            print("File does not exist")

        total_profit = total_income - total_expense
        btn1 = Button(summary_frame,text="Back",command=lambda:self.clearMove(summary_frame)).grid(row=3,columnspan=2,sticky=W+E)

        label1 = Label(summary_frame, text="Total Income").grid(row=0,column=0,sticky=E)
        label2 = Label(summary_frame, text="Total Expense").grid(row=1,column=0,stick=E)
        label3 = Label(summary_frame, text="Total Profit").grid(row=2,column=0,stick=E)
        label4 = Label(summary_frame, text=str(total_income)).grid(row=0,column=1,stick=W)
        label5 = Label(summary_frame, text=str(total_expense)).grid(row=1,column=1,stick=W)
        label6 = Label(summary_frame, text=str(total_profit)).grid(row=2,column=1,stick=W)

    def displayFileContents(self, filename, del_frame):
        del_frame.destroy()
        data = pd.read_csv(filename)
        display_frame = Frame(self.main_frame)
        display_frame.grid(sticky=N+S+E+W)
        Grid.columnconfigure(display_frame, 0, weight=1)
        text = Text(display_frame, height=10)
        #text = Text(display_frame)
        text.insert(END, data)
        text.grid(sticky=N+S+E+W)
        back_button = Button(display_frame,text="Back",command=lambda:self.clearMove(display_frame))
        back_button.grid(row=2,sticky=N+S+E+W)

    def addNewMonth(self,year,month):
        month_file_path = ('Program Data/{}/month'.format(year))
        month_file = open(month_file_path, 'a')
        if month:
            month_file.write(months[month])
        else:
            date = datetime.datetime.now()
            month_file.write(months[date.month])
    
    def fileTest(self, filename):
        test_file = Path(filename)
        if test_file.is_file():
            return True
        else:
            return False
            

    def makeDirectories(self):
        date = datetime.datetime.now()

        try:
            os.makedirs('Program Data/{}'.format(date.year))
        except OSError:
            print("Directory already exists")

        try:
            os.mkdir('files')
        except OSError:
            print("Directory already exists")
            

    def checkMonth(self):
        date = datetime.datetime.now()
        if self.month != date.month:
            return False
        else:
            return True

    def testConfig(self):
        config_file = Path('config')
        if not config_file.is_file():
            return False
        else:
            return True

    def createConfig(self):
        config_file = open('config', 'w')
        config_file.close()

    def createTimeList(self, time_type):
        date = datetime.datetime.now()
        if time_type == 'year':
            file_path = Path('Program Data/year')
        elif time_type == 'month':
            file_path = Path('Program Data/{}/month'.format(date.year))

        if file_path.is_file():
            print('{} already exists'.format(file_path))
            return

        time_file = open(file_path, 'w')
        if time_type == 'year':
            time_file.write('{}\n'.format(date.year))
        elif time_type == 'month':
            time_file.write('{}\n'.format(date.month))
        time_file.close()

    def loadMonthList(self):
        date = datetime.datetime.now()
        month_file = open('Program Data/{}/month'.format(self.current_year), 'r')
        self.month_list = month_file.read().splitlines()
        month_file.close()
        if self.month_list[-1] != str(date.month):
            month_file = open('Program Data/{}/month'.format(self.current_year), 'w')
            month_file.write('{}\n'.format(date.month))
            month_file.cloe()
            self.month_list.append(str(date.month))
            

    def loadYearList(self):
        date = datetime.datetime.now()
        year_file = open('Program Data/year', 'r')
        self.year_list = year_file.read().splitlines()
        year_file.close()
        if self.year_list[-1] != str(date.year):
            year_file = open('Program Data/year', 'a')
            year_file.write('{}\n'.format(date.year))
            year_file.close()
            self.year_list.append(str(date.year))
        

    def loadConfig(self):
        print("config loaded")
        #config_file = open('config', 'r')
        #settings = config_file.read().splitlines()

    def createInputFile(self, filename):
        output_string = "Price,Name,Date\n"
        new_input_file = open(filename, 'w')
        new_input_file.write(output_string)
        

def main():
    root = Tk()
    root.geometry('220x205')
    a = AccountGui(root)
    root.mainloop()

if __name__ == '__main__':
    main()
