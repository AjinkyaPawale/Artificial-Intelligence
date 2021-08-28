#!/usr/bin/env python
# coding: utf-8

# In[1]:


# classify.py : Classify text objects into two categories
#
# Shivani Vogiral, svogiral
#
# Based on skeleton code by D. Crandall, March 2021
# 

import sys

# Additional libraries

import pandas as pd
import numpy as np
import re
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
import time

def load_file(filename):
    objects=[]
    labels=[]
    with open(filename, "r") as f:
        for line in f:
            parsed = line.strip().split(' ',1)
            labels.append(parsed[0] if len(parsed)>0 else "")
            objects.append(parsed[1] if len(parsed)>1 else "")
    
    return {"objects": objects, "labels": labels, "classes": list(set(labels))}

def clean_data(data):

    '''
    Procedure:
    1. Lower case each tweet in the **training and test data**
    2. Obtain a list of unique tokens in each tweet using nltk's sent_tokenize and word_tokenize
    3. Ignore the tokens that are special characters and numbers.
    4. Remove stop words
    5. Join all the filtered tokens to form a string of the tweet where each filtered token is separated by a space

    The cleaned train tweets are added into a column called "Clean Text" into the train data dataframe and similarly the cleaned test tweets are added as a column to the test data dataframe.
    '''
    clean_text = []
    spcl= '[-,;@_!#$%^&*()<>?/\|}{~:''.+""]'
    for i in data["Tweet"]:
        filtered_tokens=[]
        
        i = i.lower()
        # tokens = [word for sent in sent_tokenize(i) for word in word_tokenize(i)]
        tokens = i.split(' ')
        for token in tokens:
            if token!='':
                token = re.sub(spcl,'',token)
                token = re.sub('[0-9]','',token)
                filtered_tokens.append(token)
        v = [word for word in filtered_tokens if word not in stop_words]
        temp = ' '.join(w for w in v)
        clean_text.append(temp)
    data['Clean Text'] = clean_text
    return data

def get_words_label_matrix(data):

    '''
    Procedure:
    1. Consider all the "Clean Text" tweets from the training data.
    2. Split the train data dataframe by label to create 2 dataframes for the labels "EastCoast" and "WestCoast"
    3. Create two dictionaries, one with unique words and their counts in all the tweets associated with "EastCoast" and a similar one for "WestCoast"
    '''
    words_eastcoast = {}
    words_westcoast = {}
    EastCoast = []
    WestCoast = []
    eastcoast_df = data[data['Label']=='EastCoast']
    westcoast_df = data[data['Label']=='WestCoast']

    for i in range(len(eastcoast_df)):
        sent = eastcoast_df.iloc[i]['Clean Text'].split(' ')
        for w in sent:
            if w not in words_eastcoast:
                words_eastcoast[w]=1
            else:
                words_eastcoast[w]+=1
                
    for i in range(len(westcoast_df)):
        sent = westcoast_df.iloc[i]['Clean Text'].split(' ')
        for w in sent:
            if w not in words_westcoast:
                words_westcoast[w]=1
            else:
                words_westcoast[w]+=1
    return words_eastcoast,words_westcoast


# In[4]:


