import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import pandas as pd
import numpy as np

style.use('ggplot')

matplotlib.use('TkAgg')

path = 'graph.png'
LARGE_FONT = ('RobotoMono-Medium', 13)


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

        menuBar.add_cascade(label='File', menu=fileMenu)
        tk.Tk.config(self, menu=menuBar)
        self.frames = {}
        for F in (StartPage, StudOptionFrame, StudentORTeacher):
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
        agreement = 'By Clicking on next you hereby ' + '\n' \
                                                        'Agree to use our policy' + '\n' \
                                                                                    'We assure you that we won\'t sell out''\n' \
                                                                                    'your data. It will only be used to improve this''\n' \
                                                                                    'software. ''\n\n' \
                                                                                    'Enjoy using this Software!'
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
        Teacher = tk.ttk.Button(self, text='Teacher', command=lambda: controller.show_frame(StudOptionFrame))
        Teacher.grid(row=2, column=2, padx=25, pady=25, )


class StudOptionFrame(tk.Frame):
    def __init__(self, parent, controller):
        self.file = ''
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='Student', font=LARGE_FONT)
        label.grid(row=0, column=1, padx=100, pady=10)
        back = tk.ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=10, pady=10)
        addFileBtn = tk.ttk.Button(self, text='Add File', command=lambda: self.getFile(self))
        addFileBtn.grid(row=1, column=0, pady=150)
        self.fileStatus = tk.Label(self, text='Add a File')
        self.fileStatus.grid(row=1, column=1)
        SubVSMks = tk.ttk.Button(self, text='Subject VS Marks', command=lambda: self.marks_wrt_subject(self))
        SubVSMks.grid(row=1, column=2)
        SubVSMks = tk.ttk.Button(self, text='Subject VS Marks', command=lambda: self.marks_wrt_subject(self))
        SubVSMks.grid(row=1, column=2, pady=115, sticky='N')
        self.file = ''

    @staticmethod
    def getFile(self):
        self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                               filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
        if self.file == '':
            self.fileStatus.config(text='No File Added'.upper())
        else:
            self.fileStatus.config(text='File Added'.upper())

    @staticmethod
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


app = SPE_src()
app.resizable(width=0, height=0)
# app.geometry('1280x720')
app.mainloop()
