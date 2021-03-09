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
import sounddevice as sd
from scipy.io import wavfile

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
        self.is_audio = False

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour, PageFive, PageSix, PageTen):

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

        def two():
            controller.is_audio = False
            controller.show_frame(PageTwo)

        def ten():
            controller.is_audio = True
            controller.show_frame(PageTen)

        label = ttk.Label(
            self, text="Quel signal vous voulez traiter?", font=LARGE_FONT)
        # label.pack(pady=10, padx=10)
        label.place(relx=.3, rely=.1)

        button1 = ttk.Button(self, text="Signal somme de sinus",
                             command=two)
        button1.place(relx=.25, rely=.5, width=150, height=50)

        button2 = ttk.Button(self, text="Signal Audio",
                             command=ten)
        button2.place(relx=.6, rely=.5, width=150, height=50)


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
            s1.add_white_noise(int(entry_noise_amplitude.get()))
            plot(t, s1)

        def reset():
            f_sample = 44000
            t = np.linspace(0, 1, f_sample)
            s1 = controller.signal1
            s1.reset_signal()
            plot(t, s1)

        label = ttk.Label(
            self, text="Creé le signal à traiter", font=LARGE_FONT)
        label.place(relx=.4, rely=.1)

        button_add_signal = ttk.Button(self, text="Add frequency to the signal",
                                       command=add_signal)
        button_add_signal.place(relx=.1, rely=.3, width=200, height=30)

        entry_amplitude = tk.Entry(self, width=50, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter signal amplitude: ", font=MEDIUM_FONT)
        labelText.place(relx=.1, rely=.4)
        entry_amplitude.place(relx=.28, rely=.4)
        entry_frequency = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter signal frequency: ", font=MEDIUM_FONT)
        labelText2.place(relx=.1, rely=.5)
        entry_frequency.place(relx=.28, rely=.5)
        entry_noise_amplitude = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText3 = ttk.Label(
            self, text="Enter noise amplitude: ", font=MEDIUM_FONT)
        labelText3.place(relx=.1, rely=.6)
        entry_noise_amplitude.place(relx=.28, rely=.6)

        button_add_noise = ttk.Button(self, text="Add white noise",
                                      command=add_noise)
        button_add_noise.place(relx=.3, rely=.3, width=150, height=30)

        button1 = ttk.Button(self, text="next",
                             command=lambda: controller.show_frame(PageThree))
        button1.place(relx=.5, rely=.8)

        button3 = ttk.Button(self, text="reset signal",
                             command=reset)
        button3.place(relx=.3, rely=.8)

        button2 = ttk.Button(self, text="back",
                             command=lambda: controller.show_frame(PageOne))
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

        button3 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(PageTwo))
        button3.place(relx=.1, rely=.8)


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
            if(comboBox_filter_name_0.get() == "cheby1"):
                rp = float(entry_rp.get())
                b2, a2 = filter1.filter_create(rp=rp)
            elif(comboBox_filter_name_0.get() == "cheby2"):
                rs = float(entry_rs.get())
                b2, a2 = filter1.filter_create(rs=rs)
            elif(comboBox_filter_name_0.get() == "ellip"):
                rp = float(entry_rp.get())
                rs = float(entry_rs.get())
                b2, a2 = filter1.filter_create(rp=rp, rs=rs)
            else:
                b2, a2 = filter1.filter_create()
            w2, h2 = filter1.filter_plot_prep(b2, a2)
            Wn = filter1.Wn
            plot(f_sample, w2, h2, Wn)

        def comboBox_filter_name_click(event):
            # rp
            if(comboBox_filter_name_0.get() == "cheby1" or comboBox_filter_name_0.get() == "ellip"):
                labelText4.place(relx=.35, rely=.6)
                entry_rp.place(relx=.52, rely=.6, width=100)
            else:
                labelText4.place_forget()
                entry_rp.place_forget()

            # rs
            if(comboBox_filter_name_0.get() == "cheby2" or comboBox_filter_name_0.get() == "ellip"):
                labelText5.place(relx=.35, rely=.7)
                entry_rs.place(relx=.52, rely=.7, width=100)
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
            self, text="Enter max attenuation: ", font=MEDIUM_FONT)
        labelText4.place_forget()
        entry_rp.place_forget()

        entry_rs = tk.Entry(
            self, width=50, bg='white', fg='black')
        labelText5 = ttk.Label(
            self, text="Enter min attenuation: ", font=MEDIUM_FONT)
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

        def design_filter():
            filter1 = controller.filter1
            filter1.set_name(comboBox_filter_name_0.get())
            filter1.set_type(comboBox_filter_type_0.get())
            filter1.set_gpass(float(entry_gpass.get()))
            filter1.set_gstop(float(entry_gstop.get()))
            if(filter1.filter_type == "bandpass" or filter1.filter_type == "bandstop"):
                filter1.set_fpass([int(entry_fpass.get()), int(
                    entry_fpass2.get())])
                filter1.set_fstop([int(entry_fstop.get()), int(
                    entry_fstop2.get())])
            else:
                filter1.set_fpass([int(entry_fpass.get())])
                filter1.set_fstop([int(entry_fstop.get())])
            f_sample = 44000
            Td = 1
            filter1.Normalize_Filter(f_sample)
            filter1.PreWarping_Filter(Td)
            filter1.filter_design()
            if(comboBox_filter_name_0.get() == "cheby1"):
                rp = float(entry_rp.get())
                b2, a2 = filter1.filter_create(rp=rp)
            elif(comboBox_filter_name_0.get() == "cheby2"):
                rs = float(entry_rs.get())
                b2, a2 = filter1.filter_create(rs=rs)
            elif(comboBox_filter_name_0.get() == "ellip"):
                rp = float(entry_rp.get())
                rs = float(entry_rs.get())
                b2, a2 = filter1.filter_create(rp=rp, rs=rs)
            else:
                b2, a2 = filter1.filter_create()
            w2, h2 = filter1.filter_plot_prep(b2, a2)
            Wn = filter1.Wn
            plot(f_sample, w2, h2, Wn)

        def comboBox_filter_name_click(event):
            # rp
            if(comboBox_filter_name_0.get() == "cheby1" or comboBox_filter_name_0.get() == "ellip"):
                labelText5.place(relx=.33, rely=.6)
                entry_rp.place(relx=.51, rely=.6)
            else:
                labelText5.place_forget()
                entry_rp.place_forget()
            # rs
            if(comboBox_filter_name_0.get() == "cheby2" or comboBox_filter_name_0.get() == "ellip"):
                labelText6.place(relx=.33, rely=.65)
                entry_rs.place(relx=.51, rely=.65)
            else:
                labelText6.place_forget()
                entry_rs.place_forget()
            return

        def comboBox_filter_type_click(event):
            if(comboBox_filter_type_0.get() == "bandpass" or comboBox_filter_type_0.get() == "bandstop"):
                labelText3.place(relx=.33, rely=.5)
                entry_fpass2.place(relx=.51, rely=.5)
                labelText4.place(relx=.33, rely=.55)
                entry_fstop2.place(relx=.51, rely=.55)
            else:
                labelText3.place_forget()
                entry_fpass2.place_forget()
                labelText4.place_forget()
                entry_fstop2.place_forget()

        filter_names = ["butter", "cheby1", "cheby2", "ellip"]
        filter_types = ["low", "high", "bandpass", "bandstop"]

        labelText = ttk.Label(
            self, text="Enter filter name: ", font=MEDIUM_FONT)
        labelText.place(relx=.15, rely=.25)
        comboBox_filter_name_0 = tk.StringVar()
        comboBox_filter_name_0.set(filter_names[0])
        comboBox_filter_name = tk.OptionMenu(
            self, comboBox_filter_name_0, *filter_names, command=comboBox_filter_name_click)
        comboBox_filter_name.place(relx=.15, rely=.3, width=100, height=30)
        comboBox_filter_name["borderwidth"] = 0

        labelText = ttk.Label(
            self, text="Enter filter type: ", font=MEDIUM_FONT)
        labelText.place(relx=.3, rely=.25)
        comboBox_filter_type_0 = tk.StringVar()
        comboBox_filter_type_0.set(filter_types[0])
        comboBox_filter_type = tk.OptionMenu(
            self, comboBox_filter_type_0, *filter_types, command=comboBox_filter_type_click)
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
            self, text="Enter pass frequency 2: ", font=MEDIUM_FONT)
        labelText3.place_forget()
        entry_fpass2.place_forget()
        entry_fstop2 = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText4 = ttk.Label(
            self, text="Enter stop frequency 2: ", font=MEDIUM_FONT)
        labelText4.place_forget()
        entry_fstop2.place_forget()

        entry_gpass = tk.Entry(self, width=25, bg='white', fg='black')
        labelText = ttk.Label(
            self, text="Enter pass attenuation: ", font=MEDIUM_FONT)
        labelText.place(relx=.04, rely=.6)
        entry_gpass.place(relx=.2, rely=.6)
        entry_gstop = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText2 = ttk.Label(
            self, text="Enter stop attenuation: ", font=MEDIUM_FONT)
        labelText2.place(relx=.04, rely=.65)
        entry_gstop.place(relx=.2, rely=.65)

        entry_rp = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText5 = ttk.Label(
            self, text="Enter max attenuation: ", font=MEDIUM_FONT)
        labelText5.place_forget()
        entry_rp.place_forget()

        entry_rs = tk.Entry(
            self, width=25, bg='white', fg='black')
        labelText6 = ttk.Label(
            self, text="Enter min attenuation: ", font=MEDIUM_FONT)
        labelText6.place_forget()
        entry_rs.place_forget()

        button_create_filter = ttk.Button(self, text="Design Filter",
                                          command=design_filter)
        button_create_filter.place(relx=.3, rely=.8)

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
        label.place(relx=.45, rely=.05)

        label_before = ttk.Label(self, text="Before", font=MEDIUM_FONT)
        label_before.place(relx=.2, rely=.1)

        label_after = ttk.Label(self, text="After", font=MEDIUM_FONT)
        label_after.place(relx=.6, rely=.1)

        def plot(t, s1, output):
            # the figure that will contain the plot
            fig = Figure(figsize=(3, 3),
                         dpi=100)
            # adding the subplot
            plot1 = fig.add_subplot(111)
            # plotting the graph
            plot1.plot(t[:300], s1.sum[:300])
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig,
                                       master=self)
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(relx=.2, rely=.15)

            # fig2
            f_sample = t.size
            xf = fftfreq(f_sample, 1/f_sample)
            fft_output2 = (fft(s1.sum))
            fft_output2 = fft_output2/np.max(fft_output2)
            fig2 = Figure(figsize=(3, 3),
                          dpi=100)
            plot2 = fig2.add_subplot(111)
            if controller.is_audio == False:
                plot2.plot(xf[0:20000], np.abs(fft_output2)[0:20000])
            else:
                plot2.plot(xf, np.abs(fft_output2))
            canvas = FigureCanvasTkAgg(fig2,
                                       master=self)
            canvas.draw()
            canvas.get_tk_widget().place(relx=.2, rely=.55)

            # fig3
            # the figure that will contain the plot
            fig3 = Figure(figsize=(3, 3),
                          dpi=100)
            # adding the subplot
            plot3 = fig3.add_subplot(111)
            # plotting the graph
            plot3.plot(t[:300], output[:300])
            # creating the Tkinter canvas
            # containing the Matplotlib figure
            canvas = FigureCanvasTkAgg(fig3,
                                       master=self)
            canvas.draw()
            # placing the canvas on the Tkinter window
            canvas.get_tk_widget().place(relx=.6, rely=.15)

            # fig4
            fft_output4 = (fft(output))
            fft_output4 = fft_output4/np.max(fft_output4)
            fig4 = Figure(figsize=(3, 3),
                          dpi=100)
            plot4 = fig4.add_subplot(111)
            if controller.is_audio == False:
                plot4.plot(xf[0:20000], np.abs(fft_output4)[0:20000])
            else:
                plot4.plot(xf, np.abs(fft_output4))
            canvas = FigureCanvasTkAgg(fig4,
                                       master=self)
            canvas.draw()
            canvas.get_tk_widget().place(relx=.6, rely=.55)

        def plot_result():
            if controller.is_audio == False:
                f_sample = 44000
                t = np.linspace(0, 1, f_sample)
            else:
                f_sample = 44000
                t = np.linspace(0, 5, 266240)
            s1 = controller.signal1
            filter1 = controller.filter1
            output = filter1.filter_apply(filter1.b, filter1.a, s1.sum)
            plot(t, s1, output)
            # if controller.is_audio == True:
            #     fs, data = wavfile.read('./audio/test.wav')
            #     sd.play(output, fs)

        button2 = ttk.Button(self, text="Plot Result",
                             command=plot_result)
        button2.place(relx=.44, rely=.5, width=100, height=30)

        button1 = ttk.Button(self, text="Back",
                             command=lambda: controller.show_frame(PageThree))
        button1.place(relx=.1, rely=.94)


