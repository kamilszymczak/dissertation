import tweepy
from tweepy import OAuthHandler

from flask import Flask, jsonify, request
from flask_cors import CORS
import html
import numpy as np
from tensorflow import keras
import pickle as pk

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os
# os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

app = Flask(__name__)
CORS(app, supports_credentials=True)

# Twitter API keys
consumer_key= 'maIS6lxgXN5a41WCXA4mG2xXB'
consumer_secret= '649l6RQZh74xfusSyrGWcm9n65bBD3FQ1qBUY2lpffpW3O2NGz'
access_token= '1947162528-h6f9zcAPcUHBzVlamjOyXsS8HFtRmgvVkYnmAZ2'
access_token_secret= 'hwz6ncD2vT66iXdPkI1yPRUHQp5XBZgslpAe2IScSgEzm'
# Creating the authentication object
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# Setting your access token and secret
auth.set_access_token(access_token, access_token_secret)
# Creating the API object while passing in auth information
api = tweepy.API(auth) 


# load ML model
model = load_model('../../ml/model_exported.h5')
# load tokenizer
with open("../../ml/tokenizer_m1.pickle", 'rb') as handle:
    tokenizer = pk.load(handle)
print("ML Model Loaded")

from nltk.tokenize import RegexpTokenizer
import re
import sys 
# sys.path.append('E:\GitHubProjects\dissertation\Scripts')
sys.path.append('..\..\Scripts')
import helperfn as hf

stop = hf.stop_words()
uni_names = hf.uni_names()

def getTweets(user_query):
    query = '%s (university OR uni OR studying OR student OR lecture OR lectures OR professor OR lecturer) -"FC" -filter:retweets -filter:links -filter:mentions' % (user_query)

    # Fetching tweets with parameters
    results = api.search(q=query, lang="en", tweet_mode='extended', count=100)

    # loop through all tweets pulled
    tweets_list = []
    for tweet in results:
        #html.unescape to fix HTML esape e.g. &amp; to &
        unescape = html.unescape(tweet.full_text)
        # removal of \n next line char replaced with space
        tweets_list.append(re.sub(r"\n", " ", unescape))
    return tweets_list


def getSentiment(tweets):
    tweets_sequences = tokenizer.texts_to_sequences(tweets)
    padded = pad_sequences(tweets_sequences, maxlen=137)
    sentiment = model.predict(padded).flatten().tolist()

    # return [{"review": tweets[i], "sentiment": sentiment[i][0]} for i in range(len(tweets))]
    return sentiment

def cleanTweets(tweets):
    tweets = hf.remove_mentions(tweets)

    tokenizer = RegexpTokenizer(r'([\w\']+|\[+|]+|\!+|"+|\$+|%+|&+|\'+|\(+|\)+|\*+|\++|,+|\.+|:+|;+|=+|#+|@+|\?+|\[+|\^+|_+|`+|{+|\|+|\}+|~+|-+|]+)') 

    tweets = [tokenizer.tokenize(x) for x in tweets]

    # lower case
    tweets = [hf.lower_token(x) for x in tweets]

    # remove stop words
    # tweets = [item for item in tweets if item not in stop]
    tweets = [hf.remove_stopwords(x) for x in tweets]

    # remove university names as they impact accuracy, these words should be neutral sentiment 
    # tweets = [item for item in tweets if item not in uni_names]
    tweets = [hf.remove_uni_names(x) for x in tweets]

    # #reduce puncuations, remove duplicates next to each other and leave only one e.g. !!! to !
    tweets = [hf.remove_punctuations(x) for x in tweets]
    return tweets

def cleanSingle(text):
    # remove @ mentions or URL links
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)

    tokenizer = RegexpTokenizer(r'([\w\']+|\[+|]+|\!+|"+|\$+|%+|&+|\'+|\(+|\)+|\*+|\++|,+|\.+|:+|;+|=+|#+|@+|\?+|\[+|\^+|_+|`+|{+|\|+|\}+|~+|-+|]+)') 

    text = tokenizer.tokenize(text)

    # lower case
    text = hf.lower_token(text)

    # remove stop words
    text = [item for item in text if item not in stop]

    # remove university names as they impact accuracy, these words should be neutral sentiment 
    text = [item for item in text if item not in uni_names]

    # reduce puncuations, remove duplicates next to each other and leave only one e.g. !!! to !
    text = hf.remove_punctuations(text)
    return text


from nltk.tokenize import sent_tokenize, word_tokenize
def sentimentSentence(tweets):
    allTweets = []
    for tweet in tweets:
        sentences = sent_tokenize(tweet) 
        sentencesClean = [cleanSingle(sentence) for sentence in sentences]    
        tweetSentiment = getSentiment(sentencesClean)
        singleTweet = [{"tweet": [{"sentence": sentences[i], "sentiment": tweetSentiment[i]} for i in range(len(sentences))]}]
        allTweets.append(singleTweet)

    return allTweets

def sentimentToString(pred):
    rounded = round(pred)
    if rounded == 0:
        return "Negative"
    else:
        return "Positive"

@app.route('/', methods=['POST'])
def predict():
    if request.method == "POST":
        user_query = request.form['input']
        tweets = getTweets(user_query)

        #PREDICT EACH TWEET VERSION
        cleaned = cleanTweets(tweets)
        sentiment = getSentiment(cleaned)
        output = [{"review": tweets[i], "sentiment": sentimentToString(sentiment[i])} for i in range(len(tweets))]
        return jsonify(output), 200

        #PREDICT SENTENCES VERSION
        # output = sentimentSentence(tweets)
        # return jsonify(output), 200