# classifier : Train and apply a bayes net classifier
#
# This function should take a train_data dictionary that has three entries:
#        train_data["objects"] is a list of strings corresponding to documents
#        train_data["labels"] is a list of strings corresponding to ground truth labels for each document
#        train_data["classes"] is the list of possible class names (always two)
#
# and a test_data dictionary that has objects and classes entries in the same format as above. It
# should return a list of the same length as test_data["objects"], where the i-th element of the result
# list is the estimated classlabel for test_data["objects"][i]
#
# Do not change the return type or parameters of this function!
#
def classifier(train_data, test_data):

    '''
    The data is initially loaded into a dictionary of the form:

    ```
    {
    "objects": objects,
    "labels": labels,
    "classes": list(set(labels))
    }
    ```
    The training data and testing data are read into a Pandas dataframe.
    The train data dataframe has columns : Tweet, Label and the test data dataframe has columns: Tweet.
    '''
    train_data_df = pd.DataFrame({'Tweet':train_data['objects'], 'Label':train_data['labels']})
    train_data_df = clean_data(train_data_df)

    test_data_df = pd.DataFrame({'Tweet':test_data['objects']})
    test_data_df = clean_data(test_data_df)
    
    words_eastcoast,words_westcoast = get_words_label_matrix(train_data_df) 
    
    n_eastcoast = len(train_data_df[train_data_df['Label'] == 'EastCoast'])
    n_westcoast = len(train_data_df[train_data_df['Label'] == 'WestCoast'])
    
    # Prior Probabilities
    p_eastcoast = n_eastcoast/(n_eastcoast+n_westcoast)
    p_westcoast = n_westcoast/(n_eastcoast+n_westcoast)
    
    # Total Number of unique words in both labels.
    total_cnts_features_eastcoast = len(words_eastcoast)
    total_cnts_features_westcoast = len(words_westcoast)
    total_features = len(set(list(words_eastcoast.keys())+list(words_westcoast.keys())))

    labels = []
    
    for i in range(len(test_data_df)):
        probability_word_eastcoast = 1
        probability_word_westcoast = 1
        sent = test_data_df.iloc[i]['Clean Text'].split(' ')
        for word in sent:
            if word in words_eastcoast:
                p_word_eastcoast = words_eastcoast[word]/len(words_eastcoast)
                probability_word_eastcoast = probability_word_eastcoast * p_word_eastcoast
            
            else:
                probability_word_eastcoast = probability_word_eastcoast * (1/(total_cnts_features_eastcoast+total_features))
                
        for word in sent:
            if word in words_westcoast:
                p_word_westcoast = words_westcoast[word]/len(words_westcoast)
                probability_word_westcoast = probability_word_westcoast * p_word_westcoast
            
            else:
                probability_word_westcoast = probability_word_westcoast * (1/(total_cnts_features_westcoast+total_features))
                
        posterior_eastcoast = probability_word_eastcoast * p_eastcoast
        posterior_westcoast = probability_word_westcoast * p_westcoast


        # Classification:
        # Given a test tweet of the form w1 w2 w3 ... wn, the posterior probabilities of both labels are computed as follows:
        # P("EastCoast" | w1 w2 w3 ... wn) = P(w1 | "EastCoast) * P(w2 | "EastCoast") * ... * P( wn | "EastCoast") * P("EastCoast")
        # P("EastCoast" | w1 w2 w3 ... wn) = Posterior Probability
        # P(wn | "EastCoast) = Likelihood [Obtained from the two previously created dictionaries of unique words for both labels]
        # P("EastCoast") = Prior Probability [Calculated as number of tweets with East Coast Label / Total number of tweets]
        # The posterior probabilities for WestCoast label are computer in a similar manner.
        # In order to classify the tweet into either of the labels, the concept of "Odds Ratio" is utilized:
        # odds ratio = (P("EastCoast" | w1 w2 w3 ... wn)) / P("WestCoast" | w1 w2 w3 ... wn)
        # If the odds ratio > 1 then the tweet is classified as "EastCoast" and "WestCoast" otherwise.
        #
        # Special Case: Laplace Smoothing
        #
        # Suppose a word wk does not exist in the unique words dictionary for either labels, then the likelihood for this word give the label is zero.
        # In order to avoid the "zero probability" case, the word wk is assigned a small probability value as follows:
        # P(wk | "EastCoast") = 1 / (total number of unique words in east coast + total number of unique words across all documents)
        # P(wk | "WestCoast") is computed in a similar manner.

        odds_ratio = posterior_eastcoast / posterior_westcoast
        if odds_ratio > 1:
            label = "EastCoast"
        else:
            label = "WestCoast"
        labels.append(label)
    return labels

if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise Exception("Usage: classify.py train_file.txt test_file.txt")

    (_, train_file, test_file) = sys.argv
    # Load in the training and test datasets. The file format is simple: one object
    # per line, the first word one the line is the label.

    train_data = load_file(train_file)
    test_data = load_file(test_file)
    if(train_data["classes"] != test_data["classes"] or len(test_data["classes"]) != 2):
        raise Exception("Number of classes should be 2, and must be the same in test and training data")

    # make a copy of the test data without the correct labels, so the classifier can't cheat!
    test_data_sanitized = {"objects": test_data["objects"], "classes": test_data["classes"]}

    results= classifier(train_data, test_data_sanitized)

    # calculate accuracy
    correct_ct = sum([ (results[i] == test_data["labels"][i]) for i in range(0, len(test_data["labels"])) ])
    print("Classification accuracy = %5.2f%%" % (100.0 * correct_ct / len(test_data["labels"])))

