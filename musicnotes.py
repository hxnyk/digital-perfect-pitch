#!/usr/bin/python3
from __future__ import division

import os
import math
import matplotlib.pyplot as plt
import numpy
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from scipy.signal import correlate

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
            rate, data = wavfile.read('note_data/' + fi)
            non_norm_freqs = []
            notes = []
            # .wav is a two channel audio file
            # 0 is the first track
            first_track = data.T[0]
            # Converts single channel domain to frequency domain
            fft_arr= fft(first_track)
            #get first half of fft - corresponds to positive frequencies. Ignores negative ones 
            split_fft = numpy.array_split(fft_arr, 2)[0]
            #get index of maximum intensity
            maximum_index = numpy.argmax(split_fft)
            #create frequency array (the x axis of the fourier transform)
            fft_freqs = numpy.fft.fftfreq(len(data.T[0]), 1 / rate)
            #find the frequency at the corresponding max y value (intensity)
            freq = fft_freqs[maximum_index]
            norm_freqs.append(freq)
            notes.append(fi[0].upper())

        norm_freqs = numpy.linalg.norm(non_norm_freqs)
        for i, freqs in enumerate(non_norm_freqs): 
            self.music_data[notes[i]] = freqs

    #function not working right now - will probably delete
    '''
    def __FindMaxFreq(self, fft_arr, rate, data_length): 
        #get first half of fft - corresponds to positive frequencies. Ignores negative ones 
        split_fft = numpy.array_split(fft_arr, 2)[0]
        #get index of maximum intensity
        maximum_index = numpy.argmax(split_fft)
        #create frequency array (the x axis of the fourier transform)
        fft_freqs = numpy.fft.fftfreq(data_length, 1 / rate)
        #find the frequency at the corresponding max y value (intensity)
        freq = fft_freqs[maximum_index]
        return freq'''

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
        rate, data = wavfile.read(filename)
        test_track = data.T[0]
        test_fft = fft(test_track)
        split_fft = numpy.array_split(test_fft, 2)[0]
        maximum_index = numpy.argmax(split_fft)
        #create frequency array (the x axis of the fourier transform)
        fft_freqs = numpy.fft.fftfreq(len(data.T[0]), 1 / rate)
        #find the frequency at the corresponding max y value (intensity)
        input_freq = fft_freqs[maximum_index]

        #[note, freq, higher/lower octave, octave difference from training octave]
        minimum = ["", math.inf, "", ""]
        lower_octave = "no"
        higher_octave = "no"
        for note, training_freq in self.music_data.items():
            if input_freq >= training_freq - 10.0 and input_freq <= training_freq + 10.0:
                minimum = [note, input_freq, "different", 0]
                break; 
            elif input_freq < training_freq: 
                #7 octaves on a piano
                for multiplier in range(1, 8): 
                    new_training_freq = training_freq * (1 / (2 * multiplier))
                    if input_freq >= new_training_freq - 10.0 and input_freq <= new_training_freq + 10.0 : 
                        lower_octave = "yes"
                        minimum = [note, input_freq, "lower", multiplier]
                        break; 

            if lower_octave == "yes": 
                break; 

            else: 
                for multiplier in range(1,8): 
                    new_training_freq = training_freq * (2 * multiplier)
                    if input_freq >= new_training_freq - 10.0 and input_freq <= new_training_freq + 10.0: 
                        higher_octave == "yes"
                        minimum = [note, input_freq, "higher", multiplier]

        return minimum

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
        #print(variable)
        b = numpy.fft.fftfreq(len(data.T[0]), 1 / rate)
        count = 0
        start = 0
        end = 0
        notes = []
        for i, thing in enumerate(b):
            if thing > 0:

                if b[i+1] < 0:
                    end = i
                    freq_index = numpy.argmax(a[start:end])
                    freq = b[freq_index]
                    notes.append(self.__Pitch(freq))

                    #start = end + 1
            if thing < 0:
                if i+1 == len(b):
                    break
                if b[i+1] > 0:
                    start = i+1





        #b = max(b)
        return notes

def mutipleNotes(self, filename): 
    rate, data = wavfile.read(filename)
    separate_notes = numpy.array_split(data, 6)
    test_track = fft(separate_notes[0])

    test_fft = fft(test_track)
    split_fft = numpy.array_split(test_fft, 2)[0]
    maximum_index = numpy.argmax(split_fft)
    #create frequency array (the x axis of the fourier transform)
    fft_freqs = numpy.fft.fftfreq(len(data.T[0]), 1 / rate)
    #find the frequency at the corresponding max y value (intensity)
    input_freq = fft_freqs[maximum_index]

    print (input_freq)


    '''
    test = matplotlib.mlab.specgram(fft_track, NFFT=1024 * 6)
    spect = test[0]
    freqs = test[1]
    time_spectrum = test[2]

    num = 0
    spectmax = numpy.argmax(spect)
    for i, item in enumerate(spect):
        if spectmax in item:
            num = i'''