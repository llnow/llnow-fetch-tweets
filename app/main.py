from set_twitter import *
from fetch_stored_tweets import *
from fetch_new_tweets import *
from merge_tweets import *
from put_tweets import *
import os

# WordCloudを生成するために必要なツイート数
n_required_tweets = int(os.environ['N_REQUIRED_TWEETS'])
# ツイート取得リクエストの間隔(秒)
sleep_sec = int(os.environ['SLEEP_SEC'])
# max_api_request_force
max_api_request_force = int(os.environ['MAX_API_REQUEST_FORCE'])


def main(event, context):
    mode = context.invoked_function_arn.split(':')[-1]
    twitter = set_twitter()
    stored_tweets = fetch_stored_tweets(mode)
    new_tweets, search_metadata = fetch_new_tweets(twitter, sleep_sec, max_api_request_force, mode)
    res, flag_trigger_next_process = merge_tweets(stored_tweets, new_tweets, search_metadata, n_required_tweets, mode)
    put_tweets(res, flag_trigger_next_process, mode)
