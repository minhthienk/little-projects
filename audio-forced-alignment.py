import os
import sys
import re
import time
from slugify import slugify
from pydub import AudioSegment
import shutil

def get_aligned_words(mp3_path, text_path):
    # convert mp3 to wav
    output = "aligner/temp_wav_file.wav"
    cmd = 'ffmpeg ' \
        + '-y -i "{}" -vn -ar 44100 -ac 1 -b:a 16k "{}"'.format(mp3_path, output)
    os.system(cmd)

    # create transcript file
    with open(text_path, 'r') as text_file:
        transcript = text_file.read()

    transcript = re.sub(r'\s+',' ',transcript)
    with open("aligner/temp_wav_file.txt", 'w') as file:
        file.write(transcript)

    try:
        shutil.rmtree("/home/minhthienk/Documents/MFA/extracted_models/")
    except Exception as e:
        print(e)
        pass

    try:
        shutil.rmtree('/home/minhthienk/Documents/MFA/aligner_pretrained_aligner/')
    except Exception as e:
        print(e)
        pass



    corpus_directory = 'aligner'
    dictionary = '/home/minhthienk/Documents/MFA/pretrained_models/dictionary/english_us_arpa.dict'
    acoustic_model = '/home/minhthienk/Documents/MFA/pretrained_models/acoustic/english_us_arpa.zip'
    output_directory = 'aligner/output'

    cmd = 'mfa align {} {} {} {}'.format(
        corpus_directory,
        dictionary,
        acoustic_model,
        output_directory)


    # run aligner
    os.system(cmd)

    # get output TextGrid
    with open('aligner/output/temp_wav_file.TextGrid', 'r') as file:
        textgrid = file.read()
    
    # textgrid to list
    textgrid = re.sub('\t','',textgrid)
    textgrid = re.findall('name = "words".+name = "phones"',textgrid, flags=re.DOTALL)[0]
    intervals = re.findall(r'intervals \[.*?\].*?text = ".*?"', textgrid, flags=re.DOTALL)

    # convert textgrid to time frame
    time_mark = 0
    timings = []
    words = transcript.split()
    word_count = 0
    for interval in intervals: 
        text = re.findall('".*"', interval)[0].replace('"','')
        xmin = re.findall('xmin = .*', interval)[0].replace('xmin = ','')
        xmax = re.findall('xmax = .*', interval)[0].replace('xmax = ','')
        timings.append((text, xmin, xmax))

    return timings




def get_aligned_sentences(aligned_words, txt_file):
    # read the txt file and convert to a list of strings
    with open(txt_file, 'r') as file_object:
        txt = file_object.read()
        txt = re.sub(r'\t',' ',txt)
        txt = re.sub(r' +',' ',txt)
        txt = re.sub(r' *\n *','\n',txt)
        txt = re.sub(r'\n+','\n',txt) # remove double linefeed
        txt = re.sub(r'^\n','',txt) # remove linefeed at the beginning
        txt = re.sub(r'\n$','',txt) # replace redundant spaces
        txt = re.sub(r' +',' ',txt) # remove linefeed at the end
        print(txt)
        txt_lines = txt.split('\n')


    count_from = 0
    sentence_start = None
    sentence_end = None
    aligned_sentences = []

    for line in txt_lines:
        line = line.strip()
        word_num = line.count(' ') + 1
        aligned_word_count = 0
        start_flag = True
        for i in range(count_from, len(aligned_words)):
            #print(i, '/', len(aligned_words))
            word = aligned_words[i][0]
            xmin = aligned_words[i][1]
            xmax = aligned_words[i][2]
            if  word!='':
                aligned_word_count += 1
                if start_flag==True:
                    sentence_start = xmin
                    start_flag=False
            
            if aligned_word_count==word_num:
                sentence_end = xmax
                count_from = i+1
                break
        
        aligned_sentences.append((line, sentence_start, sentence_end))
    return aligned_sentences


