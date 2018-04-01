#!/usr/bin/python3

import os
import math
import matplotlib.pyplot as plt
import numpy
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from scipy.signal import correlate


class MusicNote:
    """
    MusicNote is a library that fetches the specific musical pitch
    given an audio file.
    """
    NOTE_FILES = os.listdir("note_data/")
    music_data = {}

    def __init__(self):
        """Initalize MusicNote class."""
        self.TrainData()

    def TrainData(self):
        for fi in self.NOTE_FILES:
            _, data = wavfile.read('note_data/' + fi)

            # .wav is a two channel audio file
            # 0 is the first track
            a = data.T[0]

            # Converts single channel domain to frequency domain
            b = fft(a)
            self.music_data[fi[0].upper()] = b

    def GetNote(self, filename):
        _, data = wavfile.read(filename)
        a = data.T[0]
        b = fft(a)

        minimum = ["", numpy.finfo(numpy.float).max]
        for note, fft2 in self.music_data.items():
            corr = 0.0
            for i in range(len(b)):
                corr += abs(b[i] - fft2[i])

            print("b: " + str(type(b)))
            print("fft: " + str(type(fft2)) + "\n")

            print(str(type(corr)) + " " + str(corr))
            print(corr)

            print(str(type(minimum[1])) + " " + str(minimum[1]))
            print(minimum[1])
            print("=======================================================\n")
            if corr < minimum[1]:
                print("New fft value: " str(fft2))
                minimum = [note, fft2]

        print("Note is: " + str(note))
        return note
