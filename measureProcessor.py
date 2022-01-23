import json
import numpy as np
from scipy.fft import fft
from scipy.fft import rfft, rfftfreq
from scipy.signal import find_peaks


def thd(abs_data,xpeak):  
    sq_sum=0.0
    for r in range(len(abs_data)):
        if(r in xpeak):
            sq_sum = sq_sum + (abs_data[r])**2

    sq_harmonics = sq_sum -(max(abs_data))**2
    thd = sq_harmonics**0.5 / max(abs_data)

    return thd

def distortionFactor(thd):
    den = 1+(thd**2)
    return (1/den)**.5
 

filename = 'measure.json'
# Opening JSON file
f = open(filename)
data = json.load(f)
f.close()

sample_balanced = data['current'] - np.mean(data['current'])


abs_yf = np.abs(fft(sample_balanced))

SAMPLE_RATE = 2500  # Hertz
DURATION = 1

N = SAMPLE_RATE * DURATION

f_signal = rfft(sample_balanced)
xf = rfftfreq(N, 1 / SAMPLE_RATE)

yf = f_signal.copy()
xpeak,ypeak = find_peaks(abs(yf), distance=25)
# yf[(np.abs(xf)>3)] = 0 # cut signal above 3Hz


for x in range(5):
    yf[x] = 0


thd_value = thd(abs(yf), xpeak)
print ("Total Harmonic Distortion:")
print ("\t{:.4f}".format(thd_value*100),"%")

df_value = distortionFactor(thd_value)
print ("Distorsion factor:")
print ("\t{:.4f}".format(df_value))

print ("Displacement factor 'cos(phi)':")
cosphi = 0
print ('\t',cosphi)

print("Power Factor = Displacement Factor x Distortion Factor:")
print ("\t{:.4f}".format(df_value+cosphi))
