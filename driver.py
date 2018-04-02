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
    note = tester.GetNote("test_data/b1.wav")
    print(note)

if __name__ == "__main__":
    main()
