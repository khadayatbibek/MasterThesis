# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 13:37:26 2020

@author: Bibek77
"""


import re
import pandas as pd
import numpy as np
import nltk
import string
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import  WhitespaceTokenizer

# tokenize text

wh_token=WhitespaceTokenizer()

def tokenize_text(All_texts):
   #TOKEN_PATTERN = r'\s+'
    #regex_wt = nltk.RegexpTokenizer(pattern=TOKEN_PATTERN, gaps=True)
    word_tokens = wh_token.tokenize(All_texts)
    return word_tokens



def remove_characters_after_tokenization(tokens):
    remove=string.punctuation
    remove = remove.replace(".", "’")
    remove = remove.replace("?", "“")
    remove = remove.replace("", "”")
    remove = remove.replace("", "-")

    #remove = remove.replace("", "‘")
   # remove = remove.replace("", "•")
    #remove = remove.replace("", "•")


    
    
    pattern = re.compile('[{}]'.format(re.escape(remove))) 
    filtered_tokens = filter(None, [pattern.sub('', token) for token in tokens]) 
    return filtered_tokens

def convert_to_lowercase(tokens):
    return [token.lower() for token in tokens ]

def remove_stopwords(tokens):
    stopword_list = nltk.corpus.stopwords.words('english')
    filtered_tokens = [token for token in tokens if token not in stopword_list]
    return filtered_tokens

def apply_lemmatization(tokens, wnl=WordNetLemmatizer()):
    return [wnl.lemmatize(token) for token in tokens]

def cleanText(All_texts):
    clean_texts = []
    for txt in All_texts:
        text_i = tokenize_text(txt)
        text_i = remove_characters_after_tokenization(text_i)
        text_i = convert_to_lowercase(text_i)
        #text_i = remove_stopwords(text_i)
        #text_i = apply_lemmatization(text_i)
        clean_texts.append(text_i)
    return clean_texts