from scipy.io import wavfile
import numpy as np
import scipy.fftpack

def tryreadwav(filename):
    fs, data = wavfile.read(filename)
    y = data
    N = len(y)
    T = 1.0/fs
    t = np.linspace(0,N*T,N)
    # y =1*(np.sin(w1*2*np.pi*t)+np.cos(w2*2*np.pi*t)+np.sin(w3*2*np.pi*t)+np.cos(w4*2*np.pi*t))
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T),int( N/2))
    a=2.0/N * np.abs(yf[:N//2])
    print(int(xf[np.argmax(a)]))
    b=np.where(a>(np.max(a)/2))
    frek=[]
    for i in b[0]:
        if int(xf[i]) not in frek:
            frek.append(int(xf[i]))
    return frek,len(data)
    # return frek[0:3],len(data)