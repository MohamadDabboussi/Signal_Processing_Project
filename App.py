import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from Filter_Class import My_Filter
from Signal_Class import My_Signal
from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, fftshift
import math
import numpy as np

LARGE_FONT = ("Verdana", 20)
MEDIUM_FONT = ("Verdana", 12)


class Projet(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Projet Traitement Numerique")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.geometry("1300x760")

        self.signal1 = My_Signal()
        self.filter1 = My_Filter()

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(
            self, text="Projet Traitement Numerique", font=LARGE_FONT)
        label.place(relx=.3, rely=.1)

        button = ttk.Button(self, text="RII Filter",
                            command=lambda: controller.show_frame(PageOne))
        button.place(relx=.4, rely=.5, width=150, height=50)

        # button2 = ttk.Button(self, text="RIF Filter",
        #                      command=lambda: controller.show_frame(PageTwo))
        # button2.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(
            self, text="Quel signal vous voulez traiter?", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        label.grid(row=0, column=1, padx=10, pady=50)
        label.place(relx=.3, rely=.1)

        button1 = ttk.Button(self, text="Signal somme de sinus",
                             command=lambda: controller.show_frame(PageTwo))

        button1.grid(row=1, column=0, padx=10, pady=20, ipady=30, ipadx=30)
        button1.place(relx=.33, rely=.5, width=150, height=50)

        button2 = ttk.Button(self, text="Signal Audio",
                             command=lambda: controller.show_frame(PageTwo))
        button2.grid(row=1, column=2, padx=10, pady=20, ipady=30, ipadx=30)
        button2.place(relx=.66, rely=.5, width=150, height=50)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        def plot(t, s1):
            # the figure that will contain the plot
            fig = Figure(figsize=(4, 3),
                         dpi=100)
            # adding the subplot
            plot1 = fig.add_subplot(111)
            # plotting the graph
            plot1.plot(t[:200], s1.sum[:200])
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig,
                                       master=self)
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().grid(row=1, column=3, columnspan=2, padx=10, pady=10)
            canvas.get_tk_widget().place(relx=.66, rely=.15)

            # fig2
            f_sample = t.size
            xf = fftfreq(f_sample, 1/f_sample)
            fft_output2 = (fft(s1.sum))
            fft_output2 = fft_output2/np.max(fft_output2)
            fig2 = Figure(figsize=(4, 3),
                          dpi=100)
            plot2 = fig2.add_subplot(111)
            plot2.plot(xf[0:20000], np.abs(fft_output2)[0:20000])
            canvas = FigureCanvasTkAgg(fig2,
                                       master=self)
            canvas.draw()
            canvas.get_tk_widget().place(relx=.66, rely=.55)

        def add_signal():
            f_sample = 44000
            t = np.linspace(0, 1, f_sample)
            s1 = controller.signal1
            s1.add_signal(t, int(entry_amplitude.get()),
                          int(entry_frequency.get()))
            plot(t, s1)

        def add_noise():
            f_sample = 44000
            t = np.linspace(0, 1, f_sample)
            s1 = controller.signal1
            s1.add_white_noise(2)
            plot(t, s1)

        def reset():
            f_sample = 44000
            t = np.linspace(0, 1, f_sample)
            s1 = controller.signal1
            s1.reset_signal()
            plot(t, s1)

        label = ttk.Label(
            self, text="Creé le signal à traiter", font=LARGE_FONT)
        label.grid(row=0, column=1, padx=10, pady=10)
        label.place(relx=.4, rely=.1)

        button_add_signal = ttk.Button(self, text="add frequency to the signal",
                                       command=add_signal)
        button_add_signal.grid(row=1, column=0, padx=10, pady=10)
        button_add_signal.place(relx=.1, rely=.3)

        entry_amplitude = tk.Entry(self, width=50, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter amplitude: ", font=MEDIUM_FONT)
        labelText.place(relx=.1, rely=.4)
        entry_amplitude.place(relx=.28, rely=.4)
        entry_frequency = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter frequency: ", font=MEDIUM_FONT)
        labelText2.place(relx=.1, rely=.5)
        entry_frequency.place(relx=.28, rely=.5)

        button_add_noise = ttk.Button(self, text="add white noise",
                                      command=add_noise)
        button_add_noise.grid(row=1, column=1, padx=10, pady=10)
        button_add_noise.place(relx=.3, rely=.3)

        button1 = ttk.Button(self, text="next",
                             command=lambda: controller.show_frame(PageThree))
        button1.grid(row=2, column=2, padx=10, pady=10)
        button1.place(relx=.5, rely=.8)

        button3 = ttk.Button(self, text="reset signal",
                             command=reset)
        button3.grid(row=2, column=1, padx=10, pady=10)
        button3.place(relx=.3, rely=.8)

        button2 = ttk.Button(self, text="back",
                             command=lambda: controller.show_frame(PageOne))
        button2.grid(row=2, column=0, padx=10, pady=10)
        button2.place(relx=.1, rely=.8)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(
            self, text="Do you know the order of the filter and the cutoff frequency ?", font=LARGE_FONT)
        label.place(relx=.2, rely=.1)

        button1 = ttk.Button(self, text="Yes",
                             command=lambda: controller.show_frame(PageFour))
        button1.place(relx=.3, rely=.5, width=100, height=50)

        button2 = ttk.Button(self, text="No",
                             command=lambda: controller.show_frame(PageFive))
        button2.place(relx=.6, rely=.5, width=100, height=50)


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Create Filter", font=LARGE_FONT)
        label.place(relx=.4, rely=.1)

        def plot(f_sample, w2, h2, Wn):
            # the figure that will contain the plot
            fig = Figure(figsize=(4, 3),
                         dpi=100)
            # adding the subplot
            plot1 = fig.add_subplot(111)
            # plotting the graph
            plot1.semilogx(w2*f_sample/(2*math.pi), 20*np.log10(abs(h2)))
            plot1.set_xscale('log')
            plot1.title.set_text('Butterworth filter frequency response')
            plot1.set_xlabel('Frequency [Hz]')
            plot1.set_ylabel('Amplitude [dB]')
            plot1.margins(0, 0.1)
            plot1.grid(which='both', axis='both')
            if(Wn.size > 1):
                plot1.axvline(Wn[0]*f_sample/2, color='green')
                plot1.axvline(Wn[1]*f_sample/2, color='green')
            else:
                plot1.axvline(Wn*f_sample/2, color='green')
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig,
                                       master=self)
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(relx=.66, rely=.3)

        def create_filter():
            filter1 = controller.filter1
            filter1.set_name(comboBox_filter_name_0.get())
            filter1.set_type(comboBox_filter_type_0.get())
            f_sample = 44000
            order = int(entry_order.get())
            if(filter1.filter_type == "bandpass" or filter1.filter_type == "bandstop"):
                Wn = [int(entry_cutoff_frequency.get()), int(
                    entry_cutoff_frequency2.get())]
            else:
                Wn = [int(entry_cutoff_frequency.get())]
            filter1.filter_design(order, Wn, f_sample)
            b2, a2 = filter1.filter_create(rs=40)
            w2, h2 = filter1.filter_plot_prep(b2, a2)
            Wn = filter1.Wn
            plot(f_sample, w2, h2, Wn)

        def comboBox_filter_name_click(event):
            # rp
            if(comboBox_filter_name_0.get() == "cheby1" or comboBox_filter_name_0.get() == "ellip"):
                labelText4.place(relx=.35, rely=.6)
                entry_rp.place(relx=.43, rely=.6, width=100)
            else:
                labelText4.place_forget()
                entry_rp.place_forget()

            # rs
            if(comboBox_filter_name_0.get() == "cheby2" or comboBox_filter_name_0.get() == "ellip"):
                labelText5.place(relx=.35, rely=.7)
                entry_rs.place(relx=.43, rely=.7, width=100)
            else:
                labelText5.place_forget()
                entry_rs.place_forget()
            return

        def comboBox_filter_type_click(event):
            if(comboBox_filter_type_0.get() == "bandpass" or comboBox_filter_type_0.get() == "bandstop"):
                labelText3.place(relx=.05, rely=.7)
                entry_cutoff_frequency2.place(relx=.23, rely=.7, width=100)
            else:
                labelText3.place_forget()
                entry_cutoff_frequency2.place_forget()

        filter_names = ["butter", "cheby1", "cheby2", "ellip"]
        filter_types = ["low", "high", "bandpass", "bandstop"]

        # self.option_add("*TCombobox*Listbox*Background", 'green')
        # self.option_add("*TCombobox*Listbox*selectedbackground", 'green')
        # self.option_add("*TCombobox*Listbox*foreground", 'black')

        # c = ttk.Combobox(
        #     self, value=filter_names, state='readonly')
        # c.current(0)
        # c.bind("<<ComboboxSelected>>", comboBox_filter_name_click)
        # c.place(relx=.15, rely=.2, width=100, height=30)

        # c2 = ttk.Combobox(
        #     self, value=filter_types, state='readonly')
        # c2.current(0)
        # c2.bind("<<ComboboxSelected>>", comboBox_filter_type_click)
        # c2.place(relx=.3, rely=.2, width=100, height=30)

        comboBox_filter_name_0 = tk.StringVar()
        comboBox_filter_name_0.set(filter_names[0])
        comboBox_filter_name = tk.OptionMenu(
            self, comboBox_filter_name_0, *filter_names, command=comboBox_filter_name_click)
        comboBox_filter_name.place(relx=.15, rely=.3, width=100, height=30)
        comboBox_filter_name["borderwidth"] = 0

        comboBox_filter_type_0 = tk.StringVar()
        comboBox_filter_type_0.set(filter_types[0])
        comboBox_filter_type = tk.OptionMenu(
            self, comboBox_filter_type_0, *filter_types, command=comboBox_filter_type_click)
        comboBox_filter_type.place(relx=.3, rely=.3, width=100, height=30)
        comboBox_filter_type["borderwidth"] = 0

        entry_order = tk.Entry(self, width=50, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter filter order: ", font=MEDIUM_FONT)
        labelText.place(relx=.05, rely=.5)
        entry_order.place(relx=.2, rely=.5)

        entry_cutoff_frequency = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter cutoff frequency: ", font=MEDIUM_FONT)
        labelText2.place(relx=.05, rely=.6)
        entry_cutoff_frequency.place(relx=.23, rely=.6, width=100)

        entry_cutoff_frequency2 = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText3 = ttk.Label(
            self, text="Enter 2nd cutoff frequency: ", font=MEDIUM_FONT)
        labelText3.place_forget()
        entry_cutoff_frequency2.place_forget()

        entry_rp = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText4 = ttk.Label(
            self, text="Enter rp: ", font=MEDIUM_FONT)
        labelText4.place_forget()
        entry_rp.place_forget()

        entry_rs = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText5 = ttk.Label(
            self, text="Enter rs: ", font=MEDIUM_FONT)
        labelText5.place_forget()
        entry_rs.place_forget()

        button_create_filter = ttk.Button(self, text="Create Filter",
                                          command=create_filter)
        button_create_filter.place(relx=.3, rely=.8)

        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(PageThree))
        button1.place(relx=.1, rely=.8)
        button2 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(PageSix))
        button2.place(relx=.5, rely=.8)


