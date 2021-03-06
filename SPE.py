import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from typing import Any, Union
from collections import OrderedDict
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib import style, use
import pandas as pd
import numpy as np
from pandas import DataFrame, Series
from pandas.io.parsers import TextFileReader

style.use('ggplot')
use('TkAgg')

path = 'graph.png'
LARGE_FONT = ('RobotoMono-Medium', 15)
bg = '#282c34'


def TryExcept(tryFunc):
    try:
        print('using TryExcept')
        return tryFunc()

    except AttributeError:
        print('Attribute Error Found')


class SPE_src(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.config(self, bg=bg)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        menuBar = tk.Menu(container)
        fileMenu = tk.Menu(menuBar, tearoff=False)
        fileMenu.add_command(label='Save Settings', command=lambda: self.popupmsg('Not Supported Yet.'))
        fileMenu.add_separator()
        fileMenu.add_command(label='Close', command=quit)
        graphMenu = tk.Menu(menuBar, tearoff=False)
        graphMenu.add_command(label='Bar', )
        graphMenu.add_command(label='Pie', )
        graphMenu.add_command(label='line', )
        menuBar.add_cascade(label='File', menu=fileMenu)
        menuBar.add_cascade(label='Graph', menu=graphMenu)
        tk.Tk.config(self, menu=menuBar)
        tk.Tk.config(self, menu=menuBar)

        DT = ttk.Style()
        DT.configure('TButton', foreground='black', borderwidth=1, focusthickness=3,
                     focuscolor='none')
        DT.map('TButton', background=[('active', 'red')])
        self.frames = {}
        for F in (StartPage, StudOptionFrame, StudentORTeacher, TchrOptionFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg=bg)
        label = tk.Label(self, text='Students Performance Evaluation', font=LARGE_FONT, bg=bg, fg='white')
        label.grid(columnspan=2, pady=10)
        self.img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self, image=self.img, bg=bg, relief=tk.RIDGE)
        panel.grid(rowspan=2, padx=25, pady=25)
        agreement = 'By Clicking on next you hereby \n' \
                    'Agree to use our policy\nWe assure you that we won\'t sell out\nyour data. ' \
                    'It will only be used to improve this\nsoftware. \n\nEnjoy using this Software!'
        agmtText = tk.Label(self, text=agreement, bg=bg, font=LARGE_FONT, fg='white', relief=tk.RIDGE)
        agmtText.grid(row=1, column=1, padx=25, ipadx=20, ipady=50)
        CloseBtn = tk.ttk.Button(self, text='Exit', command=lambda: exit())
        CloseBtn.grid(row=2, column=1, sticky='SE', padx=125, pady=25)
        NextBtn = tk.ttk.Button(self, text='Next', command=lambda: controller.show_frame(StudentORTeacher))
        NextBtn.grid(row=2, column=1, sticky='SE', padx=25, pady=25, )


class StudentORTeacher(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg='#282c34')
        label = tk.Label(self, text='Who are you?', font=LARGE_FONT, bg=bg, fg='white')
        label.grid(columnspan=3, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StartPage))
        back.grid(row=0, columnspan=3, sticky='NW', padx=20, pady=20)
        self.studImg = ImageTk.PhotoImage(Image.open('student.png'))
        self.teachImg = ImageTk.PhotoImage(Image.open('teacher.png'))
        Student = tk.Button(self, text='Student', bg=bg, relief=tk.RIDGE, image=self.studImg, command=lambda: controller.show_frame(StudOptionFrame))
        Student.grid(row=2, column=1, padx=50, pady=25, )
        Teacher = tk.Button(self, text='Teacher', bg=bg, relief=tk.RIDGE, image=self.teachImg, command=lambda: controller.show_frame(TchrOptionFrame))
        Teacher.grid(row=2, column=2, padx=25, pady=25,)


