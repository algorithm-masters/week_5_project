import nltk
import numpy as np
import pandas as pd
import bokeh as bk
from bokeh.models.glyphs import VBar
from bokeh.models import ColumnDataSource, DataRange1d, Plot, LinearAxis, Grid
from bokeh.io import curdoc, show
from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from pyramid_restful.viewsets import APIViewSet
from pyramid.response import Response
from pyramid.view import view_config
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def stacked_bar_for_one(data):
    """ Chart display for one analysis/one user.
    """
    if data == {}:
        return 'There is not data for this user'
    analysis_df = pd.DataFrame()
    user_id = data.keys()
    sentence_counter = 0
    key_list = []
    for key in user_id:
        for one_record in data[key]:
            record_obj = json.loads(one_record)
            for sentence in record_obj['Sentences']:
                # key_list.append(sentence)
                ss = record_obj['Sentences'][sentence]
                ss['sentence'] = sentence
                columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
                sentence_counter += 1
                key_list.append(str(sentence_counter))
                index = [sentence_counter]
                temp = pd.DataFrame(ss, columns=columns, index=index)
                analysis_df = pd.concat([analysis_df, temp], sort=True)
    output_file("stacked.html")
    
    # import pdb; pdb.set_trace()
    # key_list = list(obj['Sentences'].keys())
    emotions = ['Negative', 'Neutral', 'Positive']
    data = {'Sentences': analysis_df.index,
            'Negative': analysis_df.neg,
            'Neutral': analysis_df.neu,
            'Positive': analysis_df.pos}
    colors = ["#e84d60", "#c9d9d3", "#718dbf"]
    p = figure(x_range=key_list, y_range=(0, 1.2), plot_height=500, title="Sentiment Analysis",
            toolbar_location=None, tools="")
    p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
                legend=[value(x) for x in emotions])
    p.y_range.start = 0
    p.x_range.range_padding = 0.2
    p.xaxis.axis_label = 'Sentences'
    p.yaxis.axis_label = 'Percentage (%)'
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    html = file_html(p, CDN, "Single User Stacked Bar")
    return html

def stacked_bar_for_all(data):
    """ Chart display for get analysis for all users combined.
    This is for the admin to view a collection of user's analysis  """
    if data == {}:
        return 'There is no data in the database'

    analysis_df = pd.DataFrame()
    user_id = data.keys()
    sentence_counter = 0
    key_list = []
    for key in user_id:
        for one_record in data[key]:
            record_obj = json.loads(one_record)
            for sentence in record_obj['Sentences']:
                # key_list.append(sentence)
                ss = record_obj['Sentences'][sentence]
                ss['sentence'] = sentence
                columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
                sentence_counter += 1
                key_list.append(str(sentence_counter))
                index = [sentence_counter]
                temp = pd.DataFrame(ss, columns=columns, index=index)
                analysis_df = pd.concat([analysis_df, temp], sort=True)
    output_file("stacked.html")
    
    # import pdb; pdb.set_trace()
    # key_list = list(obj['Sentences'].keys())
    emotions = ['Negative', 'Neutral', 'Positive']
    data = {'Sentences': analysis_df.index,
            'Negative': analysis_df.neg,
            'Neutral': analysis_df.neu,
            'Positive': analysis_df.pos}
    colors = ["#e84d60", "#c9d9d3", "#718dbf"]
    p = figure(x_range=key_list, y_range=(0, 1.2), plot_height=500, title="Sentiment Analysis",
            toolbar_location=None, tools="")
    p.vbar_stack(emotions, x='Sentences', width=0.9, color=colors, source=data,
                legend=[value(x) for x in emotions])
    p.y_range.start = 0
    p.x_range.range_padding = 0.2
    p.xaxis.visible = False
    p.xaxis.axis_label = 'Sentences'
    p.yaxis.axis_label = 'Percentage (%)'
    p.xgrid.grid_line_color = None
    p.axis.minor_tick_line_color = None
    p.outline_line_color = None
    p.legend.location = "top_left"
    p.legend.orientation = "horizontal"
    html = file_html(p, CDN, "Single User Stacked Bar")
    return html


def pie_for_all(data):
    if data == {}:
        return 'There is no data in the database'
    analysis_df = pd.DataFrame()
    user_id = data.keys()
    sentence_counter = 0
    key_list = []
    for key in user_id:
        for one_record in data[key]:
            record_obj = json.loads(one_record)
            for sentence in record_obj['Sentences']:
                # key_list.append(sentence)
                ss = record_obj['Sentences'][sentence]
                ss['sentence'] = sentence
                columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
                sentence_counter += 1
                key_list.append(str(sentence_counter))
                index = [sentence_counter]
                temp = pd.DataFrame(ss, columns=columns, index=index)
                analysis_df = pd.concat([analysis_df, temp], sort=True)
    output_file("stacked.html")


def compound_for_all(data):
    if data == {}:
        return 'There is not data for this user'
    analysis_df = pd.DataFrame()
    user_id = data.keys()
    sentence_counter = 0
    key_list = []
    for key in user_id:
        for one_record in data[key]:
            record_obj = json.loads(one_record)
            for sentence in record_obj['Sentences']:
                # key_list.append(sentence)
                ss = record_obj['Sentences'][sentence]
                ss['sentence'] = sentence
                columns = ['neg', 'neu', 'pos', 'compound', 'sentence']
                sentence_counter += 1
                key_list.append(str(sentence_counter))
                index = [sentence_counter]
                temp = pd.DataFrame(ss, columns=columns, index=index)
                analysis_df = pd.concat([analysis_df, temp], sort=True)
    output_file("stacked.html")

    source_bar = figure(plot_width=1000, plot_height=400, title="Compound Bar for All Users")
    source_bar.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['compound'], color="#718dbf")
    source_bar.xaxis.axis_label = 'Sentances'
    source_bar.yaxis.axis_label = 'Percentage'
    source_bar2 = figure(plot_width=1000, plot_height=400, title="Negative Bar for All Users")
    source_bar2.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['neg'], color="#e84d60")
    source_bar2.xaxis.axis_label = 'Sentances'
    source_bar2.yaxis.axis_label = 'Percentage'
    source_bar3 = figure(plot_width=1000, plot_height=400, title="Positive Bar for All Users")
    source_bar3.vbar(x=analysis_df.index, width=1, bottom=0, top=analysis_df['pos'], color="#64b479")
    source_bar3.xaxis.axis_label = 'Sentances'
    source_bar3.yaxis.axis_label = 'Percentage'
    graphs = [source_bar, source_bar2, source_bar3]
    html = file_html(graphs, CDN, "Compound bar for all")
    return html
        
