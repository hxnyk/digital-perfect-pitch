#!/usr/bin/python3

import os
from musicnotes import MusicNote

def print_output(note): 
    octave_word = ""
    if note[3] > 1 or note[3] == 0: 
        octave_word = "octaves"
    else: 
        octave_word = "octave"    
    print("Calculated note is: ", note[0] + str(note[4]), "\nFrequency is: ", str(note[1]), "\nThis octave is", note[3], octave_word, note[2], "than training data")
    print("Accurate note is: ", note[5], "\n")

def accum_accuracy(is_accurate, accuracy_count):
    if is_accurate == "yes": 
        accuracy_count += 1
    return accuracy_count

def main():
    tester = MusicNote()
    
    
    print("Playing twinkletwinkle: ")
    note = tester.getMultipleNotes("melodies/twinkletwinkle.wav")
    print(note[0])
    print(note[1])
    
    contour = note[1]
    tester.searchContours(contour)

    '''
    print("Playing 2 notes, [C1, A1]")
    note = tester.getMultipleNotes("test_data/c1_a1.wav")
    print (getDuration("test_data/c1_a1.wav"))
    print(note)
   
    for fi in os.listdir("note_data/"):
        note = tester.GetNote("note_data/" + fi)
        print(note)
      
    accuracy_count = 0
    print("Playing 'b' note")
    note = tester.GetNote("test_data/b1.wav")
    print_output(note)
    accuracy_count = accum_accuracy(tester.IsAccurate(note), accuracy_count)

    print("Playing 'g' note")
    note = tester.GetNote("test_data/g1.wav")
    print_output(note)
    accuracy_count = accum_accuracy(tester.IsAccurate(note), accuracy_count)
    
    print("Playing 'f' note")
    note = tester.GetNote("test_data/f1.wav")
    print_output(note)
    accuracy_count = accum_accuracy(tester.IsAccurate(note), accuracy_count)
    
    print("Playing 'a' note")
    note = tester.GetNote("test_data/a1.wav")
    print_output(note)
    accuracy_count = accum_accuracy(tester.IsAccurate(note), accuracy_count)

    print (accuracy_count)
    '''
    

if __name__ == "__main__":
    main()
