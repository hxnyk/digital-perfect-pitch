#!/usr/bin/python3
from __future__ import  division

import os
import json
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
import zeep
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import pygame


import thinkdsp

from math import log2


class MusicNote:
    """
    MusicNote is a library that fetches the specific musical pitch
    given an audio file.
    """
    NOTE_FILES = os.listdir("note_data/")
    NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    music_data = {}
    note_values = {"C": 1, "D": 2, "E": 3, "F": 4, "G": 5, "A": 6, "B": 7}

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

    def IsAccurate(self, note_data): 
        calc_note = note_data[0] + str(note_data[4])
        acc_note = note_data[5]
        if calc_note == acc_note: 
            return "yes"
        else: 
            return "no"

    def CalculateOctave(self, note, difference): 
        if note == 'A' or note == 'B': 
            calculated_octave = 4 + difference
        elif note == 'C' or note == 'D' or note == 'F' or note == 'G': 
            calculated_octave = 5 + difference
        else: 
            calculated_octave = 6 + difference

        return calculated_octave  

    def GetAccNote(self, freq):
        accurate_note = self.__Pitch(freq)
        return accurate_note
    
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

        #[note, freq, higher/lower octave, octave difference from training octave, calculated octave, accurate note]
        minimum = ["", math.inf, "", "", "", 0]
        lower_octave = "no"
        higher_octave = "no"
        accuracy_count = 0
        for note, training_freq in self.music_data.items():
            acc_note = self.GetAccNote(input_freq)
            if input_freq >= training_freq - 10.0 and input_freq <= training_freq + 10.0: 
                calc_octave = self.CalculateOctave(note, 0)  
                minimum = [note, input_freq, "different", 0, calc_octave, acc_note]
                break; 
            elif input_freq < training_freq: 
                #7 octaves on a piano
                for multiplier in range(1, 8): 
                    new_training_freq = training_freq * (1 / (2 * multiplier))
                    if input_freq >= new_training_freq - 10.0 and input_freq <= new_training_freq + 10.0 : 
                        lower_octave = "yes"
                        calc_octave = self.CalculateOctave(note, (-1 * multiplier))
                        minimum = [note, input_freq, "lower", multiplier, calc_octave, acc_note]
                        break; 

            if lower_octave == "yes": 
                break; 

            else: 
                for multiplier in range(1,8): 
                    new_training_freq = training_freq * (2 * multiplier)
                    if input_freq >= new_training_freq - 10.0 and input_freq <= new_training_freq + 10.0: 
                        higher_octave == "yes"
                        calc_octave = self.CalculateOctave(note, multiplier)
                        minimum = [note, input_freq, "higher", multiplier, calc_octave, acc_note]

        return minimum

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

        #numNotes = len(peakutils.indexes(fft_track, thres=0.02/max(fft_track), min_dist=rate/2))
        numNotes = 9
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
                if self.note_values[note[0]] > self.note_values[detected_notes[i - 1][0][0]]: 
                    parson_code += 'U'
                elif self.note_values[note[0]] < self.note_values[detected_notes[i - 1][0][0]]: 
                    parson_code += 'D'
                else: 
                    parson_code += 'R'

            start = start + duration
            duration = interval
        
        return (detected_notes, parson_code)
        
    def searchContours(self, parson_code):
        coll = "Musipedia"
        query = parson_code
        keywords = ""
        pitch = 0.6
        rhythm = 0.4
        items = 5
        offset = 0
        cats = ""
        wsdl = 'https://www.musipedia.org/soap/index.php?wsdl'
        client1 = zeep.Client(wsdl=wsdl)
        with open('config.json', 'r') as config:
            data = json.load(config)
            output = client1.service.search(data["username"], data["password"],
                                            coll, query, keywords, pitch, rhythm, items, offset, cats)

            print(output["items"][0])
            self.playMIDI(output["items"][0]["url"])
            return output["items"]

    def play_music(self, music_file):
        """
        stream music with mixer.music module in blocking manner
        this will stream the sound from disk while playing

        Referenced: https://www.daniweb.com/programming/software-development/code/216976/play-a-midi-music-file-using-pygame
        """
        clock = pygame.time.Clock()
        try:
            pygame.mixer.music.load(music_file)
            print("Music file %s loaded!" % music_file)
        except pygame.error:
            print("File %s not found! (%s)" % (music_file, pygame.get_error()))
            return
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            # check if playback has finished
            clock.tick(15)

    def playMIDI(self, url):
        """ Given a MIDI link, will download and play """
        midi = None
        url = "http://www.musipedia.org/edit.html?&L=0&no_cache=1&tx_detedit_pi1%5Bmode%5D=d&tx_detedit_pi1%5Btid%5D=037a595e6f4f0576a9efe43154d71c18"
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        links = set()
        data = urlopen(req).read()
        soup = BeautifulSoup(data,
                             "html.parser", from_encoding="iso-8859-1")
        links.update(soup.findAll("a", href=True))
        for item in links:
            try:
                test = str(item)
                if "mid" in test:
                    midi = "http://www.musipedia.org" + item.get("href")
            except:
                continue
        
        if midi:
            file_name = "playfi.mid"
            req = Request(midi, headers={'User-Agent': 'Mozilla/5.0'})
            rsp = urlopen(req)
            with open(file_name,'wb') as f:
                f.write(rsp.read())
            
            freq = 44100    # audio CD quality
            bitsize = -16   # unsigned 16 bit
            channels = 2    # 1 is mono, 2 is stereo
            buffer = 1024    # number of samples
            pygame.mixer.init(freq, bitsize, channels, buffer)
            # optional volume 0 to 1.0
            pygame.mixer.music.set_volume(0.8)
            self.play_music(file_name)
                        