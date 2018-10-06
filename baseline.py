#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 11:21:16 2018

@author: helmisatria
"""

import numpy as np

def read_file_init_table(fname):
    tag_count = {}
    tag_count['<start>'] = 0
    word_tag = {}
    tag_trans = {}
    with open(fname) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    idx_line = 0
    is_first_word = 0
    
    while idx_line < len(content):
        prev_tag = '<start>'
        while not content[idx_line].startswith('</kalimat'):
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                if content_part[1] in tag_count:
                    tag_count[content_part[1]] += 1
                else:
                    tag_count[content_part[1]] = 1
                    
                current_word_tag = content_part[0]+','+content_part[1]
                if current_word_tag in word_tag:
                    word_tag[current_word_tag] += 1
                else:    
                    word_tag[current_word_tag] = 1
                    
                if is_first_word == 1:
                    current_tag_trans = '<start>,'+content_part[1]
                    is_first_word = 0
                else:
                    current_tag_trans = prev_tag+','+content_part[1]
                    
                if current_tag_trans in tag_trans:
                    tag_trans[current_tag_trans] += 1
                else:
                    tag_trans[current_tag_trans] = 1                    
                prev_tag = content_part[1]   
                
            else:
                tag_count['<start>'] += 1
                is_first_word = 1
            idx_line = idx_line + 1

        idx_line = idx_line+1
    return tag_count, word_tag, tag_trans

tag_count, word_tag, tag_trans = read_file_init_table('data_train.txt')

# Membaca test file
def read_test_file(filename):
    
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    
    Sentences = []
    
    idx_line = 0
    kalimat = []
    while idx_line < len(content):
        while not content[idx_line].startswith('</kalimat'):
            if  content[idx_line].startswith('<kalimat'):
                kalimat = []
            if  not content[idx_line].startswith('<kalimat'):
                content_part = content[idx_line].split('\t')
                kalimat.append(content_part)
            idx_line = idx_line + 1
        Sentences.append(kalimat)
            
        idx_line = idx_line+1
    
    return Sentences

# Metoda baseline
def baseline(word_tag, sentence):
    s = [x[0] for x in sentence]
    expected_tag = [x[1] for x in sentence]
    tag_sequence = []
    
    for i, word in enumerate(s):
        scores = []
    
        for j, key in enumerate(word_tag.keys()):
            k = key.split(',')[0].lower()
            tag = key.split(',')[1]
            
            if (word == k):
                scores.append({ 'k': k, 'tag': tag, 'score': word_tag[key] })
        
        onlyScores = [x['score'] for x in scores]
        
        try:
            max_index = onlyScores.index(max(onlyScores))
            best_tag = scores[max_index]['tag']
            tag_sequence.append(best_tag)
        except:
            tag_sequence.append('NN')
        
    return tag_sequence, expected_tag

Test_Sentences = read_test_file('data_test.txt')

# Mengeksekusi metode baseline dari tiap kalimat di data test
Score = np.zeros(20)
Accuracy = 0
for i, sentence in enumerate(Test_Sentences):
    
    tagPredicted, tagExpected = baseline(word_tag, sentence)
    
    for j, tag in enumerate(tagPredicted):
        if (tag == tagExpected[j]):
            Score[i] += 1
    Score[i] /= len(sentence)

Accuracy = sum(Score)/20
print('Accuracy: ', Accuracy)