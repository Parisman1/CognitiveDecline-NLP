import os
import json
from decimal import Decimal
from datetime import datetime
from collections import namedtuple
import statistics


def main():
    files = os.listdir('output')
    print(files)
    results = []
    FileFeatures = namedtuple('FileFeatures', ['filename', 'speaker', 'num_words', 'avg_word_len'])
    for i, fname in enumerate(files):
        if i  == 0:  # debug
            with open('output/'+fname, 'r')as f:
                data = json.loads(f.read())
                speaker = which_speaker(data)
                transcript = []
                word_lens = []
                for word_dict in data:
                    if word_dict['speaker_tag'] == speaker:
                        transcript.append(word_dict['word'])
                        word_lens.append(time_to_num(word_dict['end_time']) - time_to_num(word_dict['start_time']))
                print(word_lens)
                results.append(FileFeatures(fname, speaker, len(word_lens), sum(word_lens)/len(word_lens)))
    print(results)


def which_speaker(data):
    speaker1_count = sum([1 for word_dict in data if word_dict['speaker_tag'] == 1])
    speaker2_count = sum([1 for word_dict in data if word_dict['speaker_tag'] == 2])
    print(f"{speaker1_count=}")
    print(f"{speaker2_count=}")
    return 1 if speaker1_count >= speaker2_count else 2


def time_to_num(time_str):
    times = time_str.split(':')
    print(times)
    out = float(times[1]) * 60 + float(time_str[2])
    print(out)
    return out


if __name__ == '__main__':
    main()
