#!/usr/bin/python3

import os
import math
import matplotlib.pyplot as plt
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
        return None
