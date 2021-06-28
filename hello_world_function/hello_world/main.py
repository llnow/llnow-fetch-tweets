from fetch_stored_tweet import *
from fetch_new_tweet import *
from merge_tweet import *
from put_tweet import *
from requests_oauthlib import OAuth1Session
import os


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
THRESHOLD = 1000  # WordCloudを生成するために必要なツイート数

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main(event, context):
    stored_tweets = fetch_stored_tweet()
    new_tweets = fetch_new_tweet(twitter)
    tweets = merge_tweet(stored_tweets, new_tweets)
    put_tweet(tweets)
