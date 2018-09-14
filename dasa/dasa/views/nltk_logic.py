import nltk
import numpy

from nltk.tokenize import sent_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyze(input_message):
    """This function will take in the input text (which is parsed to a string in nltk_output.py),
    divide up the string into sentences using the nltk tokenizer, and analyze each sentence
    for sentiment. The nltk analysis was trained above this function using the pre built nltk corpus.
    ARGS:
        Input string
    OUTPUT:
        JSON sendable object of sentence by sentence sentiment analysis, as well as aggregate analysis
        of the entire file.
    """
    sid = SentimentIntensityAnalyzer()
    sentence_list = sent_tokenize(input_message)
    response_object = {
        'Sentences':{},
        'Body':''
    }
    for sentence_num in range(len(sentence_list)):
        ss = sid.polarity_scores(sentence_list[sentence_num])
        response_object['Sentences'][sentence_num] = [sentence_list[sentence_num], ss]

    ss_body = sid.polarity_scores(input_message)
    response_object['Body'] = ss_body

    return response_object
