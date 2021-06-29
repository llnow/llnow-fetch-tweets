import boto3
import json

BUCKET_NAME = 'll-now-material'


def put_tweets(tweets, THRESHOLD):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    tweets_path = '/tmp/tweets.json'
    with open(tweets_path, 'w') as f:
        json.dump(tweets, f, indent=4)
    # ready_tweetsとしてs3に格納
    if len(tweets) >= THRESHOLD:
        # アップロード(上書き)
        bucket.upload_file(tweets_path, 'tmp/ready_tweets.json')
    # stored_tweetsとしてs3に格納
    else:
        # アップロード(上書き)
        bucket.upload_file(tweets_path, 'tmp/stored_tweets.json')
