import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from scipy.signal import correlate
import math 

fs, data = wavfile.read('note_data/a.wav')
a = data.T[0] 
b=[(ele/2**8.)*2-1 for ele in a]
c = fft(b)

'''
d = len(c)/2

plt.plot(abs(c[:(d-1)]),'r') 
plt.show()'''

<<<<<<< HEAD
fs1, data1 = wavfile.read('note_data/c.wav')
=======
fs1, data1 = wavfile.read('note_data/d.wav')
print(data1)
>>>>>>> 81befa22cefd2fef32a005f07d18d23f248ec281
a1 = data1.T[0]
print len(data1)
print type(data1)
b1=[(ele/2**8.)*2-1 for ele in a1]
c1 = fft(b1)

corr = 0
<<<<<<< HEAD
for i in range(0, len(c)):
    corr += abs(c[i] - c1[i])
print "Distance between C and D: ", corr
=======
for i in range(0, len(b)):
    corr += abs(b[i] - b1[i])
print("Distance between C and D: " + str(corr))
>>>>>>> 81befa22cefd2fef32a005f07d18d23f248ec281

'''
fs2, data2 = wavfile.read('note_data/c.wav')
a2 = data2.T[0]
b2 = fft(a2)

corr = 0
for i in range(0, len(b)):
    corr += abs(b[i] - b2[i])
print("Distance between C and C: " + str(corr) )
  

correlate = correlate(b, b1, 'full')
for num in correlate: 
    print num
print corr    
print correlate'''