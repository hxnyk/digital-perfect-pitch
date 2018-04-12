from __future__ import print_function, division

import thinkdsp
import thinkplot
import matplotlib.pyplot as pyplot

import numpy

#fs, data = wavfile.read('b1.wav')  


#wave = mix.make_wave(duration=0.5, start=0, framerate=11025)
wave = thinkdsp.read_wave('hbd.wav')


#spectrum = wave.make_spectrum()
#thinkplot.config(xlabel='time (s)', legend=False)
#period = mix.period
#segment = wave.segment(start=0, duration=period*3)
#segment.plot()
spectrogram = wave.make_spectrogram(seg_length=1024)
'''start = 0.5
duration = 3.
segment = wave.segment(start, duration)
'''
#spectrum = segment.make_spectrum()


spectrogram.plot(high = 1000)
#thinkplot.show()




pyplot.show()