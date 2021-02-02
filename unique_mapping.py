'''
Finding and extracting one-to-one mapping tokens
Replacing them in source side and keeping the remaining tokens as they are
Script takes three files:
    1. Source
    2. Target
    3. Alignment

Source counting is from 0 and target is from 0
Date: 17 December 2020

How to run: python3 unique_mapping.py source_file target_file
source_to_target_alignment_file
'''

# imports
import time
import argparse
import spacy
from spacy.lang.hi import STOP_WORDS as hindi_stop_words

# spacy en
en = spacy.load('en_core_web_sm')

# spacy de
de = spacy.load('de_core_news_sm')

# spacy fr
fr = spacy.load('fr_core_news_sm')

# english alphabet
# alphabet = "abcdefghijklmnopqrstuvwxyz"

# arg parser
parser = argparse.ArgumentParser(
    description="Unique mapping extraction from alignment information")
parser.add_argument(dest='src_file', type=argparse.FileType('r'))
parser.add_argument(dest='trg_file', type=argparse.FileType('r'))
parser.add_argument(dest='alignment_file', type=argparse.FileType('r'))

args = parser.parse_args()


# func: data reading
# args: input file
# return: list containing data
# no need to manually open since we are passing it as open file argument from argparser
def read_data(in_file):
    data = list()
    for l in in_file:
        data.append(l.rstrip('\n'))

    return data

# func: get unique mapping
# args: single line of alignment data
# return: dictionary where keys are left side uniquely mapped tokens and values are the corresponding right side tokens
# this code will run for each line in alignment data
def unique_mapping(align_data):
    item = align_data.split(' ')  # we get tokenwise alignments
    left_count_dict = dict()
    right_count_dict = dict()
    left_return_dict = dict()
    right_return_dict = dict()
    return_dict = dict()

    for i in item:
        left = int(i.split('-')[0])   # left token position
        right = int(i.split('-')[1])  # right token position

        if left in left_count_dict.keys():
            left_count_dict[left] += 1
        else:
            left_count_dict[left] = 1

        if right in right_count_dict.keys():
            right_count_dict[right] += 1
        else:
            right_count_dict[right] = 1

    # we got the counts of left tokens
    # we skip tokens whose count is > 1
    for d in left_count_dict.items():
        if d[1] <= 1:   # d[1]: value
            left_return_dict[d[0]] = 1   # d[0]: key

    for d in right_count_dict.items():
        if d[1] <= 1:   # d[1]: value
            right_return_dict[d[0]] = 1   # d[0]: key

    # print(left_count_dict)
    # print(right_count_dict)
    # print(left_return_dict)
    # print(right_return_dict)

    # we got the unique mappings
    # we have to fill the return_dict with unique source - target mappings
    for i in item:
        left = int(i.split('-')[0])   # left token position
        right = int(i.split('-')[1])  # right token position

        # we have add the values to only tokens having unique mappings
        if left in left_return_dict.keys():
            if right in right_return_dict.keys():
                return_dict[left] = right

    # print(align_data)
    # print(return_dict)
    # return_dict = {v: k for k, v in return_dict.items()}
    return return_dict

# func: replace the left side/source side with right side/target side according to unique mapping we got from func: unique_mapping
# args: left side data, right side data, alignment data
# return: replaced data i.e. right in left (eg: hindi in english)
def replace_data(left_data, right_data, align_data):
    return_list = list()
    for item in zip(left_data, right_data, align_data):
        src = item[0].split()
        trg = item[1].split()
        unique_mapping_dict = unique_mapping(item[2])
        # print(unique_mapping_dict)

        # since left align information starts with 0: NULL, and actual indexing starts from 0: first token, we have to decrement every key from unique_mapping_dict
        # replacing the src with trg tokens where it is unique mapping
        temp_list = list()
        '''
        print(src)
        print(trg)
        print(unique_mapping_dict)
        print(len(src), len(trg))
        '''
        src_fname = str(args.src_file.name)
        # trg_fname = str(args.trg_file.name)
        for tok in src:
            tok_index = src.index(tok)
            # print(tok[0], tok[-1])
            # print(args.src_file.name)
            if src_fname.split('.')[-1] == 'en':  # check if src is English or not
                # replacing the word if it has unique mapping and if it is not a stop word
                if tok_index in unique_mapping_dict.keys() and (en.vocab[tok].is_stop == False): #or tok not in hindi_stop_words):
                    # print(unique_mapping_dict[tok_index])
                    temp_list.append(trg[unique_mapping_dict[tok_index]]) # getting the target token at the position
                else:
                    temp_list.append(tok)

            elif src_fname.split('.')[-1] == 'hi':
                if tok_index in unique_mapping_dict.keys() and (tok not in hindi_stop_words):
                    temp_list.append(trg[unique_mapping_dict[tok_index]])
                else:
                    temp_list.append(tok)

            elif src_fname.split('.')[-1] == 'de':
                if tok_index in unique_mapping_dict.keys() and (de.vocab[tok].is_stop == False):
                    temp_list.append(trg[unique_mapping_dict[tok_index]])
                else:
                    temp_list.append(tok)

            elif src_fname.split('.')[-1] == 'fr':
                if tok_index in unique_mapping_dict.keys() and (fr.vocab[tok].is_stop == False):
                    temp_list.append(trg[unique_mapping_dict[tok_index]])
                else:
                    temp_list.append(tok)

        # print(' '.join(str(i) for i in temp_list))
        return_list.append(' '.join(str(i) for i in temp_list))

    return return_list


# func: main
if __name__ == "__main__":
    start_time = time.time()
    left_data = read_data(args.src_file)  # src data
    right_data = read_data(args.trg_file)  # trg data
    align_data = read_data(args.alignment_file)  # alignment data

    # print(len(left_data), len(right_data), len(align_data))
    # unique_mapping(align_data[0])
    cm_data = replace_data(left_data, right_data, align_data)
    # print(f'{left_data[0]}\n{right_data[0]}\n{align_data[0]}\n{cm_data[0]}')

    out_file_name = './generated_cm_data.txt'
    out_file = open(out_file_name, 'w', encoding='utf-8')
    for s in cm_data:
        out_file.write('%s\n' %s)

    out_file.close()
    end_time = time.time()
    run_time = end_time - start_time
    print(f'Generated code-mixed data saved in: {out_file_name}')
    print(f'Time took: {run_time:.2f}s')
