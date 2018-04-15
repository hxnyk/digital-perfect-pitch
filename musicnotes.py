#!/usr/bin/python3
from __future__ import  division

import os
import math
import numpy
import matplotlib
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft
from scipy.io import wavfile
from scipy.signal import correlate
from thinkdsp import Spectrogram
from thinkdsp import Spectrum
from thinkdsp import Wave
from thinkdsp import _SpectrumParent
import wave
import contextlib
import peakutils

import thinkdsp

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
            self.music_data[fi[0].upper()] = freq
        print (self.music_data)

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
        """ DEPRECATED """
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
        """ DEPRECATED """
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
    
    def GetNote3(self, filename):
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

    def hon(self, filename):
        rate, data = wavfile.read(filename)
        track = data.T[0]
        fft_track = fft(track)

        test = matplotlib.mlab.specgram(fft_track, NFFT=1024*6)
        print(type(test[0]))
        print(test[0].shape)
        print(len(test))
        # split this up

        # get max intensity


        plt.plot(test[0])
        plt.show()

    def getDuration(self, fname):
        
        with contextlib.closing(wave.open(fname,'r')) as f:
            frames = f.getnframes()
            rate = f.getframerate()
            duration = frames / float(rate)
            return duration    

    def getMultipleNotes(self, filename): 

        detected_notes = []
        parson_code = ""

        rate, data = wavfile.read(filename)
        test_track = data.T[0]
        fft_track = fft(test_track)

        numNotes = len(peakutils.indexes(fft_track, thres=0.02/max(fft_track), min_dist=rate/2))
        piano = thinkdsp.read_wave(filename)
        interval = self.getDuration(filename) / float(numNotes)

        spectrogram = piano.make_spectrogram(seg_length=1024)
        start = 0.0
        duration = interval
        for i in range(0, numNotes): 
            segment = piano.segment(start, duration)
            spectrum = segment.make_spectrum()
            freq = spectrum.peaks()[:1][0][1]
            note = self.__Pitch(freq)
            note_freq = (note, freq)
            detected_notes.append(note_freq)

            if i > 0: 
                if freq > detected_notes[i - 1][1]: 
                    parson_code += 'U'
                elif freq < detected_notes[i - 1][1]: 
                    parson_code += 'D'
                else: 
                    parson_code += 'R'

            start = start + duration
            duration = interval
        
        return (detected_notes, parson_code)
        