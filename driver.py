#!/usr/bin/python3

import os
from musicnotes import MusicNote


def main():
    tester = MusicNote()
    """
    for fi in os.listdir("note_data/"):
        note = tester.GetNote("note_data/" + fi)
        print(note)
    """

    print("Playing 'b' note")
    note = tester.GetNote2("test_data/b1.wav")
    print(note)
    print("Playing 'g' note")
    note = tester.GetNote2("test_data/g1.wav")
    print(note)
    print("Playing 'f' note")
    note = tester.GetNote2("test_data/f1.wav")
    print(note)
    
    print("Playing 'a' note")
    note = tester.GetNote2("test_data/a1.wav")
    print(note)

if __name__ == "__main__":
    main()