class PageTen(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        signal1 = controller.signal1
        fs, data = wavfile.read('./audio/test.wav')

        def plot(t, s1):
            f_sample = t.size
            xf = fftfreq(f_sample, 1/f_sample)
            fft_output2 = (fft(s1.sum))
            fft_output2 = fft_output2/np.max(fft_output2)
            fig2 = Figure(figsize=(4, 4),
                          dpi=100)
            plot2 = fig2.add_subplot(111)
            plot2.plot(xf, np.abs(fft_output2))
            canvas = FigureCanvasTkAgg(fig2,
                                       master=self)
            canvas.draw()
            canvas.get_tk_widget().place(relx=.32, rely=.3)

        def play():
            sd.play(signal1.sum, fs)

        def add_high_frequency_noise():
            fs, data = wavfile.read('./audio/test.wav')
            signal1 = controller.signal1
            signal1.set_sum(data.T[0])
            f_sample = 44000
            t = np.linspace(0, 5, 266240)
            signal1.add_high_frequency_noise(t, 500)
            # plot
            plot(t, signal1)

        def add_white_noise():
            fs, data = wavfile.read('./audio/test.wav')
            signal1 = controller.signal1
            signal1.set_sum(data.T[0])
            f_sample = 44000
            t = np.linspace(0, 5, 266240)
            signal1.add_white_noise(500)
            # plot
            plot(t, signal1)

        def reset():
            fs, data = wavfile.read('./audio/test.wav')
            signal1 = controller.signal1
            signal1.set_sum(data.T[0])
            f_sample = 44000
            t = np.linspace(0, 5, 266240)
            # plot
            plot(t, signal1)

        label = ttk.Label(
            self, text="Choose the audio signal", font=LARGE_FONT)
        label.place(relx=.35, rely=.05)

        button1 = ttk.Button(self, text="Add high frequency noise",
                             command=add_high_frequency_noise)
        button1.place(relx=.2, rely=.15, width=150, height=50)

        button2 = ttk.Button(self, text="Add white noise",
                             command=add_white_noise)
        button2.place(relx=.6, rely=.15, width=150, height=50)

        button5 = ttk.Button(self, text="reset",
                             command=reset)
        button5.place(relx=.35, rely=.9)

        button6 = ttk.Button(self, text="play",
                             command=play)
        button6.place(relx=.6, rely=.9)

        button3 = ttk.Button(self, text="back",
                             command=lambda: controller.show_frame(PageOne))
        button3.place(relx=.1, rely=.9)

        button4 = ttk.Button(self, text="next",
                             command=lambda: controller.show_frame(PageThree))
        button4.place(relx=.85, rely=.9)


app = Projet()
app.iconbitmap('./img/ulfg_logo.ico')
app.resizable(False, False)
app.tk_setPalette('black')
app.mainloop()
