import json
import main_functions
import requests
import streamlit as st
import pandas as pd
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from pprint import pprint
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

# nltk.download('punkt')
# nltk.download('stopwords')

api_key_dict = main_functions.read_from_file('JSON_files/api_key.json')
api_key = api_key_dict['my_key']
sections = ['arts', 'automobiles', 'books', 'business', 'fashion', 'food',
            'health', 'home', 'insider', 'magazine', 'movies', 'nyregion',
            'obituaries', 'opinion', 'politics', 'realestate', 'science',
            'sports', 'sundayreview', 'technology', 'theater', 't-magazine',
            'travel', 'upshot','us', 'world']
def get_top_stories(option):
    url = f'https://api.nytimes.com/svc/topstories/v2/{option}.json?api-key=' + api_key
    response = requests.get(url).json()
    main_functions.save_to_file(response, 'JSON_files/response.json')
    my_articles = main_functions.read_from_file('JSON_files/response.json')
    return my_articles


#Most viewed, shared, or emailed articles
def get_most_popular(type, period):
    api_key_dict = main_functions.read_from_file('JSON_files/api_key.json')
    api_key = api_key_dict['my_key']
    # type = ['emailed', 'shared', 'viewed']
    # period = [1, 7, 30]
    url2 = f'https://api.nytimes.com/svc/mostpopular/v2/{type}/{period}.json?api-key=' + api_key
    most_vse_response = requests.get(url2).json()
    main_functions.save_to_file(most_vse_response, 'JSON_files/most_vse_response.json')
    my_articles_pop = main_functions.read_from_file('JSON_files/most_vse_response.json')
    return my_articles_pop


#empty string to store the abstracts

def get_freq_dist(option):
    from nltk.corpus import stopwords
    my_articles = get_top_stories(option)
    str1 = ""
    for i in my_articles['results']:
        str1 += i['abstract']

    #sentences = sent_tokenize(str1)
    words = word_tokenize(str1)
    words_with_no_punct = []
    for w in words:
        if w.isalpha():
            words_with_no_punct.append(w.lower())
    stopwords = stopwords.words('english')
    words_withNo_stopwords = []
    for w in words_with_no_punct:
        if w not in stopwords:
            words_withNo_stopwords.append(w.lower())
    frequence_dist = FreqDist(words_withNo_stopwords)
    most_common_freq_dist = frequence_dist.most_common(10)
#pprint(most_common_freq_dist)
    return most_common_freq_dist

st.title('COP4813 - Web Application Programming')
st.header('Project 1')
st.subheader('Part A - The Stories API')

st.text('This app uses the Top Stories API to display the most common words used')
st.text('in the top current articles based on a specified topic selected by the user.')
st.text('The data is displayed as a line chart and as a wordcloud image.')

st.subheader('I. Topic Selection')

name = st.text_input('Please enter your name')

option = st.selectbox('Select a topic of your interest:',sections)
st.write(f'Hi {name}, you selected {option} topic')

'''*********************************************************************************************'''
st.subheader('II. Frequency Distribution')
see_freq_distr =st.checkbox('Click here to generate frquency distribution.')

most_common_freq_dist = get_freq_dist(option)
#my_table = dict(most_common_freq_dist)
my_table = pd.DataFrame(most_common_freq_dist)
if see_freq_distr:
    dframe = pd.DataFrame({
        'words': my_table[0],
        'count': my_table[1]
    })

    fig = px.line(dframe, x="words", y="count", title = '')
    st.plotly_chart(fig)

'''*********************************************************************************************'''
st.subheader('III. Wordcloud')
see_wordcloud =st.checkbox('Click here to generate wordcloud.')

if see_wordcloud:
    my_articles = get_top_stories(option)
    str1 = ""
    for i in my_articles['results']:
        str1 += i['abstract']

    word_cloud = WordCloud().generate(str1)
    plt.figure(figsize=(15, 15))
    plt.imshow(word_cloud)
    plt.axis('off')
    plt.show()
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)

'''*********************************************************************************************'''
st.subheader('Part B - Most Popular Articles')
st.text('Select if you want to see the most shared, emailed, or view articles.')

type = st.selectbox('Select your preferred set of articles',
                       ['','shared', 'emailed', 'viewed'])



'''*********************************************************************************************'''
period = st.selectbox('Select the period of time (last days)',
                       ['','1', '7', '30'])
if type and period:
    my_articles = get_most_popular(type, period)
    str2 = ""
    for i in my_articles['results']:
        str2 += i['abstract']

    word_cloud_popular = WordCloud().generate(str2)
    plt.figure(figsize=(15, 15))
    plt.imshow(word_cloud_popular)
    plt.axis('off')
    plt.show()
    st.pyplot()
    st.set_option('deprecation.showPyplotGlobalUse', False)