#!/usr/bin/python3

import os
from musicnotes import MusicNote


def main():
    tester = MusicNote()
    for fi in os.listdir("note_data/"):
        tester.GetNote("note_data/" + fi)


if __name__ == "__main__":
    main()