class PageFive(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Design Filter", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        filter_names = ["butter", "cheby1", "cheby2", "ellip"]
        filter_types = ["low", "high", "bandpass", "bandstop"]

        labelText = ttk.Label(
            self, text="Enter filter name: ", font=MEDIUM_FONT)
        labelText.place(relx=.15, rely=.25)
        comboBox_filter_name_0 = tk.StringVar()
        comboBox_filter_name_0.set(filter_names[0])
        comboBox_filter_name = tk.OptionMenu(
            self, comboBox_filter_name_0, *filter_names)
        comboBox_filter_name.place(relx=.15, rely=.3, width=100, height=30)
        comboBox_filter_name["borderwidth"] = 0

        labelText = ttk.Label(
            self, text="Enter filter type: ", font=MEDIUM_FONT)
        labelText.place(relx=.3, rely=.25)
        comboBox_filter_type_0 = tk.StringVar()
        comboBox_filter_type_0.set(filter_types[0])
        comboBox_filter_type = tk.OptionMenu(
            self, comboBox_filter_type_0, *filter_types)
        comboBox_filter_type.place(relx=.3, rely=.3, width=100, height=30)
        comboBox_filter_type["borderwidth"] = 0

        entry_fpass = tk.Entry(self, width=25, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter pass frequency: ", font=MEDIUM_FONT)
        labelText.place(relx=.05, rely=.5)
        entry_fpass.place(relx=.2, rely=.5)
        entry_fstop = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter stop frequency: ", font=MEDIUM_FONT)
        labelText2.place(relx=.05, rely=.55)
        entry_fstop.place(relx=.2, rely=.55)

        entry_fpass2 = tk.Entry(self, width=25, bg='white', fg='black')
        labelText3 = ttk.Label(
            self, text="Enter pass frequency: ", font=MEDIUM_FONT)
        labelText3.place(relx=.35, rely=.5)
        entry_fpass2.place(relx=.5, rely=.5)
        entry_fstop2 = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText4 = ttk.Label(
            self, text="Enter stop frequency: ", font=MEDIUM_FONT)
        labelText4.place(relx=.35, rely=.55)
        entry_fstop2.place(relx=.5, rely=.55)

        entry_gpass = tk.Entry(self, width=50, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter pass attenuation: ", font=MEDIUM_FONT)
        labelText.place(relx=.05, rely=.6)
        entry_gpass.place(relx=.2, rely=.6)
        entry_gstop = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter stop attenuation: ", font=MEDIUM_FONT)
        labelText2.place(relx=.05, rely=.65)
        entry_gstop.place(relx=.2, rely=.65)

        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(PageThree))
        button1.place(relx=.1, rely=.8)
        button2 = ttk.Button(self, text="Next",
                             command=lambda: controller.show_frame(PageSix))
        button2.place(relx=.5, rely=.8)


class PageSix(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Result", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()


app = Projet()
app.resizable(False, False)
app.tk_setPalette('black')
app.mainloop()
