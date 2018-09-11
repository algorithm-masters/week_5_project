import nltk
import numpy

from nltk.tokenize import sent_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)
(100, 100)

train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]
training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs
sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])
# We use simple unigram word features, handling negation:

unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
len(unigram_feats)
83
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)
# We apply features to obtain a feature-value representation of our datasets:

training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)
# We can now train our classifier on the training set, and subsequently output the evaluation results:

trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)
# Training classifier

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

