from pylab import *
import matplotlib.pyplot as plt
import math
import struct
import pyaudio
import random
import numpy as np

# noise_extraction using wavelet transform
h0 = (1+math.sqrt(3))/(4*math.sqrt(2))
h1 = (3+math.sqrt(3))/(4*math.sqrt(2))
h2 = (3-math.sqrt(3))/(4*math.sqrt(2))
h3 = (1-math.sqrt(3))/(4*math.sqrt(2))

thresh = 100

def cn(x0, x1, x2, x3):
    return h0*x0+h1*x1+h2*x2+h3*x3

def dn(x0, x1, x2, x3):
    return h3*x0-h2*x1+h1*x2-h0*x3

def y_even(c1, c0, d1, d0):
    return h0*c1+h2*c0+h3*d1+h1*d0

def y_odd(c1, c0, d1, d0):
    return h1*c1+h3*c0-h2*d1-h0*d0

def slicing(array):
    arr1 = array
    arr2 = array[1:]
    arr3 = array[2:]
    arr4 = array[3:]
    return arr1, arr2, arr3, arr4

def filt1(n):
    if n>thresh:
        re =  thresh
    elif n<(-1)*thresh:
        re = thresh
    else:
        re = n
    return re


def filt0(n):
    if n>0 and n<thresh:
        re =  0
    elif n<0 and n>(-1)*thresh:
        re = 0
    else:
        re = n
    return re

def noise(array,length, flag = 0):

    d1 = [0] * int(length/2)
    c1 = [0] * int(length /2)
    d2 = [0] * int(length/4)
    c2 = [0] * int(length /4)
    d3 = [0] * int(length/8)
    c3 = [0] * int(length /8)
    d4 = [0] * int(length/16)
    c4 = [0] * int(length/16)

    y1 = [0] * int(length / 2)
    y2 = [0] * int(length / 4)
    y3 = [0] * int(length / 8)
    y = [0] * length
    # print(array)
    # print(array[2*5])

    l11, l12, l13, l14 = slicing(array)
    if flag == 0:
        for i in range(0, int(len(l14)/2)):
            # print(i)
            c1[i] = cn(l11[2*i], l12[2*i], l13[2*i], l14[2*i])
            d1[i] = dn(l11[2*i], l12[2*i], l13[2*i], l14[2*i])
            d1[i] = filt0(d1[i])
        l21, l22, l23, l24 = slicing(c1)

        for j in range(0, int(len(l24)/2)):
            c2[j] = cn(l21[2*j], l22[2*j], l23[2*j], l24[2*j])
            d2[j] = dn(l21[2*j], l22[2*j], l23[2*j], l24[2*j])
            d2[j] = filt0(d2[j])
        l31, l32, l33, l34 = slicing(c2)

        for k in range(0, int(len(l34)/2)):
            c3[k] = cn(l31[2*k], l32[2*k], l33[2*k], l34[2*k])
            d3[k] = dn(l31[2*k], l32[2*k], l33[2*k], l34[2*k])
            d3[k] = filt0(d3[k])

        l41, l42, l43, l44 = slicing(c3)

        for m in range(0, int(len(l44)/2)):
            c4[m] = cn(l41[2*m], l42[2*m], l43[2*m], l44[2*m])
            d4[m] = dn(l41[2*m], l32[2*m], l43[2*m], l44[2*m])
            c4[m] = filt0(c4[m])
            d4[m] = filt0(d4[m])
    else:
        for i in range(0, int(len(l14) / 2)):
            # print(i)
            c1[i] = cn(l11[2 * i], l12[2 * i], l13[2 * i], l14[2 * i])
            d1[i] = dn(l11[2 * i], l12[2 * i], l13[2 * i], l14[2 * i])
            d1[i] = filt1(d1[i])
        l21, l22, l23, l24 = slicing(c1)

        for j in range(0, int(len(l24) / 2)):
            c2[j] = cn(l21[2 * j], l22[2 * j], l23[2 * j], l24[2 * j])
            d2[j] = dn(l21[2 * j], l22[2 * j], l23[2 * j], l24[2 * j])
            d2[j] = filt1(d2[j])
        l31, l32, l33, l34 = slicing(c2)

        for k in range(0, int(len(l34) / 2)):
            c3[k] = cn(l31[2 * k], l32[2 * k], l33[2 * k], l34[2 * k])
            d3[k] = dn(l31[2 * k], l32[2 * k], l33[2 * k], l34[2 * k])
            d3[k] = filt1(d3[k])

        l41, l42, l43, l44 = slicing(c3)

        for m in range(0, int(len(l44) / 2)):
            c4[m] = cn(l41[2 * m], l42[2 * m], l43[2 * m], l44[2 * m])
            d4[m] = dn(l41[2 * m], l32[2 * m], l43[2 * m], l44[2 * m])
            c4[m] = filt1(c4[m])
            d4[m] = filt1(d4[m])


    # for i in range(2045):
    #     print(i)
    #     d1[i] = dn(array[2*i], array[2*i+1], array[2*i+2], array[2*i+3])
    #     print(i, d1[i], 2*i, 2*i+1, 2*i+2, 2*i+3)
    #     if d1[i] >thresh:
    #         d1[i] = thresh
    #
    #     elif d1[i] < (-1)*thresh:
    #         d1[i] = (-1)*thresh
    #     c1[i] = cn(array[2*i], array[2*i+1], array[2*i+2], array[2*i+3])
    #     print(c1[i])
    # for j in range(1020):
    #     d2[j] = dn(c1[2*j], c1[2*j+1], c1[2*j+2], c1[2*j+3])
    #     if d2[j] >thresh:
    #         d2[j] = thresh
    #     elif d2[j] <(-1)*thresh:
    #         d2[j] = (-1)*thresh
    #     c2[j] = cn(c1[2 * j], c1[2 * j + 1], c1[2 * j + 2], c1[2 * j + 3])
    # for k in range(507):
    #     d3[k] = dn(c2[2 * k], c2[2 * k + 1], c2[2 * k + 2], c2[2 * k + 3])
    #     if d3[k] >thresh:
    #         d3[k] = thresh
    #     elif d3[k] <(-1)*thresh:
    #         d3[k] =(-1)*thresh
    #     c3[k] = cn(c2[2 * k], c2[2 * k + 1], c2[2 * k + 2], c2[2 * k + 3])
    # for l in range(249):
    #     d4[l] = dn(c3[2 * l], c3[2 * l + 1], c3[2 *l + 2], c3[2 * l + 3])
    #     if d4[l] > thresh:
    #         d4[l] = thresh
    #     elif d4[l] <(-1)*thresh:
    #         d4[l] =(-1)*thresh
    #     c4[l] = cn(c3[2 * l], c3[2 * l + 1], c3[2 * l + 2], c3[2 * l + 3])
    #     if c4[l] > thresh:
    #         c4[l] = thresh
    #     elif c4[l] < (-1)*thresh:
    #         c4[l] = (-1)*thresh
    #
    for i in range(0,len(d4)):
        y3[2*i] = y_odd(c4[i], c4[i-1], d4[i], d4[i-1])
        y3[2*i+1] = y_even(c4[i], c4[i-1], d4[i], d4[i-1])
    for i in range(0, len(d3)):
        y2[2*i] = y_odd(y3[i], y3[i - 1], d3[i], d3[i - 1])
        y2[2*i+1] = y_even(y3[i], y3[i - 1], d3[i], d3[i - 1])
    for i in range(0, len(d2)):
        y1[2*i] = y_odd(y2[i], y2[i - 1], d2[i], d2[i - 1])
        y1[2*i+1] = y_even(y2[i], y2[i - 1], d2[i], d2[i - 1])
    for i in range(0, len(d1)):
        y[2*i] = y_odd(y1[i], y1[i - 1], d1[i], d1[i - 1])
        y[2*i+1] = y_even(y1[i], y1[i - 1], d1[i], d1[i - 1])


    noise_A = y
    return noise_A

