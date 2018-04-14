#!/usr/bin/python3

import os
import math
import numpy
import matplotlib
import scipy
import wave
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftshift
from scipy.io import wavfile
from scipy.signal import correlate
import peakutils

from math import log2


class MusicNote:
    """
    MusicNote is a library that fetches the specific musical pitch
    given an audio file.
    """
    NOTE_FILES = os.listdir("note_data/")
    music_data = {}

    def __init__(self):
        """Initalize MusicNote class."""
        self.__TrainData()

    def __TrainData(self):
        """Train piano note data."""
        for fi in self.NOTE_FILES:
            _, data = wavfile.read('note_data/' + fi)

            # .wav is a two channel audio file
            # 0 is the first track
            a = data.T[0]

            # Converts single channel domain to frequency domain
            b = fft(a)
            self.music_data[fi[0].upper()] = b

    def __Pitch(self, freq):
        """
        Returns which octave a note is (ie. C4, C5, C6)
        Using the Stuttgard pitch (C4 @ 440Hz) as baseline

        Referenced: johndcook.com/blog/2016/02/10/musical-pitch-notation/
        """

        # C near the hearing threshold is known as C0 and is 16Hz
        C0 = 16  # Hz
        name = ["C", "C#", "D", "D#", "E", "F",
                "F#", "G", "G#", "A", "A#", "B"]

        half_steps = round(12 * log2(freq / C0))
        octave = half_steps // 12  # Floor division
        num = half_steps % 12
        return name[num] + str(octave)

    def GetNote(self, filename):
        """Given a file, return what note is played."""
        _, data = wavfile.read(filename)
        a = data.T[0]
        b = fft(a)

        minimum = ["", numpy.finfo(numpy.float).max]
        for note, fft2 in self.music_data.items():
            corr = 0.0
            for i in range(len(fft2)):
                try:
                    corr += abs(b[i] - fft2[i])
                except:
                    break

            if corr <= minimum[1]:
                minimum = [note, corr]

        return minimum[0]

    def GetNote2(self, filename):
        rate, data = wavfile.read(filename)
        a = fft(data.T[0])

        '''if a.size % 2 != 0:
            indexVar  = a.size - 1
            numpy.delete(a, indexVar)
            print("LENGTHHHHHHH: " + str(a.size))
        '''
        #a = numpy.array_split(a, 2)[0]
        maximum = numpy.amax(a)
        for i, thing in enumerate(a):
            if thing == maximum:
                variable = i
                break

        #variable = a.index(maximum)
        # print(variable)
        b = numpy.fft.fftfreq(len(data.T[0]), 1 / rate)
        count = 0
        start = 0
        end = 0
        notes = []

        for i, thing in enumerate(b):
            if thing > 0:

                if b[i + 1] < 0:
                    end = i
                    freq_index = numpy.argmax(a[start:end])
                    freq = b[freq_index]
                    notes.append(self.__Pitch(freq))

                    #start = end + 1
            if thing < 0:
                if i + 1 == len(b):
                    break
                if b[i + 1] > 0:
                    start = i + 1

        #b = max(b)
        return notes

    def hon(self, filename):
        rate, data = wavfile.read(filename)
        fft_track = (fft(data.T[0]))
        f = numpy.linspace(0, rate/2, len(fft_track))

        test = matplotlib.mlab.specgram(fft_track, NFFT=1024 * 6, Fs=rate)
        spect = test[0]
        freqs = test[1]
        time_spectrum = test[2]

        """
        make array 
        """
        # plt.plot(f, fft_track)
        indexes = peakutils.indexes(fft_track, thres=0.02/max(fft_track), min_dist=rate/2)
        print("-------------HON-----------------")
        print(indexes)
        print(len(indexes))
        #plt.plot(f, fft_track) # peaks on x-axis is frequenciews i care about
        #plt.plot(spect) # peaks on x-axis is frequencies i care about
        #plt.show()

        plt.stem(spect)
        plt.show()

        pitches = []
        for idx in indexes:
            pitches.append(self.__Pitch(idx))
        print(pitches)

        everything = []

        for item in spect.tolist():
            for val in item:
                everything.append(val)

        #indexes = peakutils.indexes(everything, thres=0.02/max(everything), min_dist=100)
        # print(indexes)

        num = -1
        spectmax = numpy.argmax(spect)
        for i, item in enumerate(spect):
            if spectmax in item:
                num = i

        print(num)
        print(freqs[num])
        print(self.__Pitch(freqs[num]))
