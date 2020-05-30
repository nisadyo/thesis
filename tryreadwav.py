from scipy.io import wavfile
import numpy as np
import scipy.fftpack
import gammatone

def tryReadWavRecord(filename):
    fs, data = wavfile.read(filename)
    y = data
    N = len(y)
    T = 1.0/fs
    print(fs)
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
    print(frek)
    # return frek,len(data)
    return fs, frek[0:3], len(data)

def tryReadWavAudio(filename):
    fs, data = wavfile.read(filename)
    y = [i[0] for i in data]
    N = len(y)
    T = 1.0/fs
    t = np.linspace(0,N*T,N)
    # y =1*(np.sin(w1*2*np.pi*t)+np.cos(w2*2*np.pi*t)+np.sin(w3*2*np.pi*t)+np.cos(w4*2*np.pi*t))
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T),int( N/2))
    a = 2.0/N * np.abs(yf[:N//2]) #spectrum
    print(int(xf[np.argmax(a)]))
    b = np.where(a>(np.max(a)/2))
    frek = []
    for i in b[0]:
        if int(xf[i]) not in frek:
            frek.append(int(xf[i]))
    return fs, frek, len(data[0])

def tryReadGammatone(filename):
    fs, data = wavfile.read(filename)
    y = data
    N = len(y)
    T = 1.0/fs
    t = np.linspace(0,N*T,N)
    # y =1*(np.sin(w1*2*np.pi*t)+np.cos(w2*2*np.pi*t)+np.sin(w3*2*np.pi*t)+np.cos(w4*2*np.pi*t))
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T),int( N/2))
    a=2.0/N * np.abs(yf[:N//2])
    b=np.where(a>(np.max(a)/2))
    frek=[]
    for i in b[0]:
        if int(xf[i]) not in frek:
            frek.append(int(xf[i]))
    center = gammatone.filters.centre_freqs(fs, 1, frek[0])
    fcoefs = gammatone.filters.make_erb_filters(fs, center, 100)
    
    norm = gammatone.filters.erb_space(frek[0], frek[2], len(fcoefs[0]))
    # print("ini norm")
    norm=norm.tolist()
    # return frek,len(data)
    return fs, fcoefs, norm