# output_noise = []
# for i in range(4096):
#     output_noise.append(random.randint(-1000,1000))
#
#
#
# # print(output_noise)
# result = noise(output_noise, 4096)
# plt.plot(output_noise, color = 'b', alpha = 0.5)
# plt.plot(result, color = 'r', alpha = 0.5)
# plt.show()


# DURATION = 1
# MAXVALUE = 2**15-1
#
# CHANNELS        = 1     # Number of channels
# RATE            = 44100     # Sampling rate (frames/second)
# win_length      = 4096       # Signal length
# WIDTH           = 2     # Number of bytes per sample
# LEN             = DURATION * RATE
# hop_len = int(win_length/8)
#
# p = pyaudio.PyAudio()
# stream = p.open(
#     format      = pyaudio.paInt16,
#     channels    = 1,
#     rate        = RATE,
#     input       = True,
#     output      = False)
#
# print('* Start')
#
# num_blocks = int(RATE / win_length * DURATION)
#
# for i in range(0, num_blocks):
#
#     input_bytes = stream.read(win_length, exception_on_overflow=False)
#
#     # Convert binary data to tuple of numbers
#     input_tuple = struct.unpack('h' * win_length, input_bytes)
#
#     # freq_A = librosa.stft(input_tuple, n_fft=win_length, hop_length = hop_len, win_length = win_length, window='hann')
#     # freq = librosa.fft_frequencies(sr=RATE, n_fft=win_length)
#     # print(len(freq_A), len(freq))
#     # peak1 = find_peak(freq_A)
#     inpu = np.array(input_tuple)
#     print(inpu)
#     noisy = noise(inpu, win_length)
#
#     plt.plot(input_tuple, color = 'b')
#     plt.plot(noisy, color = 'r')
#     plt.show()




# print('* Finished')
#
# stream.stop_stream()
# stream.close()
# p.terminate()
