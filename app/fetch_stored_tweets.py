import boto3
from botocore.exceptions import ClientError
import json

bucket_name_prod = 'll-now-material'
bucket_name_dev = 'll-now-material-dev'
bucket_key = 'tmp/stored_tweets.json'


def fetch_stored_tweets(mode):
    s3 = boto3.resource('s3')
    if mode == 'dev':
        bucket_name = bucket_name_dev
    else:
        bucket_name = bucket_name_prod
    bucket = s3.Bucket(bucket_name)
    obj = bucket.Object(bucket_key)
    try:
        response = obj.get()
    except ClientError as e:
        # stored_tweets.jsonがs3に存在しない場合
        print(e)
        return None
    body = response['Body'].read()
    tweets = json.loads(body.decode('utf-8'))['statuses']  # search_metadataは取得せず，statusesだけ取得する

    return tweets
