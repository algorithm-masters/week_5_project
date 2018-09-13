import nltk
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import bokeh as bk
from bokeh.models.glyphs import VBar
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid

from bokeh.io import curdoc, show
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure

# from sklearn.model_selection import train_test_split
# from sklearn.metrics import mean_squared_error

# nltk.download()
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
from pyramid.view import view_config
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# %matplotlib inline

# matplotlib.rcParams['figure.figsize'] = [12.0, 8.0]


sentences = [
    "This is a positive sentence and really good!",
    "I hate my job and my boss sucks",
    "I love pizza and it tastes great",
    "Max is so smart",
    "My dog is dumber than a box of rocks",
    "Code Fellows is a great bootcamp"
]

obj = {
    "Sentences": {
        "0":
            {
                "neg": 0,
                "neu": 0.406,
                "pos": 0.594,
                "compound": 0.6588
            }
        ,
        "1":
            {
                "neg": 0,
                "neu": 0.701,
                "pos": 0.299,
                "compound": 0.4561
            }
        ,
        "2":
            {
                "neg": 0.561,
                "neu": 0.343,
                "pos": 0.096,
                "compound": -0.8301
            }
        ,
        "3":
            {
                "neg": 0,
                "neu": 0.435,
                "pos": 0.565,
                "compound": 0.5994
            }
        ,
        "4":
            {
                "neg": 0,
                "neu": 1,
                "pos": 0,
                "compound": 0
            }

    },

    "Body": {
        "neg": 0.186,
        "neu": 0.525,
        "pos": 0.289,
        "compound": 0.544
    }
}


class ChartsAPIView(APIViewSet):
    def chart_for_one_user(self, data):
        """ Chart display for one analysis/one user. """
        pass

    def chart_get_all_analysis(self, data):
        """ Chart display for get analysis for all users combined.
        This is for the admin to view a collection of user's analysis  """
        pass

# BELOW IS FROM JUPYTER NOTEBOOK
# function takes in an object, return html.
sid = SentimentIntensityAnalyzer()
for sentence in sentences:
    ss = sid.polarity_scores(sentence)

df = pd.DataFrame()
for i in range(len(obj)):
    ss = sid.polarity_scores(sentences[i])
    ss['text'] = sentences[i]
    columns = ['neg', 'neu', 'pos', 'compound', 'text']
    index = [i]

    temp = pd.DataFrame(ss, columns=columns, index=index)
    df = pd.concat([df, temp], sort=True)

# Bokeh

output_file("stacked.html")

emotions = ['Negative', 'Neutral', 'Positive']

data = {'Sentences': df.index,
        'Negative': df.neg,
        'Neutral': df.neu,
        'Positive': df.pos}
colors = ["#e84d60", "#c9d9d3", "#718dbf"]

key_list = list(obj['Sentences'].keys())

p = figure(x_range=key_list, y_range=(0, 1.2), plot_height=500, title="Sentiment Analysis",
           toolbar_location=None, tools="")

p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
             legend=[value(x) for x in emotions])

p.y_range.start = 0
p.x_range.range_padding = 0.2
p.xgrid.grid_line_color = None
p.axis.minor_tick_line_color = None
p.outline_line_color = None
p.legend.location = "top_left"
p.legend.orientation = "horizontal"

# show(p)