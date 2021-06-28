import boto3
import json

BUCKET_NAME = 'll-now-material'
BUCKET_KEY = 'stored_tweets.json'


def fetch_stored_tweets():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)
    obj = bucket.Object(BUCKET_KEY)
    response = obj.get()
    body = response['Body'].read()
    tweets = json.loads(body.decode('utf-8'))

    return tweets
