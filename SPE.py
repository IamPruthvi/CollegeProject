import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
import matplotlib
import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import pandas as pd
import numpy as np

matplotlib.use('TkAgg')

path = 'D:/graph.png'
LARGE_FONT = ('RobotoMono-Medium', 13)


class SPE_src(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
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
        label = tk.Label(self, text='Students Performance Evaluation', font=LARGE_FONT)
        label.grid(columnspan=2, pady=10)
        self.img = ImageTk.PhotoImage(Image.open(path))
        panel = tk.Label(self, image=self.img)
        panel.grid(rowspan=2, padx=50, pady=10)
        button1 = tk.Button(self, text='Page 1', command=lambda: controller.show_frame(PageOne))
        button1.grid(row=1, column=1, padx=20)
        button2 = tk.Button(self, text='Page 2', command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=2, column=1)


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Students Performance Evaluation', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StartPage))
        button1.pack()


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text='Graph')
        label.pack(padx=10, pady=10)
        button = ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StartPage))
        button.pack()
        # AddFile = ttk.Button(self, text='Add File', command=lambda:
        # filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
        #                            filetypes=(('CSV Files', '*.csv'), ("All Files", "*."))))
        # AddFile.pack()
        # f = Figure(figsize=(5, 5), dpi=100)
        # a = f.add_subplot(111)
        # a.plot([1, 2, 3, 4, 5, 6, 7, 8], [6, 2, 6, 3, 5, 1, 2, 4])
        # canvas = FigureCanvasTkAgg(f, self)
        # canvas.draw()
        # toolbar = NavigationToolbar2Tk(canvas, self)
        # toolbar.update()
        # canvas.tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        # canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        AddFile = ttk.Button(self, text='Add File', command=self.marks_wrt_subject)
        AddFile.pack()

    @staticmethod
    def marks_wrt_subject():
        file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                          filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
        if file != '':
            data = pd.read_csv(file)
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
            print('hello world')

app = SPE_src()
app.mainloop()
