from tkinter import ttk, Tk, Frame, Menu, RIDGE, StringVar, Toplevel, Label, Button, filedialog, messagebox, IntVar, \
    Checkbutton
from typing import Any, Union
from PIL import ImageTk, Image
from matplotlib.pyplot import clf, xticks, legend, title, ylim, show, plot, figure, subplot, xlabel, ylabel
from matplotlib import style, use
from numpy import array, transpose, max, average, mean, arange, unique, min
from pandas import DataFrame, Series, read_csv, Index
from pandas.io.parsers import TextFileReader
from webbrowser import open as op
from PyPDF2 import PdfFileMerger
from functools import partial

style.use('ggplot')
use('TkAgg')

# TODO Add Congratulations to topper.

SUPER_LARGE_FONT = ('RobotoMono-Medium', 30)
LARGE_FONT = ('RobotoMono-Medium', 15)
bg = '#282c34'


def TryExcept(tryFunc):
    try:
        tryFunc()

    except (AttributeError, KeyError, ValueError, TypeError):
        print('Error Found')


class SPE_src(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.config(self, bg=bg)
        self.SeatNum = StringVar()
        container = Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        menuBar = Menu(container)
        fileMenu = Menu(menuBar, tearoff=False)
        fileMenu.add_command(label='Save Settings', command=lambda: self.popupmsg('Not Supported Yet.'))
        fileMenu.add_separator()
        fileMenu.add_command(label='Close', command=quit)
        graphMenu = Menu(menuBar, tearoff=False)
        graphMenu.add_command(label='Bar', )
        graphMenu.add_command(label='Pie', )
        graphMenu.add_command(label='line', )
        graphMenu.add_command(label='Export as PDF', command=self.PDF_Creator)
        CollegeMenu = Menu(menuBar, tearoff=False)
        CollegeMenu.add_command(label='Info', command=lambda: op('http://nmfdegree.edu.in/#'))
        HelpBar = Menu(menuBar, tearoff=False)
        HelpBar.add_command(label='Tutorial', command=lambda: op('Tutorial Page V2.html'))
        menuBar.add_cascade(label='File', menu=fileMenu)
        menuBar.add_cascade(label='Graph', menu=graphMenu)
        menuBar.add_cascade(label='Info', menu=CollegeMenu)
        menuBar.add_cascade(label='Help', menu=HelpBar)
        Tk.config(self, menu=menuBar)

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

    @staticmethod
    def PDF_Creator():
        pdfs = ['Class Performance.pdf', 'Individual Student.pdf', 'Passed vs Failed.pdf',
                'TOP 5.pdf', 'Your Performance VS Class.pdf']
        merger = PdfFileMerger()
        for pdf in pdfs:
            merger.append('Saved Images/' + pdf)
        merger.write('Result.pdf')
        merger.close()
        messagebox.showinfo(title='PDF exported,', message='PDF is Saved')

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.config(self, bg=bg)
        label = Label(self, text='Students Performance Evaluation', font=SUPER_LARGE_FONT, bg=bg, fg='white')
        label.grid(columnspan=2, pady=10)
        self.img = ImageTk.PhotoImage(Image.open('graph.png'))
        panel = Label(self, image=self.img, bg=bg, relief=RIDGE)
        panel.grid(rowspan=2, padx=25, pady=25)
        agreement = 'By Clicking on next you hereby \n' \
                    'Agree to use our policy\nWe assure you that we won\'t sell out\nyour data. ' \
                    'It will only be used to improve this\nsoftware. \n\nEnjoy using this Software!'
        agmtText = Label(self, text=agreement, bg=bg, font=LARGE_FONT, fg='white', relief=RIDGE)
        agmtText.grid(row=1, column=1, padx=25, ipadx=20, ipady=50)
        CloseBtn = ttk.Button(self, text='Exit', command=lambda: exit())
        CloseBtn.grid(row=2, column=1, sticky='SE', padx=125, pady=25)
        NextBtn = ttk.Button(self, text='Next', command=lambda: controller.show_frame(StudentORTeacher))
        NextBtn.grid(row=2, column=1, sticky='SE', padx=25, pady=25, )


class StudentORTeacher(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        Frame.config(self, bg='#282c34')
        label = Label(self, text='Who are you?', font=SUPER_LARGE_FONT, bg=bg, fg='white')
        label.grid(columnspan=3, pady=10)
        back = ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StartPage))
        back.grid(row=0, columnspan=3, sticky='NW', padx=20, pady=20)
        self.studImg = ImageTk.PhotoImage(Image.open('student.png'))
        self.teachImg = ImageTk.PhotoImage(Image.open('teacher.png'))
        Student = Button(self, text='Student', bg=bg, relief=RIDGE, image=self.studImg,
                         command=lambda: controller.show_frame(StudOptionFrame))
        Student.grid(row=2, column=1, padx=50, pady=25, )
        Teacher = Button(self, text='Teacher', bg=bg, relief=RIDGE, image=self.teachImg,
                         command=lambda: controller.show_frame(TchrOptionFrame))
        Teacher.grid(row=2, column=2, padx=25, pady=25)


