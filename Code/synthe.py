import numpy as np
import math
import matplotlib.pyplot as plt

win_length = 4096

FREQUENCY = [196.00, 220.00, 246.94, 261.63, 293.67, 329,63, 349.23, 440.00,493.88,523.25, 587.33, 659.26, 698.46, 783.99, 880.00, 987.77, 1046.5, 1174.7]
note = ['G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'B5', 'C6', 'D6']


inharmonics = np.load('Liuqin_inharmonics.npy')
amplitude = np.load('Liuqin_amplitude.npy')
f_h =  np.zeros([19,18])
# for i in range(19):#fundamental frequency
#     for j in range(18): #harmonic level
#         f_h[i][j] = inharmonics[i][j]
# print(len(f_h))


output_sine =  np.zeros([19,4096])
for x in range(19):
    for y in range(18):
        print('x', x, 'y', y, 'freq', inharmonics[x][y], 'amp', amplitude[x][y] )
        # sinex = np.zeros(4096)
        # for t in range(4096):
        #     sinex[t] =  math.cos(2*math.pi*(x+5)*t)
        sinex = [ amplitude[x][y] * math.cos(math.pi * 2 * inharmonics[x][y] * t / 44100)  for t in range(4096)]


        # plt.plot(sinex, color = 'b', alpha = 0.5)
        # plt.title(x)
        # plt.show()
        output_sine[x] += sinex
        # plt.plot(output_sine[x])
        # plt.show()
    plt.plot(output_sine[x])
    plt.show()
    # output_sine[x] = int(output_sine[x])
print(output_sine.size)
print(len(output_sine))
print(len(output_sine[0]))

np.save('Syn.npy', output_sine)
