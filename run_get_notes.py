import numpy as np
import wave
import struct
from test_get_notes import play
if __name__ == "__main__":
    
    #code for checking output for single audio file
    #Reading audio file
    
    sound_file = wave.open('test_data/hbd.wav', 'r')
    
    #call play() to identify notes
    print("Notes in File 1 = ")
    play(sound_file)

    #code for checking output for remaining all audio files
    for file_number in range(2,6):
        file_name = "Audio_files/Audio_" + str(file_number) + ".wav"
        sound_file = wave.open(file_name)
        print("Notes in File " + str(file_number) + " = ")
        play(sound_file)
