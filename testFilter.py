from scipy.io import wavfile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftfreq, fftshift
from IPython.display import Audio


f_sample = 44000
mean = 0
std = 1
num_samples = 266240
t = np.linspace(0, 5, 266240)
noise1 = 500*(np.sin(2*np.pi*8000*t)+np.sin(2*np.pi*7000*t) +
              np.sin(2*np.pi*6000*t)+np.sin(2*np.pi*10000*t))

# noise = 5000*np.random.normal(mean, std, size=num_samples)
# nf = fftfreq(266240, 1)
# fft_noise = (fft(noise))
# fft_noise[:60000] = 0

# fs, ys = wavfile.read("test.wav")
# s = ys.T[0]+noise

# f = np.linspace(-f_sample/2, f_sample/2-1, 44000)
# xf = fftfreq(266240, 1)
# fft_s = (fft(s))
#noise1 = 5000*np.random.normal(mean, std, size=num_samples)
fs, ys = wavfile.read("test.wav")
s = ys.T[0]+noise1
plt.plot(t, s)
plt.show()

f = np.linspace(-f_sample/2, f_sample/2-1, 44000)
xf = fftfreq(266240, 1)
fft_s = (fft(s))
plt.plot(xf, fft_s)
plt.show()

f_pass = 3500
f_stop = 5000
wp = f_pass/(f_sample/2)
ws = f_stop/(f_sample/2)
g_pass = 0.5
g_stop = 65
Td = 1

omega_p = (2/Td)*np.tan(wp*Td/2)
omega_s = (2/Td)*np.tan(ws*Td/2)
N, Wn = signal.buttord(omega_p, omega_s, g_pass, g_stop,
                       analog=False)

b, a = signal.butter(N, Wn, 'low', False)
w, h = signal.freqz(b, a, 512)

plt.semilogx(w*f_sample/(2*math.pi), 20*np.log10(abs(h)))
plt.xscale('log')
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
plt.axvline(Wn*f_sample/2, color='green')
plt.show()


output = signal.filtfilt(b, a, s)
f = np.linspace(-f_sample/2, f_sample/2-1, 44000)
xf = fftfreq(266240, Td)
fft_output = (fft(output))
plt.plot(xf, fft_output)
plt.show()

Audio(s, rate=fs)

Audio(output, rate=fs)
