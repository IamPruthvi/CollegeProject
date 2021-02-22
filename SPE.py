import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib import style, use
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import pandas as pd
import numpy as np

style.use('ggplot')

use('TkAgg')

path = 'graph.png'
LARGE_FONT = ('RobotoMono-Medium', 13)
graphType = None


def TryExcept(tryFunc):
    try:
        print('using TryExcept')
        return tryFunc()

    except AttributeError:
        print('Error Found')


class SPE_src(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
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
        self.frames = {}
        for F in (StartPage, StudOptionFrame, StudentORTeacher, TchrOptionFrame):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    @staticmethod
    def popupmsg(msg):
        popup = tk.Tk()
        popup.wm_title('Save Settings')
        label = tk.ttk.Label(popup, text=msg, )
        label.pack()
        b1 = tk.ttk.Button(popup, text='Close', command=popup.destroy)
        b1.pack()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Students Performance Evaluation', font=LARGE_FONT)
        label.grid(columnspan=2, pady=10)
        self.img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self, image=self.img, relief=tk.RIDGE)
        panel.grid(rowspan=2, padx=25, pady=25)
        agreement = 'By Clicking on next you hereby \n' \
                    'Agree to use our policy\nWe assure you that we won\'t sell out\nyour data. ' \
                    'It will only be used to improve this\nsoftware. \n\nEnjoy using this Software!'
        agmtText = tk.Label(self, text=agreement, bg='white', font=LARGE_FONT, relief=tk.RIDGE)
        agmtText.grid(row=1, column=1, padx=25, ipadx=20, ipady=50)
        CloseBtn = tk.ttk.Button(self, text='Exit', command=lambda: exit())
        CloseBtn.grid(row=2, column=1, sticky='SE', padx=125, pady=25, )
        NextBtn = tk.ttk.Button(self, text='Next', command=lambda: controller.show_frame(StudentORTeacher))
        NextBtn.grid(row=2, column=1, sticky='SE', padx=25, pady=25, )


class StudentORTeacher(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Who are you?', font=LARGE_FONT)
        label.grid(columnspan=3, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StartPage))
        back.grid(row=0, columnspan=3, sticky='NW', padx=20, pady=20)
        self.studImg = ImageTk.PhotoImage(Image.open('student.png'))
        panel = tk.Label(self, image=self.studImg, relief=tk.RIDGE)
        panel.grid(row=1, column=1, padx=25, pady=25)
        self.teachImg = ImageTk.PhotoImage(Image.open('teacher.png'))
        panel = tk.Label(self, image=self.teachImg, relief=tk.RIDGE)
        panel.grid(row=1, column=2, padx=25, pady=25)  # r = --- c = ||||
        Student = tk.ttk.Button(self, text='Student', command=lambda: controller.show_frame(StudOptionFrame))
        Student.grid(row=2, column=1, padx=125, pady=25, )
        Teacher = tk.ttk.Button(self, text='Teacher', command=lambda: controller.show_frame(TchrOptionFrame))
        Teacher.grid(row=2, column=2, padx=25, pady=25, )


