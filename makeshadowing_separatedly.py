
import sys
import os



import re
import time

from pydub import AudioSegment

def match_target_amplitude(mp3_path):
    print('>>>>>>>>>>', mp3_path)
    target_dBFS = -15
    sound = AudioSegment.from_mp3(mp3_path)
    print(sound.dBFS)
    change_in_dBFS = target_dBFS - sound.dBFS
    sound = sound.apply_gain(change_in_dBFS)
    print(sound.dBFS)
    sound.export(mp3_path, "mp3")



def audio_joiner(file_list):
    input_files = file_list
    combined = None
    beep = AudioSegment.from_file("beep.mp3", format="mp3")
    for file in input_files:
        print(file)
        input_file = 'vegan/' + file
        match_target_amplitude(input_file)
        sound = AudioSegment.from_file(input_file, format="mp3")
        audio_length = len(sound)
        silence = AudioSegment.silent(duration=audio_length + 1000)
        if combined==None:
            combined = sound + AudioSegment.silent(200) + beep + silence
        else:
            combined += sound + AudioSegment.silent(200) + beep + silence

    # simple export
    output_file = 'output_audio_Sarah.mp3'
    file_handle = combined.export(output_file, format="mp3")
    print('>>>>>>>>>> completed: ', output_file)


def add_beep(file_name, input_folder, output_folder):
    input_file =  input_folder + '/' + file_name
    beep = AudioSegment.from_file("beep.mp3", format="mp3")
    match_target_amplitude(input_file)
    sound = AudioSegment.from_file(input_file, format="mp3")
    audio_length = len(sound)

    silence_pre = AudioSegment.silent(500)
    silence_post = AudioSegment.silent(duration=audio_length + 2000)

    combined = silence_pre + sound + AudioSegment.silent(200) + beep + silence_post
    output_file = output_folder + '/' + file_name
    file_handle = combined.export(output_file, format="mp3")
    print('>>>>>>>>>> completed: ', output_file)

def file_key(file_name):
    # use a regular expression to extract the numerical part of the file name
    match = re.search(r'\((\d+)\)', file_name)
    if match:
        num_part = int(match.group(1))
        return num_part
    else:
        # if the file name doesn't match the expected pattern, just return the file name itself
        return file_name




'''
directory_path = "vegan"  # replace with your directory path
files = os.listdir(directory_path)
sorted_files = sorted(files, key=file_key)
audio_joiner(sorted_files)
'''

directory_path = 'vegan'
files = os.listdir(directory_path)
sorted_files = sorted(files, key=file_key)

for file in sorted_files:
    if '.mp3' in file:
        add_beep(file, 'vegan', 'vegan2')










