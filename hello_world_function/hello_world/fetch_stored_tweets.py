import boto3
import json

BUCKET_NAME = 'll-now-material'
BUCKET_KEY = 'stored_tweets.json'


def fetch_stored_tweets():
    s3 = boto3.client('s3')
    res = s3.get_object(Bucket=BUCKET_NAME, Key=BUCKET_KEY)
    stored_tweets = json.loads(res['Body'].read().decode('utf-8'))
    return stored_tweets