class StudOptionFrame(tk.Frame):
    def __init__(self, parent, controller):
        self.file = ''
        self.SeatNum = tk.StringVar()
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Student', font=LARGE_FONT)
        label.grid(row=0, column=1, padx=100, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=0, pady=10)
        SeatNumEntry = tk.ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=1, column=0, sticky='NW', padx=5, pady=125)
        addFileBtn = tk.ttk.Button(self, text='Add File', command=lambda: self.getFile())
        addFileBtn.grid(row=1, column=0, pady=150)
        self.fileStatus = tk.Label(self, text='Add a File')
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
        else:
            self.fileStatus.config(text='File Added'.upper())

    def marks_wrt_subject(self):
        if self.file != '':
            data = pd.read_csv(self.file)
            col = data.columns
            subjects = data[col[0]]
            marks = data[col[1]]
            subjectsOnX = np.arange(len(subjects))
            plt.xticks(subjectsOnX, subjects)
            plt.title("Student's data")
            plt.xlabel(col[0])
            plt.ylabel('Marks')
            plt.bar(subjects, marks)
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def all_sem_performance(self):
        if self.file != '' and self.SeatNum != '':
            data = pd.read_csv(self.file)
            col = data.columns
            sub = col[2:]
            students = np.array(data[col[0]])
            SubMarks = [np.array(data[col[i]]) for i in range(2, 7)]
            MaxOfAll = [np.max(i) for i in SubMarks]
            AllAvg = [np.array(np.average(data[col[i]])) for i in range(2, 7)]
            plt.title('Your Performance vs Class')
            plt.bar(np.arange(5) + 0.00, MaxOfAll, color='#004c6d', width=0.25)
            plt.bar(np.arange(5) + 0.25, AllAvg, color='#286d8a', width=0.25)
            value = self.SeatNum.get()
            if value in students:
                stud = data.loc[data['seat'] == value]
                stud = np.array(stud[col[2:]].values).flatten()
                plt.bar(np.arange(5) + 0.50, stud, color='#008cc9', width=0.25)
            plt.xticks(np.arange(5), sub)
            plt.legend(labels=['Max', 'Average', value])
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def IndStud(self):
        if self.file != '' and self.SeatNum.get() != '':
            student = self.SeatNum.get().upper()
            data = pd.read_csv(self.file)
            col = data.columns
            subjects = [c for c in col][2:]
            print(subjects)
            SubjectMarks = data.loc[data.seat == student]
            SubjectMarks = np.array(SubjectMarks[col[2:]].values).flatten()
            plt.bar(subjects, SubjectMarks)
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')


class TchrOptionFrame(tk.Frame):
    def __init__(self, parent, controller):
        self.file = ''
        self.SeatNum = tk.StringVar()
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Teacher', font=LARGE_FONT)
        label.grid(row=0, column=1, padx=100, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=0, pady=10)
        SeatNumEntry = tk.ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=1, column=0, sticky='NW', padx=5, pady=125)
        addFileBtn = tk.ttk.Button(self, text='Add File', command=lambda: self.getFile())
        addFileBtn.grid(row=1, column=0, pady=150)
        self.fileStatus = tk.Label(self, text='Add a File')
        self.fileStatus.grid(row=1, column=1)
        ClassPer = tk.ttk.Button(self, text='Class Performance',
                                 command=lambda: TryExcept(self.ClassPerformance))
        ClassPer.grid(row=1, column=2)
        ClassGrowth = tk.ttk.Button(self, text='Class Growth', command=lambda: TryExcept(self.ClassGrowth))
        ClassGrowth.grid(row=1, column=2, pady=115, sticky='N')
        Best3 = tk.ttk.Button(self, text='Best 3', command=lambda: StudOptionFrame.marks_wrt_subject(self))
        Best3.grid(row=1, column=2, pady=80, sticky='N')

    def getFile(self):
        self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                               filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
        if self.file == '':
            self.fileStatus.config(text='No File Added'.upper())
        else:
            self.fileStatus.config(text='File Added'.upper())

    def ClassPerformance(self):
        if self.file != '':
            data = pd.read_csv(self.file)
            print(data)
            F = data.loc[data.Grade == 'F'].count()[0]
            D = data.loc[data.Grade == 'D'].count()[0]
            C = data.loc[data.Grade == 'C'].count()[0]
            B = data.loc[data.Grade == 'B'].count()[0]
            A = data.loc[data.Grade == 'A'].count()[0]
            O = data.loc[data.Grade == 'O'].count()[0]
            grade = [O, A, B, C, D, F]
            labels = ['O', 'A', 'B', 'C', 'D', 'F']
            plt.title("Student's data")
            plt.pie(grade, labels=labels, autopct='%.2f %%', explode=np.array([0.03] * 6))
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')

    def ClassGrowth(self):
        if self.file != '':
            data = pd.read_csv(self.file)
            semData = [np.mean(data.iloc[:, i]) for i in range(1, len(data.columns) - 1)]
            print(semData)
            plt.plot(semData)
            plt.ylim(5, 10)
            plt.legend(labels=['Growth in avg. CGPA '])
            plt.xticks(np.arange(6), ['I', 'II', 'III', 'IV', 'V', 'VI'])
            plt.show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')


app = SPE_src()
app.resizable(width=0, height=0)
app.title('Students Performance Evaluation')
# app.geometry('1280x720')
app.mainloop()
