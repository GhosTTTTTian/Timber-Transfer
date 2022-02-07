from pylab import *
import librosa
import librosa.display
import IPython.display
import matplotlib.pyplot as plt
import matplotlib.style as ms
import numpy as np
from scipy.signal.windows import hann
import pandas as pd
import csv
from sklearn.linear_model import LinearRegression
import numpy as np
from scipy.signal import find_peaks

def peak_detect2(listy, dis):
    peaks,_ = find_peaks(listy, distance = int(dis/1.3))
    return peaks

stretched_partials = [[0]*18 for i in range(19)]
amplitude = [[0]*18 for i in range(19)]

note = ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5',
        'E5', 'F5', 'G5', 'A5', 'B5', 'C6','D6']
F0 = [195, 219, 245.94, 260.63, 292.67, 328.63, 348.23, 391, 439, 492.88, 522.25,
      586.33, 658.26, 697.46, 783, 879, 986.77, 1045.5, 1173.7]


for i in range(19):
    file_name = note[i] + '.wav'
    b, sr = librosa.load('./Liuqin/' + file_name, sr=44100)
    k = int(32768)
    h = int(k / 8)
    B = librosa.stft(b, n_fft=k, hop_length=h, win_length=k, window='hann')
    abs_B = np.abs(B)[:, 0]
    #     print(len(B), len(abs_B))
    #     print(abs_B)
    freq_B = librosa.fft_frequencies(sr=sr, n_fft=k)
    #     print(freq_B)
    # #     print(len(freq_B))

    index = peak_detect2(abs_B, F0[i])
    #     print(index)

    x = []
    y = []
    for k in index:
        x.append(freq_B[k])
        y.append(abs_B[k])
    #     plt.figure(figsize=(30, 10))
    #     plt.scatter(x, y)

    for n in range(0, 17):
        amplitude[i][n] = y[n]

#         print(x[n])

#     plt.figure(figsize=(30, 10))
#     plt.scatter(x[1:], y[1:], color = 'red', marker = 'x')
#     plt.plot(freq_B,abs_B)
#     plt.title("Harmonic Series of " + note[i])
#     plt.savefig("./Piano_Plot/"+"har_"+note[i])
#     plt.show()

np.save('Liuqin_amplitude.npy', amplitude)

for i in range(19):
    file_name = note[i] + '.wav'
    b, sr = librosa.load('./Piano/' + file_name, sr=44100)
    k = int(32768)
    h = int(k / 8)
    B = librosa.stft(b, n_fft=k, hop_length=h, win_length=k, window='hann')
    abs_B = np.abs(B)[:, 0]
    #     print(len(B), len(abs_B))
    #     print(abs_B)
    freq_B = librosa.fft_frequencies(sr=sr, n_fft=k)
    #     print(freq_B)
    # #     print(len(freq_B))

    index = peak_detect2(abs_B, F0[i])
    #     print(index)

    x = []
    y = []
    for k in index:
        x.append(freq_B[k])
        y.append(abs_B[k])
    #     plt.figure(figsize=(30, 10))
    #     plt.scatter(x, y)

    for n in range(1, 17):
        stretched_partials[i][n - 1] = x[n]

    #         print(x[n])

    plt.figure(figsize=(30, 10))
    plt.scatter(x[1:], y[1:], color='red', marker='x')
    plt.plot(freq_B, abs_B)
    plt.title("Harmonic Series of " + note[i])
    plt.savefig("./Piano_Plot/" + "har_" + note[i])
    plt.show()

np.save('Liuqin_inharmonics.npy', stretched_partials)

inharmonics = [[0]*18 for i in range(19)]
for m in range(19):
    for n in range(1,18):
        inharmonics[m][n] = stretched_partials[m][n]- (n+1)*stretched_partials[m][0]
        print(m, n, inharmonics[m][n])

np.save('Liuqin_stretched_partials.npy', inharmonics)