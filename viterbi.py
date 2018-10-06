#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 09:51:28 2018

@author: helmisatria
"""

import numpy

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
                    
                current_word_tag = content_part[0].lower() + ',' + content_part[1]
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

# print(tag_count)
# print(word_tag)
# print(tag_trans)

# Membuat Transition Probability Matrix
def create_trans_prob_table(tag_trans, tag_count):
    # print(tag_trans)
    trans_prob = {}
    for tag1 in tag_count.keys():
        for tag2 in tag_count.keys():
            #print('tag1 = ')
            #print(tag1)
            trans_idx = tag1+','+tag2
            #print('trans_idx = ')
            #print(trans_idx)
            if trans_idx in tag_trans:
                #print(trans_idx)
                trans_prob[trans_idx] = tag_trans[trans_idx]/tag_count[tag1]
    return trans_prob

trans_prob = create_trans_prob_table(tag_trans, tag_count)
# print(trans_prob)

# Membuat Emission Probability Matrix
def create_emission_prob_table(word_tag, tag_count):
    emission_prob = {}
    for word_tag_entry in word_tag.keys():
        word_tag_split = word_tag_entry.split(',')
        # print('\n---')
        # print(word_tag_split)
        if (word_tag_split[0] == ','):
            current_word = ','
            current_tag = word_tag_split[-1]
        if (len(word_tag_split) > 2):
            current_word = ''.join(word_tag_split[:-1]).lower()
            current_tag = word_tag_split[-1]
        else:
            current_word = word_tag_split[0].lower()
            current_tag = word_tag_split[1]
        # print(current_word)
        # print(current_tag)
        emission_key = current_word+','+current_tag
        emission_prob[emission_key] = word_tag[word_tag_entry]/tag_count[current_tag]
    return emission_prob

emission_prob = create_emission_prob_table(word_tag, tag_count)
# print(emission_prob)

# Metode Viterbi
def viterbi(trans_prob, emission_prob, tag_count, sentence):
    #initialization
    viterbi_mat = {}
    tag_sequence = []
    
    # print(sentence)
    
    sentence_words = ['<start>'] + [x[0].lower() for x in sentence]
    expected_tag = [x[1] for x in sentence]
    
    current_tag = '<start>'
    max_score = 1
    for i, current_word in enumerate(sentence_words):
        viterbi_mat[current_word] = max_score
        scores = []
        
        if (i == len(sentence_words) - 1): break
        
        for j, trans in enumerate(emission_prob.keys()):
            # print(current_tag)
            score = 0
            next_word = trans.split(',')[0]
            next_tag = trans.split(',')[-1]
            
            if (next_word == sentence_words[i+1]):
                # print(current_word, ' ', next_word, ' ', current_tag, ' ', next_tag)
                try:    
                    # print('TP: ', trans_prob[current_tag + ',' + next_tag])
                    score = max_score * emission_prob[trans] * trans_prob[current_tag + ',' + next_tag]
                except:
                    score = max_score * emission_prob[trans] * 0
                    
            scores.append({ 'score': score, 'current_tag': current_tag, 'tag': next_tag })
        
        onlyScores = [x['score'] for x in scores]
        # print(onlyScores)
        max_index = onlyScores.index(max(onlyScores))
        
        max_score = max(onlyScores)
        current_tag = scores[max_index]['tag']
        tag_sequence.append(current_tag)
    
    return viterbi_mat, tag_sequence, expected_tag

# sentence = "<start> dia ingin makan ikan kemaren"
Test_Sentences = read_test_file('data_test.txt')


# Mengeksekusi metode viterbi dari tiap kalimat di data test
Scores = numpy.zeros(20)
Accuracy = 0

for i, sentence in enumerate(Test_Sentences):
    # print(i)
    viterbi_mat, tagPrediction, tagExpectation = viterbi(trans_prob, emission_prob, tag_count, sentence)
    
    for j, tag in enumerate(tagPrediction):
        if (tag == tagExpectation[j]):
            Scores[i] += 1
    Scores[i] /= len(sentence)
    
    # print(viterbi_mat)
    # print(tagPrediction)
    # print(tagExpectation)
    
Accuracy = sum(Scores) / 20 * 100
print('Accuracy: ', Accuracy)