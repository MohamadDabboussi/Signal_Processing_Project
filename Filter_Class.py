from scipy import signal
import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, fftshift
import math
import numpy as np


class My_Filter:

    def __init__(self, filter_name=None, filter_type=None, fpass=None, fstop=None, gpass=None, gstop=None, order=None, Wn=None):
        self.filter_name = filter_name
        self.filter_type = filter_type
        self.order = order
        self.Wn = Wn
        self.fpass = np.array(fpass)
        self.fstop = np.array(fstop)
        self.gpass = gpass
        self.gstop = gstop

    def set_name(self, name):
        self.filter_name = name

    def set_type(self, filter_type):
        self.filter_type = filter_type

    def Normalize_Filter(self, frequency_sample):
        self.fpass = self.fpass/(frequency_sample/2)
        self.fstop = self.fstop/(frequency_sample/2)

    def PreWarping_Filter(self, Td):
        self.fpass = (2/Td)*np.tan(self.fpass*Td/2)
        self.fstop = (2/Td)*np.tan(self.fstop*Td/2)

    def filter_design(self, N=None, Wn=None, frequency_sample=None):
        if (N is None and Wn is None):
            if (self.filter_name == 'butter'):
                N, Wn = signal.buttord(self.fpass, self.fstop, self.gpass, self.gstop,
                                       analog=False)
            elif (self.filter_name == 'cheby1'):
                N, Wn = signal.cheb1ord(self.fpass, self.fstop, self.gpass, self.gstop,
                                        analog=False)
            elif (self.filter_name == 'cheby2'):
                N, Wn = signal.cheb2ord(self.fpass, self.fstop, self.gpass, self.gstop,
                                        analog=False)
            elif (self.filter_name == 'ellip'):
                N, Wn = signal.ellipord(self.fpass, self.fstop, self.gpass, self.gstop,
                                        analog=False)
        else:
            Wn = np.array(Wn)
            Wn = Wn/(frequency_sample/2)
        self.order = N
        self.Wn = Wn

    def filter_create(self, rp=None, rs=None):
        if (self.filter_name == 'butter'):
            b, a = signal.butter(self.order, self.Wn, self.filter_type, False)
        elif (self.filter_name == 'cheby1'):
            b, a = signal.cheby1(self.order, rp, self.Wn,
                                 self.filter_type, False)
        elif (self.filter_name == 'cheby2'):
            b, a = signal.cheby2(self.order, rs, self.Wn,
                                 self.filter_type, False)
        elif (self.filter_name == 'ellip'):
            b, a = signal.ellip(self.order, rp, rs,
                                self.Wn, self.filter_type, False)
        return b, a

    def filter_apply(self, b, a, s):
        w, h = signal.freqz(b, a, 512)
        output = signal.filtfilt(b, a, s)
        return output, w, h

    def filter_plot_prep(self, b, a):
        w, h = signal.freqz(b, a, 512)
        return w, h
