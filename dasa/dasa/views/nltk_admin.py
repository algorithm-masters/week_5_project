# import nltk
# import numpy as np
# import pandas as pd
# import matplotlib
# import matplotlib.pyplot as plt
# import bokeh as bk
# from bokeh.models.glyphs import VBar
# from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
# from bokeh.io import curdoc, show

# # from sklearn.model_selection import train_test_split
# # from sklearn.metrics import mean_squared_error

# # nltk.download()
# from nltk.classify import NaiveBayesClassifier
# from nltk.corpus import subjectivity
# from nltk.sentiment import SentimentAnalyzer
# from nltk.sentiment.util import *
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# # %matplotlib inline

from pyramid_restful.viewsets import APIViewSet
from sqlalchemy.exc import IntegrityError, DataError
from pyramid.view import view_config
from pyramid.response import Response
from ..models.nltk_output import NLTKOutput
from ..models.account import Account
import requests
import json


class NLTKAPIAdmin(APIViewSet):
    """This will create the endpoints to visualize the data that has already
    been created within the database.
    """
    
    def list(self, request, graph_type=None):
        """This performs a get all request, which gets all the user data in the database,
        converts it to the type of graph that is requested, and returns html containing that
        graph.
        """
        import pdb; pdb.set_trace()
        user = {}
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        
        if account.check_admin(request, user):
            if graph_type == 'stacked_bar':
                cleaned_data = {}
                raw_data = NLTKOutput.all(request)
                for record in raw_data:
                    if record.account_id in cleaned_data:
                        cleaned_data[record.account_id].append(record.nltk_result)
                    else:
                        cleaned_data[record.account_id] = [record.nltk_result]
                
                # Send data to chart maker

                
        return Response(json=cleaned_data, status=200)

    def retrieve(self, request, graph_type=None, user_id=None):
        """This retrieves a single users data by email, and displays it with the
        given chart type
        """
        user = {}
        user_id = id
        if request.authenticated_userid:
            account = Account.one(request, request.authenticated_userid)
            user['account_id'] = account.id
        
        if account.check_admin(request, user):
            if graph_type == 'stacked_bar':
                cleaned_data = {}
                raw_data = NLTKOutput.all(request)
                for record in raw_data:
                    if record.account_id in cleaned_data:
                        cleaned_data[record.account_id].append(record.nltk_result)
                    else:
                        cleaned_data[record.account_id] = [record.nltk_result]

        return Response(json='This works', status=200)

        
# matplotlib.rcParams['figure.figsize'] = [12.0, 8.0]

# n_instances = 100
# subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
# obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
# len(subj_docs), len(obj_docs)
# (100, 100)

# train_subj_docs = subj_docs[:80]
# test_subj_docs = subj_docs[80:100]
# train_obj_docs = obj_docs[:80]
# test_obj_docs = obj_docs[80:100]
# training_docs = train_subj_docs+train_obj_docs
# testing_docs = test_subj_docs+test_obj_docs
# sentim_analyzer = SentimentAnalyzer()
# all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

# unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
# len(unigram_feats)
# 83
# sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

# training_set = sentim_analyzer.apply_features(training_docs)
# test_set = sentim_analyzer.apply_features(testing_docs)

# trainer = NaiveBayesClassifier.train
# classifier = sentim_analyzer.train(trainer, training_set)

# for key,value in sorted(sentim_analyzer.evaluate(test_set).items()):
# 	print('{0}: {1}'.format(key, value))

# sentences = [
# 	"This is a positive sentence and really good!",
# 	"I hate my job and my boss sucks",
# 	"I love pizza and it tastes great",
# 	"Max is so smart",
# 	"My dog is dumber than a box of rocks",
# 	"Code Fellows is a great bootcamp"
# 	]

# obj = {
#     "Sentences": {
#         "0":
#             {
#                 "neg": 0,
#                 "neu": 0.406,
#                 "pos": 0.594,
#                 "compound": 0.6588
#             }
#         ,
#         "1": 
#             {
#                 "neg": 0,
#                 "neu": 0.701,
#                 "pos": 0.299,
#                 "compound": 0.4561
#             }
#         ,
#         "2": 
#             {
#                 "neg": 0.561,
#                 "neu": 0.343,
#                 "pos": 0.096,
#                 "compound": -0.8301
#             }
#         ,
#         "3":
#             {
#                 "neg": 0,
#                 "neu": 0.435,
#                 "pos": 0.565,
#                 "compound": 0.5994
#             }
#         ,
#         "4": 
#             {
#                 "neg": 0,
#                 "neu": 1,
#                 "pos": 0,
#                 "compound": 0
#             }
        
#     },
#     "Body": {
#         "neg": 0.186,
#         "neu": 0.525,
#         "pos": 0.289,
#         "compound": 0.544
#     }
# }

# sid = SentimentIntensityAnalyzer()
# for sentence in sentences:
#      ss = sid.polarity_scores(sentence)

# df = pd.DataFrame()
# for i in range(len(obj)):
#     ss = sid.polarity_scores(sentences[i])
#     ss['text'] = sentences[i]
#     columns = ['neg', 'neu', 'pos', 'compound', 'text']
#     index = [i]
    
#     temp = pd.DataFrame(ss, columns=columns, index=index)
#     df = pd.concat([df, temp], sort=True)
   

# from bokeh.core.properties import value
# from bokeh.io import show, output_file
# from bokeh.plotting import figure

# output_file("stacked.html")

# emotions = ['Negative', 'Neutral', 'Positive']


# data = {'Sentences' : df.index,
#         'Negative'   : df.neg,
#         'Neutral'   : df.neu,
#         'Positive'   : df.pos}
# colors = ["#e84d60", "#c9d9d3", "#718dbf"]

# p = figure(x_range=sentences, y_range=(0, 1.2), plot_height=500, title="Sentiment Analysis",
#            toolbar_location=None, tools="")

# p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
#              legend=[value(x) for x in emotions])

# p.y_range.start = 0
# p.x_range.range_padding = 0.2
# p.xgrid.grid_line_color = None
# p.axis.minor_tick_line_color = None
# p.outline_line_color = None
# p.legend.location = "top_left"
# p.legend.orientation = "horizontal"

# show(p)
