#!/usr/bin/python3

import os
from musicnotes import MusicNote

def print_output(note): 
    octave_word = ""
    if note[3] > 1 or note[3] == 0: 
        octave_word = "octaves"
    else: 
        octave_word = "octave"    
    print("Note is: ", note[0], "\nFrequency is: ", str(note[1]), "\nThis octave is", note[3], octave_word, note[2], "than training data")
def main():
    tester = MusicNote()
    """
    for fi in os.listdir("note_data/"):
        note = tester.GetNote("note_data/" + fi)
        print(note)
    
    print("Playing 'b' note")
    note = tester.GetNote("test_data/b1.wav")
    print_output(note)

    print("Playing 'g' note")
    note = tester.GetNote("test_data/g1.wav")
    print_output(note)

    print("Playing 'f' note")
    note = tester.GetNote("test_data/f1.wav")
    print_output(note)

    print("Playing 'a' note")
    note = tester.GetNote("test_data/a1.wav")
    print_output(note)
    
    print("Playing 'c' note")
    note = tester.GetNote("test_data/c1.wav")
    print_output(note)    

    print("Playing 'd' note")
    note = tester.GetNote("test_data/d1.wav")
    print_output(note)   
    """
     

if __name__ == "__main__":
    main()
