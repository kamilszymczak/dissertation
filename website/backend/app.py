import tweepy
from tweepy import OAuthHandler
from keras.models import load_model
from flask import Flask, jsonify, request
from flask_cors import CORS

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
model = load_model('model.h5')
# summarize model
# model.summary()

def getTweets():
    tweets_list = []
    query = "glasgow university OR uni OR student OR studying -FC -filter:retweets -filter:links -filter:mentions"

    # Fetching tweets with parameters
    results = api.search(q=query, lang="en", tweet_mode='extended', count=100)

    # loop through all tweets pulled
    for tweet in results:
        row_list.append(tweet.full_text)
    return tweets_list

def getSentiment(tweets)
    tweets_sequences = tokenizer.texts_to_sequences(tweets)
    padded = pad_sequences(tweets_sequences, maxlen=122)
    sentiment = model.predict(padded)

    return [{"review": tweets[i], "sentiment": sentiment[i]} for i in range(len(tweets))]


@app.route('/getTweets', methods=['POST'])
def predict(tweets):
    if request.method == "POST":
        user_query = request.form['query']
        tweets = getTweets()

        sentiment = getSentiment(tweets)
        return jsonify(sentiment), 200