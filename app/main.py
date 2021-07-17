from set_twitter import *
from fetch_stored_tweets import *
from fetch_new_tweets import *
from merge_tweets import *
from put_tweets import *
import os

# WordCloudを生成するために必要なツイート数
N_REQUIRED_TWEETS = int(os.environ['N_REQUIRED_TWEETS'])
# ツイート取得リクエストの間隔(秒)
sleep_sec = int(os.environ['SLEEP_SEC'])
# max_api_request_force
max_api_request_force = int(os.environ['MAX_API_REQUEST_FORCE'])


def main(event, context):
    twitter = set_twitter()
    stored_tweets = fetch_stored_tweets()
    new_tweets = fetch_new_tweets(twitter, sleep_sec, max_api_request_force)
    tweets = merge_tweets(stored_tweets, new_tweets)
    put_tweets(tweets, N_REQUIRED_TWEETS)
