#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 09:51:28 2018

@author: helmisatria
"""

import numpy
import io
from itertools import permutations

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

tag_count, word_tag, tag_trans = read_file_init_table('sample_postagged_2.txt')
# print(tag_count)
# print(word_tag)
# print(tag_trans)

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

def create_emission_prob_table(word_tag, tag_count):
    emission_prob = {}
    for word_tag_entry in word_tag.keys():
        word_tag_split = word_tag_entry.split(',')
        current_word = word_tag_split[0]
        current_tag = word_tag_split[1]
        emission_key = current_word+','+current_tag
        emission_prob[emission_key] = word_tag[word_tag_entry]/tag_count[current_tag]
    return emission_prob

emission_prob = create_emission_prob_table(word_tag, tag_count)
# print(emission_prob)

def viterbi(trans_prob, emission_prob, tag_count, sentence):
    #initialization
    viterbi_mat = {}
    tag_sequence = []

    sentence_words = sentence.split()
    
    current_tag = '<start>'
    max_score = 1
    for i, current_word in enumerate(sentence_words):
        viterbi_mat[current_word] = max_score
        scores = []
        
        if (i == len(sentence_words) - 1): break
        
        for j, trans in enumerate(emission_prob.keys()):
#             print(trans)
            print(current_tag)
            score = 0
            next_word = trans.split(',')[0]
            next_tag = trans.split(',')[1]
            
            if (next_word == sentence_words[i+1]):
                print(current_word, ' ', next_word, ' ', current_tag, ' ', next_tag)
                try:    
                    print('TP: ', trans_prob[current_tag + ',' + next_tag])
                    score = max_score * emission_prob[trans] * trans_prob[current_tag + ',' + next_tag]
                except:
                    print('TP: ', 0)
                    score = max_score * emission_prob[trans] * 0
            scores.append({ 'score': score, 'current_tag': current_tag, 'tag': next_tag })
        
        onlyScores = [x['score'] for x in scores]
        print(onlyScores)
        max_index = onlyScores.index(max(onlyScores))
        
        max_score = max(onlyScores)
        current_tag = scores[max_index]['tag']
        tag_sequence.append(current_tag)
    
    return viterbi_mat, tag_sequence

sentence = "<start> dia ingin makan ikan kemaren"
result_viterbi = viterbi(trans_prob, emission_prob, tag_count, sentence)
print(result_viterbi)