import tweepy
from tweepy import OAuthHandler

from flask import Flask, jsonify, request
from flask_cors import CORS
import html

from tensorflow import keras
import pickle as pk
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.models import load_model
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
import os
print(os.getcwd())
os.chdir('../../')
print(os.getcwd())
model = load_model('ml/model_exported.h5')
# load tokenizer
with open("ml/tokenizer_m1.pickle", 'rb') as handle:
    tokenizer = pk.load(handle)
print("ML Model Loaded")
# summarize model
# model.summary()

def getTweets(user_query):
    query = user_query + " OR uni OR student OR studying -FC -filter:retweets -filter:links -filter:mentions"

    # Fetching tweets with parameters
    results = api.search(q=query, lang="en", tweet_mode='extended', count=100)

    # loop through all tweets pulled
    tweets_list = []
    for tweet in results:
        #html.unescape to fix HTML esape e.g. &amp; to &
        tweets_list.append(html.unescape(tweet.full_text))
    return tweets_list


def getSentiment(tweets):
    tweets_sequences = tokenizer.texts_to_sequences(tweets)
    padded = pad_sequences(tweets_sequences, maxlen=137)
    sentiment = model.predict(padded).tolist()

    return [{"review": tweets[i], "sentiment": sentiment[i][0]} for i in range(len(tweets))]


@app.route('/', methods=['POST'])
def predict():
    if request.method == "POST":
        user_query = request.form['input']
        print(user_query)
        tweets = getTweets(user_query)

        output = getSentiment(tweets)
        return jsonify(output), 200