from scipy.io import wavfile
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.fftpack import fft, fftfreq, fftshift
from IPython.display import Audio
from Filter_Class import My_Filter


f_sample = 44000
f_pass = [1000]
f_stop = [1500]
f_pass = [550, 1100]
f_stop = [100, 1800]
g_pass = 0.5
g_stop = 40
Td = 1

t = np.linspace(0, 1, f_sample)
f1 = 1000
f2 = 600
signal1 = 20*np.sin(2*np.pi*f1*t)+10*np.sin(2*np.pi*f2*t)
signal1 = signal1
mean = 0
std = 1
num_samples = signal1.size
noise1 = np.random.normal(mean, std, size=num_samples)
s = signal1+noise1


###############################################################################################

filtre1 = My_Filter('butter', 'band', f_pass, f_stop, g_pass, g_stop)
filtre1.Normalize_Filter(f_sample)
filtre1.PreWarping_Filter(Td)
filtre1.filter_design()
b, a = filtre1.filter_create()
output, w, h = filtre1.filter_apply(b, a, s)
Wn = filtre1.Wn

plt.semilogx(w*f_sample/(2*math.pi), 20*np.log10(abs(h)))
plt.xscale('log')
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
if(Wn.size > 1):
    plt.axvline(Wn[0]*f_sample/2, color='green')
    plt.axvline(Wn[1]*f_sample/2, color='green')
else:
    plt.axvline(Wn*f_sample/2, color='green')
plt.show()

plt.plot(t[0:200], s[0:200])
plt.show()
plt.plot(t[0:200], output[0:200])
plt.show()

xf = fftfreq(f_sample, 1/f_sample)
fft_output = (fft(output))
fft_output = fft_output/np.max(fft_output)
plt.plot(xf, np.abs(fft_output))
plt.show()


###############################################################################################

###############################################################################################


Wn = [500, 1200]
Wn = 1200

filtre2 = My_Filter('butter', 'low')
filtre2.filter_design(10, Wn, f_sample)
b2, a2 = filtre2.filter_create(rs=40)
output2, w2, h2 = filtre2.filter_apply(b2, a2, s)
Wn = filtre2.Wn

plt.semilogx(w2*f_sample/(2*math.pi), 20*np.log10(abs(h2)))
plt.xscale('log')
plt.title('Butterworth filter frequency response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Amplitude [dB]')
plt.margins(0, 0.1)
plt.grid(which='both', axis='both')
if(Wn.size > 1):
    plt.axvline(Wn[0]*f_sample/2, color='green')
    plt.axvline(Wn[1]*f_sample/2, color='green')
else:
    plt.axvline(Wn*f_sample/2, color='green')
plt.show()

plt.plot(t[0:200], s[0:200])
plt.show()
plt.plot(t[0:200], output2[0:200])
plt.show()

xf = fftfreq(f_sample, 1/f_sample)
fft_output2 = (fft(output2))
fft_output2 = fft_output2/np.max(fft_output2)
plt.plot(xf, np.abs(fft_output2))
plt.show()
