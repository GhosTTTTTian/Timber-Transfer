import numpy as np
import pyaudio
import struct
import librosa
import math
import random
from scipy.signal import find_peaks
import matplotlib.pyplot as plt
from noise_extraction import noise

FREQUENCY = [196.00, 220.00, 246.94, 261.63, 293.67, 329,63, 349.23, 440.00,493.88,523.25, 587.33, 659.26, 698.46, 783.99, 880.00, 987.77, 1046.5, 1174.7]
note = ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'D6']

def find_peak(list):
    index = []
    for i in range(1, len(list)-1):
        if list[i] > list[i-1] and list[i] > list[i+1]:
            index.append(i)
    return index

def f0_detect(array, win_len, sr):
    FFT = abs(np.fft.rfft(array))
    # plt.figure(figsize=(30, 10))
    # plt.plot(FFT)
    # plt.show()
    x_axis = librosa.fft_frequencies(sr=sr, n_fft=win_len)
    binn = x_axis[1]-x_axis[0]
#     print(x_axis[:120])
    peaks,_ = find_peaks(FFT, height = 800000, distance =16)
#     peaks,_ = find_peaks(FFT, height = 20)
    if len(peaks) == 0:
        return 20
    else:
        # print('peaks', peaks)
    #     print('peaks*binn',peaks*binn)
        estimation = abs(FREQUENCY-peaks[0]*binn)
        # print(estimation)
        min_index = np.argmin(estimation)
        f0 = FREQUENCY[min_index]
        return min_index


DURATION = 60
MAXVALUE = 2**15-1

# filter = np.load('Liuqin_filter.npy')
# stretched_partials = np.load('Liuqin_stretched_partials.npy')
output_sine_l = np.load('Syn.npy')

CHANNELS        = 1     # Number of channels
RATE            = 44100     # Sampling rate (frames/second)
win_length      = 4096       # Signal length
WIDTH           = 2     # Number of bytes per sample
LEN             = DURATION * RATE
hop_len = int(win_length/8)

p = pyaudio.PyAudio()
stream = p.open(
    format      = pyaudio.paInt16,
    channels    = 1,
    rate        = RATE,
    input       = True,
    output      = True)

print('* Start')

num_blocks = int(RATE / win_length * DURATION)

for i in range(0, num_blocks):

    input_bytes = stream.read(win_length, exception_on_overflow=False)

    # Convert binary data to tuple of numbers
    input_tuple = struct.unpack('h' * win_length, input_bytes)

    # freq_A = librosa.stft(input_tuple, n_fft=win_length, hop_length = hop_len, win_length = win_length, window='hann')
    # freq = librosa.fft_frequencies(sr=RATE, n_fft=win_length)
    # print(len(freq_A), len(freq))
    # peak1 = find_peak(freq_A)
    min = f0_detect(input_tuple, win_length, RATE)
    print(min)



    if min == 20:
        print('null')
        output_sine = [0] * win_length

    else:
        print('min', note[min])
        output_sine = output_sine_l[min]

    output_noise = noise(np.array(input_tuple), win_length, 1)
    output_block = np.add(output_sine, output_noise)
    # output_block = output_sine
    # clipping
    output_block = np.clip(output_block, -MAXVALUE, MAXVALUE)

    # convert to integer
    output_block = output_block.astype(int)
    # print(type(output_block))
    # print(len(output_block[0]))

    # Convert output value to binary data
    binary_data = struct.pack('h' * win_length, *output_block)

    # Write binary data to audio stream
    stream.write(binary_data)


print('* Finished')

stream.stop_stream()
stream.close()
p.terminate()