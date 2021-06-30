from fetch_stored_tweets import *
from fetch_new_tweets import *
from merge_tweets import *
from put_tweets import *
from requests_oauthlib import OAuth1Session
import os


CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
N_REQUIRED_TWEETS = os.environ['N_REQUIRED_TWEETS']  # WordCloudを生成するために必要なツイート数

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)


def main(event, context):
    stored_tweets = fetch_stored_tweets()
    new_tweets = fetch_new_tweets(twitter)
    tweets = merge_tweets(stored_tweets, new_tweets)
    put_tweets(tweets, THRESHOLD)
