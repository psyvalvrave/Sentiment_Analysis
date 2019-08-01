#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Names: Zhecheng Li
Program: Sentiment Analysis
Description: Extract text and star ratings from Yelp reviews json file
            Find lemmas, filter stopwords and words not in english corpus
            Produce a list in descending order with the top 500 best rated
            and 500 worst rated, and write to csv file
Last Modified: 26 Feb 2019
"""

import json
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
import csv

pos_translate = {'J':'a' , 'V':'v', 'N':'n', 'R':'r'}
def getTag(tag):
    if tag in pos_translate: return pos_translate[tag]
    else: return 'n'
    
lem = WordNetLemmatizer()
en_stopwords = set(stopwords.words('english'))
en_words = set(words.words('en'))

with open('yelp_academic_dataset_review_small.json') as file_r:
    data = json.load(file_r)
    
num_reviews = 0
lemma_list = {}
for review in data:    
    word_list = set(word_tokenize(review['text'].lower()))
    lemmas = {lem.lemmatize(wd[0], getTag(wd[1][0])) for wd in pos_tag(word_list)}
    lemmas = [wd for wd in lemmas if wd not in en_stopwords and wd in en_words]
    
    for wd in lemmas:
        if wd not in lemma_list:
            lemma_list[wd] = [review['stars'], 1]
        else:
            lemma_list[wd] = [(lemma_list[wd][0]+review['stars']), lemma_list[wd][1]+1]
         
    num_reviews += 1
    print('Processing: ' + str(round(num_reviews*100/len(data), 2)) + "%")

lemma_dict = {w:(r[0]/r[1]) for w,r in lemma_list.items() if r[1] >= 10}
lemmas = sorted(lemma_dict, key=lemma_dict.__getitem__, reverse=True)
lemma_dict = {wd:lemma_dict[wd] for wd in (lemmas[:500]+lemmas[-500:])}

with open("sentiment_analysis.csv", "w") as csvWrite:
        fieldnames=["",""]
        writer=csv.writer(csvWrite,delimiter=',')
        for wd,r in lemma_dict.items():
            writer.writerow([wd,r])