#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: (insert names here)
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image, ImageDraw, ImageFont
import sys
import random
import math
import copy
import re
import numpy as np
from collections import defaultdict

CHARACTER_WIDTH=14
CHARACTER_HEIGHT=25


def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    #print(im.size)
    #print(int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH)
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        result += [ [ "".join([ '*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg+CHARACTER_WIDTH) ]) for y in range(0, CHARACTER_HEIGHT) ], ]
    return result

def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }


def preprocess_text(file):

    # Given a text file with input of the form "WORD POS_TAG WORD POS_TAG ...." remove the POS tags 
    # and unnecessary special characters to generate cleaner text
    
    cleaned_text = []
    text_file = open(file,'r')

    for text in text_file:

        new_string = re.sub(' ADJ | ADV | ADP | CONJ | DET | NOUN | NUM | PRON | PRT | VERB | X |\n', ' ', text)
        new_string = re.sub(' \'\' . ', '\" ', new_string)
        new_string = re.sub(r' \`\` . ', ' \"', new_string)
        new_string = re.sub(r'\`\` . ', '\"', new_string)
        new_string = re.sub(' , . ', ', ', new_string)
        new_string = re.sub(r' \? . ', '? ', new_string)
        new_string = re.sub(r' \! . ', '! ', new_string)
        new_string = re.sub(' . . ', '. ', new_string)
        new_string = re.sub('    ', '', new_string)
        
        cleaned_text.append(new_string)

    return cleaned_text


def find_prob_dist(text):

    # Holds the initial probability distributions
    q0_dist = defaultdict(lambda: 0)
    trans_prob_dist = {}

    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    

    # In q0_dist key is the letter 'l', value is the number of times a sentence begins with the letter 'l'
    for sent in text:
        start_letter = sent[0]
        q0_dist[start_letter] += 1

    for l in TRAIN_LETTERS:
        
        if l in q0_dist.keys():
            pass

        else:
            q0_dist[l] = 1

    # Removes all unecessary keys from the initial distribution because 
    # it is assumed that the documents only have the 26 uppercase latin characters, 
    # the 26 lowercase characters, the 10 digits, spaces, and 7 punctuation symbols, (),.-!?'".
    q0_dist = {key:val for key, val in q0_dist.items() if key in TRAIN_LETTERS}

    # Normalizing the counts in the q0_dist to get the intial probability distribution
    total = sum(q0_dist.values())
    for key in q0_dist.keys():
        q0_dist[key] = q0_dist[key] / total
    
    # Compute the transition probabilities
    # Following code creates a nested dictionary of the form:
    '''
    {
        'A' : {'t': 543, 'l': 881, 's': 755, 'u': 227, 'j': 117, ' ': 1106, 'f': 1318, 'g': 137, 'n': 1413, '.': 222, 'i': 88, 'p': 179, 'r': 572, 'D': 11, 'm': 1010, 'c': 288, 'T': 33, 'd': 337, 'b': 130, 'v': 84, 'P': 14, "'": 10, 'w': 13, 'h': 13, 'S': 17, '1': 1, 'R': 6, 'H': 7, 'F': 6, 'M': 26, 'a': 5, 'q': 3, 'I': 28, 'e': 28, '-': 4, ',': 17, 'B': 10, 'E': 18, 'O': 2, '5': 1, 'N': 2, 'z': 4, 'y': 4, 'C': 15, '"': 12, 'A': 12, 'x': 5, 'L': 2, '/': 1, 'W': 5, 'V': 1, 'k': 1, 'K': 1, 'o': 1}

        'B' : ..............
        'C' : ..............
        ........
    

    }
    Each key in the dictionary is the letter l whose value is dictionary with the counts of each letter k that will follow the letter l


    master dict 
    72,72 matrix TP


    '''
    for sent in text:

        for i in range(len(sent)-1):

            if sent[i] in trans_prob_dist.keys():

                if sent[i+1] in trans_prob_dist[sent[i]].keys():
                        trans_prob_dist[sent[i]][sent[i+1]] += 1
                else:
                    trans_prob_dist[sent[i]][sent[i+1]] = 1
            
            else:
                trans_prob_dist[sent[i]] = {sent[i+1]: 1}

    # If there is a letter k that is less likely to follow a letter l then a small probability is assigned to it.
    for value in trans_prob_dist.values():
        for letter in TRAIN_LETTERS:
            if letter in value.keys():
                pass
            else:
                value[letter] = 1

    # Normalizing the counts in the trans_prob_dist to get the transition probability distribution
    # Probability of all letters followed by a letter '1' should add to one
    # The normalization step is performed only on the key value pairs of a given letter 'l'
    for value in trans_prob_dist.values():
        total = sum(value.values())
        for key in value.keys():
            value[key] = value[key] / total

    return q0_dist, trans_prob_dist


def find_emission_probability(noisy_img, noise_free_img,m):
    # Emission probability is computed using the following logic: 
    # If we assume that m% of the pixels are noisy, then a naive Bayes classifier could
    # assume that each pixel of a given noisy image of a letter will match the corresponding pixel in the reference
    # letter with probability (100 - m)%.
    count = np.sum([1 if noisy_img[r][c] == noise_free_img[r][c] else 0 for c in range(len(noisy_img[0])) for r in range(len(noisy_img))])
    p_value = len(noisy_img)*len(noisy_img[0]) * np.log(m/100) + count * np.log(100-m/100)
    return p_value


def naive_bayes_classifier(noisy_img, train_letters, m):
    # Naive bayes classifier:
    # Each letter in the noisy image is compared with every actual letter image and the emission probability is computed
    # The letter whose probability is the largest among the ones computed previously determines the letter that will appear in the final text sequence

    seq = ""
    
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    for i in range(len(noisy_img)):
        
        max_let = ''
        max_prob = float('-inf')
        
        for let in TRAIN_LETTERS:
            temp_prob = find_emission_probability(noisy_img[i], train_letters[let],m)
            if temp_prob > max_prob:
                max_prob = temp_prob
                max_let = let

        seq = seq + max_let

    return seq


def HMM(noisy_img, train_letters,q0_dist, trans_prob_dist,m):
    # HMM:
    '''
    Performed as follows:
    1. Compute the initial probabilities for all hidden states(actual letters) for the first observed letter(noisy image letter)
    2. Recursively find the most probable sequence of hidden states by doing the following:
        a. Find the probabilities of the probable paths from state q(t-1) to q(t) --> vi(t-1)
        b. Compute max(1<=i<=N) vi(t-1) *  TP[i,j]
        c. vi(t) = emission_prob[j,t] * max(1<=i<=N) vi(t-1) *  TP[i,j]
    3. To find most probable sequence of letters, trace back is performed iteratively as follows:
        - start from state t, find the hidden state corresponding to the highest probability, then state t-1 and so on until t=0
        - add all the hidden states to form a sequence of letter.

    In this implementation the log probabilties are considered, ie. log(a*b) = log(a)+log(b)
    '''
    
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "

    p_values = np.zeros((len(TRAIN_LETTERS), len(noisy_img)))
    for obs in range(len(noisy_img)):
        for q in range(len(TRAIN_LETTERS)):
            emis_prob = find_emission_probability(noisy_img[obs], train_letters[TRAIN_LETTERS[q]], m)
            if obs == 0:
                p_values[q][obs] = emis_prob + np.log(q0_dist[TRAIN_LETTERS[q]]) + 0.1
            else:
                prev_list = np.array([p_values[a][obs - 1] for a in range(len(TRAIN_LETTERS))])
                max_ele = np.zeros(len(TRAIN_LETTERS))
                for p in range(len(prev_list)):
                    max_ele[p] = prev_list[p] + np.log(trans_prob_dist[TRAIN_LETTERS[p]][TRAIN_LETTERS[q]]) + 0.1


                
                p_values[q][obs] = np.max(max_ele) + emis_prob + 0.1


    seq = ""
    for i in range(p_values.shape[1]-1,-1,-1):
        l_index = np.argmax(p_values[:,i])
        seq = seq + TRAIN_LETTERS[l_index]

    return seq[::-1]


#####
# main program
if len(sys.argv) != 4:
    raise Exception("Usage: python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png")

train_img_fname, train_txt_fname, test_img_fname = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)

train_data = preprocess_text(train_txt_fname)
q0_dist, trans_prob_dist = find_prob_dist(train_data)

# The final two lines of your new_string should look something like this:
print("Simple: " + naive_bayes_classifier(test_letters, train_letters, 30))
print("   HMM: " + ''.join(HMM(test_letters, train_letters,q0_dist,trans_prob_dist,30)) )