def convert_time_for_cutter(time_in_seconds):
    time_in_seconds = float(time_in_seconds)
    if time_in_seconds<0: time_in_seconds=0
    h = int(time_in_seconds/3600)
    m = int((time_in_seconds - h*3600)/60)
    s = time_in_seconds - h*3600 - m*60
    return "{:02d}:{:02d}:{:05.2f}".format(h,m,s)


def cut_audio(audio_file, start, end, output):
    start = convert_time_for_cutter(float(start)-0.3)
    end = convert_time_for_cutter(float(end)+0.3)
    cmd = 'ffmpeg ' \
        + '-y -i "{}" -ss {} -to {} -c copy {}'.format(audio_file, start, end, output)
    print('>>>>>>>>>>>>>>>>>', cmd)
    os.system(cmd)





def match_target_amplitude(mp3_path):
    print('>>>>>>>>>>', mp3_path)
    target_dBFS = -15
    sound = AudioSegment.from_mp3(mp3_path)
    print(sound.dBFS)
    change_in_dBFS = target_dBFS - sound.dBFS
    sound = sound.apply_gain(change_in_dBFS)
    print(sound.dBFS)
    sound.export(mp3_path, "mp3")


def add_silent(audio_file, output_silent):
    audio_file = audio_file.replace('"','')
    output_silent= output_silent.replace('"','')
    cmd = 'ffmpeg -y -i "concat:silent2s.mp3|{}|silent2s.mp3" -acodec copy "{}"'.format(audio_file, output_silent)
    print(cmd)
    os.system(cmd)


def align_cutter(mp3_file, txt_file, silent=False):
    if not os.path.exists('cutter-output'):
        os.makedirs('cutter-output')

    basename = os.path.basename(os.path.splitext(mp3_file)[0])

    if not os.path.exists('cutter-output/' + basename):
        os.makedirs('cutter-output/' + basename)

    if not os.path.exists('cutter-output/' + basename + '_silent_added'):
        os.makedirs('cutter-output/' + basename + '_silent_added')


    des_dir = 'cutter-output/' + basename + '/'
    des_dir_silent = 'cutter-output/' + basename + '_silent_added/'

    aligned_words = get_aligned_words(mp3_file, txt_file)
    print(aligned_words)
    aligned_sentences = get_aligned_sentences(aligned_words, txt_file)
    print(aligned_sentences)
    for sentence in aligned_sentences:
        output = '"' + des_dir + slugify(sentence[0]).replace('-',' ') + '.mp3' + '"'
        output_silent = '"' + des_dir_silent + slugify(sentence[0]).replace('-',' ') + '.mp3' + '"'
        print('\n>>>>>>>>>>>>>>>>>', sentence)
        cut_audio(mp3_file, sentence[1], sentence[2], output)
        if silent:
            print('>>>>> add silent')
            add_silent(output, output_silent)
        #match_target_amplitude(output.replace('"',''))



def cmd_cutter():
    print('Instruction:')
    print('- Input mp3 file path')
    print('- Input text file path')
    print('- Wait and see')
    print('\n')
    try:
        audio_fpath = input('audio_fpath: ')
        txt_fpath = input('txt_fpath: ')
        silent = input('add silent: y/n?: ')
        if silent=='y':
            silent=True
        else:
            silent=False
        #audio_fpath = 'test.mp3'
        #txt_fpath = 'test.txt'
        # remove " from path
        audio_fpath = audio_fpath.strip().replace('"','')
        txt_fpath = txt_fpath.strip().replace('"','')

        align_cutter(audio_fpath, txt_fpath,silent)

        print('\n\n')
    except Exception as e:
        print(e)
        #raise(e)
        input('wait .............................')
        #sys.exit()

#

print('remember to activate: "conda activate aligner"')
input('are you ready?')
cmd_cutter()
#align_cutter('nysa.mp3', 'text.txt', silent='y')
'''
mp3_file = 'nha.mp3'
txt_file = 'text.txt'
align_cutter(mp3_file, txt_file, True)
'''