class StudOptionFrame(Frame):
    data: Union[Union[TextFileReader, Series, DataFrame, None], Any]

    def __init__(self, parent, controller):
        self.file = ''
        self.SeatNum = StringVar()
        Frame.__init__(self, parent)
        Frame.config(self, bg=bg)
        label = Label(self, text='Student', font=SUPER_LARGE_FONT, bg=bg, fg='white')
        label.grid(row=0, column=3, pady=10, padx=120)
        label2 = Label(self, text='', bg=bg)
        label2.grid(row=1, column=1, pady=25)
        back = ttk.Button(self, text='<Back', command=lambda: controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, padx=0, pady=10)
        SeatNumEntry = ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=5, column=0, padx=10, pady=10)
        addFileBtn = ttk.Button(self, text='Add File', command=lambda: TryExcept(partial(self.getFile)))
        addFileBtn.grid(row=6, column=0)
        self.fileStatus = Label(self, text='Add a File', bg=bg, fg='white')
        self.fileStatus.grid(row=5, column=3, padx=100)
        ExportPDF = ttk.Button(self, text='Export Selected', command=self.Export, width=25)
        ExportPDF.grid(row=8, column=5, pady=5)
        SubVSMks = ttk.Button(self, text='Subject VS Marks', width=25)
        SubVSMks.grid(row=3, column=5, pady=10)
        AllSem = ttk.Button(self, text='Your Performance VS Class', command=lambda: TryExcept(partial(self.all_sem_performance)),
                            width=25)
        AllSem.grid(row=4, column=5, pady=10)
        IndStud = ttk.Button(self, text='Individual Student', command=lambda: TryExcept(partial(self.IndStud)), width=25)
        IndStud.grid(row=5, column=5)
        StudentDetail = ttk.Button(self, text='Student Detail', command=lambda: TryExcept(partial(self.StudentDetail)), width=25)
        StudentDetail.grid(row=6, column=5, pady=10)
        self.cb = [IntVar(), IntVar()]
        AllSemRB = Checkbutton(self, text='', variable=self.cb[0], bg=bg)
        AllSemRB.grid(row=4, column=6, padx=5)
        IndStudRB = Checkbutton(self, text='', variable=self.cb[1], bg=bg)
        IndStudRB.grid(row=5, column=6, pady=5, padx=5)
        self.SeatData = array([])

    def Export(self):
        if self.cb[0].get():
            TryExcept(partial(self.all_sem_performance))
        if self.cb[1].get():
            TryExcept(partial(self.IndStud))

    def getFile(self):
        try:
            self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                                   filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
            if self.file == '':
                self.fileStatus.config(text='No File Added'.upper())
                self.fileStatus.config(fg='#FF0000')
            else:
                self.fileStatus.config(text='File Added'.upper())
                self.fileStatus.config(fg='#00FF00')
                self.data = read_csv(self.file)
                self.SeatData = array(self.data['Seat No'])
        except KeyError:
            print('Key Error')
            messagebox.showwarning(title='Incorrect Data', message='Enter CSV file provided by college')

    def all_sem_performance(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            col = data.columns
            Subjects = [''.join(list(c)[:-6]) for c in col][3:10]
            SubjectData = []
            Student = []
            for i in range(0, len(self.SeatData), 6):
                idx = Index(self.SeatData)
                locData = idx.get_loc(self.SeatData[i])
                StudentData = data.loc[locData + 2, :]
                OneData = array(StudentData[3:10]).astype(int)
                if self.SeatData[i] == self.SeatNum.get().upper():
                    Student = array(StudentData[3:10]).astype(int)
                SubjectData.append(OneData)
            SubjectData = transpose(SubjectData)
            MaxOfAll = [max(i) for i in SubjectData]
            AvgOfAll = [average(i) for i in SubjectData]
            fig = figure()
            ax = subplot(111)
            title('Your Performance vs Class')
            xlabel('Subjects')
            ylabel('Marks Range')
            ax.bar(arange(7) + 0.00, MaxOfAll, color='#004c6d', width=0.25)
            ax.bar(arange(7) + 0.25, AvgOfAll, color='#286d8a', width=0.25)
            ax.bar(arange(7) + 0.50, Student, color='#008cc9', width=0.25)
            xticks(arange(7), Subjects)
            ax.legend(labels=['Max', 'Average', self.SeatNum.get().upper()])
            if self.cb[1].get():
                fig.savefig('Saved Images\Your Performance VS Class.pdf')
            fig.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def IndStud(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            col = data.columns
            idx = Index(self.SeatData)
            locData = idx.get_loc(self.SeatNum.get().upper())
            StudentData = data.loc[locData + 2, :]
            SubjectData = array(StudentData[3:10]).astype(int)
            Subjects = [''.join(list(c)[:-6]) for c in col][3:10]
            fig = figure()
            ax = subplot(111)
            title('Marks of ' + self.SeatNum.get().upper())
            xlabel('Subjects')
            ylabel('Marks Range')
            ylim(0, 75)
            ax.bar(Subjects, SubjectData)
            fig.show()
        else:
            messagebox.showwarning('Error 404', 'File not found')

    def StudentDetail(self):
        clf()
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            idx = Index(self.SeatData)
            locData = idx.get_loc(self.SeatNum.get().upper())
            Marks = array(data['Total [ 20 ]'])[locData + 2]
            NameValue = array(data['Name'])[locData]
            Grade = array(data['Grade'])[locData + 2]
            Remark = array(data['Grade'])[locData + 1].replace('..', 'l')
            RemarkColor = ['green' if Remark == 'Successful' else 'red']
            CGPA = array(data['Grade'])[locData]
            StudentFrame = Toplevel()
            StudentFrame.geometry('700x350')
            SeatLabel = ttk.Label(master=StudentFrame, text='Seat  No. : {}'.format(self.SeatNum.get().upper()))
            SeatLabel.grid(padx=20, pady=20, sticky='W')
            Name = ttk.Label(master=StudentFrame, text='Name : {}'.format(NameValue))
            Name.grid(row=1, column=0, padx=20, sticky='W')
            MarksLabel = ttk.Label(master=StudentFrame, text='Marks : {}'.format(Marks))
            MarksLabel.grid(row=2, column=0, padx=20, pady=20, sticky='W')
            GradeLabel = ttk.Label(master=StudentFrame, text='Grade : {}'.format(Grade))
            GradeLabel.grid(row=3, column=0, padx=20, sticky='W')
            CGPALabel = ttk.Label(master=StudentFrame, text='CGPA : {}'.format(CGPA))
            CGPALabel.grid(row=4, column=0, padx=20, pady=20, sticky='W')
            RemarkLabel = Label(master=StudentFrame, text='Remark : {}'.format(Remark), fg=RemarkColor)
            RemarkLabel.grid(row=5, column=0, padx=20, sticky='W')
        else:
            messagebox.showwarning('Error 404', 'File not found')


class TchrOptionFrame(Frame):
    data: Union[Union[TextFileReader, Series, DataFrame, None], Any]

    def __init__(self, parent, controller):
        self.file = ''
        self.SeatData = array([])
        self.SeatNum = StringVar()
        Frame.__init__(self, parent)
        Frame.config(self, bg=bg)
        label = Label(self, text='Teacher', font=SUPER_LARGE_FONT, bg=bg, fg='white')
        label.grid(row=0, column=3, pady=10, padx=120)
        label2 = Label(self, text='', bg=bg)
        label2.grid(row=1, column=1, pady=25)
        back = ttk.Button(self, text='<Back', command=controller.show_frame(StudentORTeacher))
        back.grid(row=0, column=0, pady=10)
        SeatNumEntry = ttk.Entry(self, textvariable=self.SeatNum)
        SeatNumEntry.grid(row=4 + 1, column=0, padx=10, pady=10)
        addFileBtn = ttk.Button(self, text='Add File', command=lambda: TryExcept(partial(self.getFile)))
        addFileBtn.grid(row=5 + 1, column=0)
        self.fileStatus = Label(self, text='Add a File', bg=bg, fg='white')
        self.fileStatus.grid(row=5, column=3, padx=100)
        ClassPer = ttk.Button(self, text='Class Performance', command=lambda: TryExcept(partial(self.ClassPerformance)),
                              width=25)
        ClassPer.grid(row=6, column=5, pady=5)
        ClassGrowth = ttk.Button(self, text='Class Growth', command=lambda: TryExcept(partial(self.ClassGrowthInfo)), width=25)
        ClassGrowth.grid(row=4, column=5, pady=10)
        Top5 = ttk.Button(self, text='Top 5', command=lambda: TryExcept(partial(self.Top5)), width=25)
        Top5.grid(row=5, column=5)
        StudentDetail = ttk.Button(self, text='Student Detail', command=lambda: TryExcept(partial(self.StudentDetailInfo)),
                                   width=25)
        StudentDetail.grid(row=3, column=5, pady=10)
        PFButton = ttk.Button(self, text='Passed vs Failed', command=lambda: TryExcept(partial(self.PassedVSFailed)), width=25)
        PFButton.grid(row=7, column=5, pady=10)
        ExportAll = ttk.Button(self, text='Export Selected', width=25, command=self.Export)
        ExportAll.grid(row=8, column=5, pady=5)
        self.cb = [IntVar(), IntVar(), IntVar()]
        ClassPerCB = Checkbutton(self, text='', bg=bg, variable=self.cb[0])
        ClassPerCB.grid(row=6, column=6, padx=5)
        Top5CB = Checkbutton(self, text='', bg=bg, variable=self.cb[1])
        Top5CB.grid(row=5, column=6, padx=5)
        PFCB = Checkbutton(self, text='', bg=bg, variable=self.cb[2])
        PFCB.grid(row=7, column=6, pady=5, padx=5)

    def getFile(self):
        try:
            self.file = filedialog.askopenfilename(initialdir="D:/Actual Study Material/My projects/Python",
                                                   filetypes=(('CSV Files', '*.csv'), ("All Files", "*.")))
            if self.file == '':
                self.fileStatus.config(text='NO FILE ADDED', fg='red')
            else:
                self.fileStatus.config(text='FILE ADDED', fg='green')
                self.data = read_csv(self.file)
                self.SeatData = array(self.data['Seat No'])
        except KeyError:
            print('Key Error')
            messagebox.showwarning(title='Incorrect Data', message='Enter CSV file provided by college')

    def Export(self):
        if self.cb[0].get():
            TryExcept(self.ClassPerformance)
        if self.cb[1].get():
            TryExcept(self.Top5)
        if self.cb[2].get():
            TryExcept(self.PassedVSFailed)

    def ClassPerformance(self):
        if self.file != '':
            grade = array(self.data.Grade)[2::6]
            u, c = unique(grade, return_counts=True)
            GradeCount = dict(zip(u, c))
            fig = figure()
            ax = subplot(111)
            title("Student's data")
            ax.pie(GradeCount.values(), labels=GradeCount.keys(), autopct='%.2f %%',
                   explode=array([0.03] * len(GradeCount)))
            legend()
            if self.cb[0].get():
                fig.savefig('Saved Images\Class Performance.pdf')
            fig.show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')

    def PassedVSFailed(self):
        if self.file != '':
            PF = array(self.data.Grade)[1::6]
            u, c = unique(PF, return_counts=True)
            PFCount = dict(zip(u, c))
            fig = figure()
            ax = subplot(111)
            title("Student's data")
            ax.pie(PFCount.values(), labels=PFCount.keys(), autopct='%.2f %%',
                   explode=array([0.03] * len(PFCount)))
            legend()
            if self.cb[2].get():
                fig.savefig('Saved Images\Passed vs Failed.pdf')
            fig.show()

    def ClassGrowthInfo(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            semData = [mean(self.data.iloc[:, i]) for i in range(1, len(self.data.columns) - 2)]
            idx = Index(self.SeatData)
            locData = idx.get_loc(self.SeatNum.get().upper())
            StudentData = array(self.data.loc[locData, :])[1:-2]
            plot(semData)
            plot(StudentData)
            ylim(5, 10)
            legend(labels=['Average', self.SeatNum.get().upper()])
            xticks(arange(6), ['I', 'II', 'III', 'IV', 'V', 'VI'])
            show()
        else:
            messagebox.showwarning('Error 404', 'File not found.')

    def Top5(self):
        if self.file != '':
            Total = self.data['Total [ 20 ]'][2::6]
            SeatNo = self.data['Seat No'][::6]
            StudentData = sorted(list(zip(Total, SeatNo)))
            SeatValue = array([StudentData[-5:][i][1] for i in range(5)])
            Marks = array([StudentData[-5:][i][0] for i in range(5)])
            fig = figure()
            ax = subplot(111)
            ax.bar(SeatValue, Marks)
            ylim(min(Marks) - 50, max(Marks) + 50)
            if self.cb[1].get():
                fig.savefig('Saved Images\TOP 5.pdf')
            fig.show()

    def StudentDetailInfo(self):
        if self.file != '' and self.SeatNum.get().upper() in self.SeatData:
            data = self.data
            idx = Index(self.SeatData)
            locData = idx.get_loc(self.SeatNum.get().upper())
            Marks = array(data['Total [ 20 ]'])[locData + 2]
            NameValue = array(data['Name'])[locData]
            Grade = array(data['Grade'])[locData + 2]
            Remark = array(data['Grade'])[locData + 1].replace('..', 'l')
            RemarkColor = ['green' if Remark == 'Successful' else 'red']
            CGPA = array(data['Grade'])[locData]
            StudentFrame = Toplevel()
            StudentFrame.geometry('700x350')
            SeatLabel = ttk.Label(master=StudentFrame, text='Seat  No. : {}'.format(self.SeatNum.get().upper()))
            SeatLabel.grid(padx=20, pady=20, sticky='W')
            Name = ttk.Label(master=StudentFrame, text='Name : {}'.format(NameValue))
            Name.grid(row=1, column=0, padx=20, sticky='W')
            MarksLabel = ttk.Label(master=StudentFrame, text='Marks : {}'.format(Marks))
            MarksLabel.grid(row=2, column=0, padx=20, pady=20, sticky='W')
            GradeLabel = ttk.Label(master=StudentFrame, text='Grade : {}'.format(Grade))
            GradeLabel.grid(row=3, column=0, padx=20, sticky='W')
            CGPALabel = ttk.Label(master=StudentFrame, text='CGPA : {}'.format(CGPA))
            CGPALabel.grid(row=4, column=0, padx=20, pady=20, sticky='W')
            RemarkLabel = Label(master=StudentFrame, text='Remark : {}'.format(Remark), fg=RemarkColor)
            RemarkLabel.grid(row=5, column=0, padx=20, sticky='W')
        else:
            messagebox.showwarning('Error 404', 'File not found')


app = SPE_src()
app.resizable(width=0, height=0)
app.title('Students Performance Evaluation')
# app.geometry('1280x720')
app.mainloop()
