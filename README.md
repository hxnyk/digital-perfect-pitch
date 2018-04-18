# digital-perfect-pitch
EECS 486 final project

musicnotes.py: Contains our MusicNotes class and essentially all functions we use to detect single notes, multiple notes, as well as the parsons code. 
It also has the code that interacts with the musipedia SOAP API that takes the calculated parsons code in as input

driver.py: Performs all of our 'experiments' associated with the functions in musicnotes.py :)

training_notes/: Folder of 8 notes in 3rd octaves used as training data

single_note_tests/: Files of single notes that we test our single note detection functionality with

working_songs/: Songs we found are detected by our system, we use to perform more in depth tests on our system

thinkdsp.py: This file contains code used in "Think DSP", by Allen B. Downey, available from greenteapress.com; Copyright 2013 Allen B. Downey; License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
