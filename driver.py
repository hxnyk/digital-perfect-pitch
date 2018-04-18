#!/usr/bin/python3
from __future__ import division

import os
from musicnotes import MusicNote
import math


def print_output(note): 
    octave_word = ""
    if note[3] > 1 or note[3] == 0: 
        octave_word = "octaves"
    else: 
        octave_word = "octave" 
    if note[1] == math.inf:
        print ("Note not found\n")
        return       
    print("Calculated note is: ", note[0][0] + str(note[4]), "\nFrequency is: ", str(note[1]))
    print("\nThis octave is", str(note[3]), octave_word, note[2], "than training data")
    print("\nAccurate note is: ", note[5], "\n")
    

def test_single_notes():
    music_note = MusicNote()
    accuracy = 0.0
    num_files = 0.0
    for i, filename in enumerate(os.listdir("single_note_tests/")):
        print("Name of file: ", str(filename[0] + filename[1]))
        detected_note = music_note.GetNote("single_note_tests/" + filename)
        print_output(detected_note)
        if detected_note[1] < math.inf:
            if (detected_note[0][0] + str(detected_note[4])) == str(filename[0] + filename[1]):
                accuracy += 1; 
        num_files += 1
    accuracy = accuracy / num_files
    print (accuracy)


def test_song_retrieval():
    #test which of our songs actually show up when gotten from web
    note = MusicNote()
    for i, filename in enumerate(os.listdir("melodies/")):
        print("Analyzing song ", filename[:-4])
        parsons_code = note.getMultipleNotes("melodies/" + filename)[1]
        #because names of songs vary so much, we had to analyze the songs by looking at the list of songs the API returns
        note.searchCountours(parsons_code)

def test_diff_lengths():
        #have to manually analyze results of search contours because titles of songs can vary from expectation
        #i.e for example Twinkle Twinkle comes up as nursery tune Ah vous dirai-je Maman Twinkle, twinkle little 
        note = MusicNote()
        var_one = 0
        var_two = 0
        var_three = 0

        for i, filename in enumerate(os.listdir("working_songs/")):
            parsons_code = note.getMultipleNotes("working_songs/" + filename)[1]
            note.searchCountours(parsons_code)
            if (filename == "jinglebells.wav" or filename == "oops_britney.wav"):
                var_one = 4
                var_two = 2
                var_three = 0
            if (filename == "lil-lamb.wav"):
                var_one = 6
                var_two = 4
                var_three = 2
            if (filename == "twinkletwinkle.wav"):
                var_one = 7
                var_two = 5
                var_three = 3   

            note.searchContours(parsons_code[:-var_one])
            note.searchContours(parsons_code[:-var_two])
            note.searchContours(parsons_code[:-var_three])

def main():
    
    test_single_notes()
    test_get_songs()
    test_diff_lengths()
    

if __name__ == "__main__":
    main()