class StudOptionFrame(tk.Frame):
    data: Union[Union[TextFileReader, Series, DataFrame, None], Any]

    def __init__(self, parent, controller):
        self.file = ''
        self.SeatNum = tk.StringVar()
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg=bg)
        label = tk.Label(self, text='Student', font=LARGE_FONT, bg=bg, fg='white')
        label.grid(row=0, column=1, padx=100, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=0, pady=10)
        SeatNumEntry = tk.ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=1, column=0, sticky='NW', padx=5, pady=125)
        addFileBtn = tk.ttk.Button(self, text='Add File', command=lambda: self.getFile())
        addFileBtn.grid(row=1, column=0, pady=150)
        self.fileStatus = tk.Label(self, text='Add a File', bg=bg, fg='white')
        self.fileStatus.grid(row=1, column=1)
        SubVSMks = tk.ttk.Button(self, text='Subject VS Marks', command=lambda: self.marks_wrt_subject())
        SubVSMks.grid(row=1, column=2)
        AllSem = tk.ttk.Button(self, text='Your Performance VS Class', command=lambda: self.all_sem_performance())
        AllSem.grid(row=1, column=2, pady=115, sticky='N')
        IndStud = tk.ttk.Button(self, text='Individual Student', command=lambda: self.IndStud())
        IndStud.grid(row=1, column=2, pady=80, sticky='N')

    def getFile(self):
        self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                               filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
        if self.file == '':
            self.fileStatus.config(text='No File Added'.upper())
            self.fileStatus.config(fg='#FF0000')
        else:
            self.fileStatus.config(text='File Added'.upper())
            self.fileStatus.config(fg='#00FF00')
            self.data = pd.read_csv(self.file)
            self.SeatData = np.array(self.data['Seat No'])

    def marks_wrt_subject(self):
        if self.file != '' and self.SeatNum.get() != '':
            col = self.data.columns
            subjects = self.data[col[0]]
            marks = self.data[col[1]]
            plt.xticks(np.arange(len(subjects)), subjects)
            plt.title("Student's data")
            plt.xlabel(col[0])
            plt.ylabel('Marks')
            plt.bar(subjects, marks)
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def all_sem_performance(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            col = data.columns
            Subjects = [''.join(list(c)[:-6]) for c in col][3:10]
            SubjectData = []
            Student = []
            for i in range(0, len(self.SeatData), 6):
                idx = pd.Index(self.SeatData)
                locData = idx.get_loc(self.SeatData[i])
                StudentData = data.loc[locData + 2, :]
                OneData = np.array(StudentData[3:10]).astype(np.int)
                if self.SeatData[i] == self.SeatNum.get().upper():
                    Student = np.array(StudentData[3:10]).astype(np.int)
                SubjectData.append(OneData)
            SubjectData = np.transpose(SubjectData)
            MaxOfAll = [np.max(i) for i in SubjectData]
            AvgOfAll = [np.average(i) for i in SubjectData]
            plt.title('Your Performance vs Class')
            plt.bar(np.arange(7) + 0.00, MaxOfAll, color='#004c6d', width=0.25)
            plt.bar(np.arange(7) + 0.25, AvgOfAll, color='#286d8a', width=0.25)
            plt.bar(np.arange(7) + 0.50, Student, color='#008cc9', width=0.25)
            plt.xticks(np.arange(7), Subjects)
            plt.legend(labels=['Max', 'Average', self.SeatNum.get().upper()])
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def IndStud(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            col = data.columns
            idx = pd.Index(self.SeatData)
            locData = idx.get_loc(self.SeatNum.get().upper())
            StudentData = data.loc[locData + 2, :]
            SubjectData = np.array(StudentData[3:10]).astype(np.int)
            Subjects = [''.join(list(c)[:-6]) for c in col][3:10]
            plt.ylim(0, 100)
            plt.bar(Subjects, SubjectData)
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')


class TchrOptionFrame(tk.Frame):
    data: Union[Union[TextFileReader, Series, DataFrame, None], Any]

    def __init__(self, parent, controller):
        self.file = ''
        self.SeatNum = tk.StringVar()
        tk.Frame.__init__(self, parent)
        tk.Frame.config(self, bg=bg)
        label = tk.Label(self, text='Teacher', font=LARGE_FONT, bg=bg, fg='white')
        label.grid(row=0, column=1, padx=100, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=0, pady=10)
        SeatNumEntry = tk.ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=1, column=0, sticky='NW', padx=5, pady=125)
        addFileBtn = tk.ttk.Button(self, text='Add File', command=lambda: self.getFile())
        addFileBtn.grid(row=1, column=0, pady=150)
        self.fileStatus = tk.Label(self, text='Add a File', bg=bg, fg='white')
        self.fileStatus.grid(row=1, column=1)
        ClassPer = tk.ttk.Button(self, text='Class Performance', command=lambda: TryExcept(self.ClassPerformance))
        ClassPer.grid(row=1, column=2)
        ClassGrowth = tk.ttk.Button(self, text='Class Growth', command=lambda: TryExcept(self.ClassGrowth))
        ClassGrowth.grid(row=1, column=2, pady=115, sticky='N')
        Top3 = tk.ttk.Button(self, text='Top 5', command=lambda: TryExcept(self.Top3))
        Top3.grid(row=1, column=2, pady=80, sticky='N')

    def getFile(self):
        self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                               filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
        if self.file == '':
            self.fileStatus.config(text='No File Added'.upper(), fg='red')
        else:
            self.fileStatus.config(text='File Added'.upper(), fg='green')
            self.data = pd.read_csv(self.file)

    def ClassPerformance(self):
        if self.file != '':
            grade = np.array(self.data.Grade)[2::6]
            u, c = np.unique(grade, return_counts=True)
            GradeCount = dict(zip(u, c))
            plt.title("Student's data")
            plt.pie(GradeCount.values(), labels=GradeCount.keys(), autopct='%.2f %%', explode=np.array([0.03] * len(GradeCount)))
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')

    def ClassGrowth(self):
        if self.file != '':
            semData = [np.mean(self.data.iloc[:, i]) for i in range(1, len(self.data.columns) - 1)]
            plt.plot(semData)
            plt.ylim(5, 10)
            plt.legend(labels=['Growth in avg. CGPA '])
            plt.xticks(np.arange(6), ['I', 'II', 'III', 'IV', 'V', 'VI'])
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')

    def Top3(self):
        if self.file != '':
            Total = self.data['Total [ 20 ]'][2::6]
            SeatNo = self.data['Seat No'][::6]
            StudentData = sorted(list(zip(Total, SeatNo)))
            SeatValue = [StudentData[-5:][i][1] for i in range(5)]
            Marks = [StudentData[-5:][i][0] for i in range(5)]
            plt.bar(SeatValue,  Marks)
            plt.ylim(min(Marks)-50, max(Marks)+50)
            plt.show()


app = SPE_src()
app.resizable(width=0, height=0)
app.title('Students Performance Evaluation')
# app.geometry('1280x720')
app.mainloop()
