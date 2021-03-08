import matplotlib.pyplot as plt
from scipy.fftpack import fft, fftfreq, fftshift
import math
import numpy as np


class My_Signal:
    def __init__(self, t=None, amplitude=None, frequency=None):
        self.amplitude = amplitude
        self.frequency = frequency
        if not (amplitude == None or frequency == None):
            self.sum = self.amplitude*np.sin(2*np.pi*self.frequency*t)
        else:
            self.sum = 0

    def add_signal(self, t, amplitude, frequency):
        self.sum = self.sum+amplitude*np.sin(2*np.pi*frequency*t)

    def add_white_noise(self, amplitude=1):
        mean = 0
        std = 1
        num_samples = self.sum.size
        noise = amplitude*np.random.normal(mean, std, size=num_samples)
        self.sum = self.sum+noise

    def reset_signal(self):
        self.sum = np.zeros(self.sum.size)


# f_sample = 44000
# t = np.linspace(0, 1, f_sample)
# s1 = My_Signal()
# s1.add_signal(t, 20, 1000)
# s1.add_signal(t, 10, 600)
# s1.add_white_noise(20)

# xf = fftfreq(f_sample, 1/f_sample)
# fft_output2 = (fft(s1.sum))
# fft_output2 = fft_output2/np.max(fft_output2)
# plt.plot(xf, np.abs(fft_output2))
# plt.show()
