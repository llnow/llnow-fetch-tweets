import boto3
import os
from distutils.util import strtobool
from botocore.exceptions import ClientError
import json
from generate_archive_filename import *

bucket_name_prod = 'll-now-material'
bucket_name_dev = 'll-now-material-dev'
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')  # s3のファイル削除用

upload_tweets_prod_to_dev = strtobool(os.environ['UPLOAD_TWEETS_PROD_TO_DEV'])


def put_tweets(tweets, n_required_tweets, mode):
    if mode == 'dev':
        put_tweets_to_bucket(tweets, n_required_tweets, mode)
    if mode == 'prod':
        if upload_tweets_prod_to_dev:
            put_tweets_to_bucket(tweets, n_required_tweets, 'dev')
        put_tweets_to_bucket(tweets, n_required_tweets, mode)


def put_tweets_to_bucket(tweets, n_required_tweets, mode):
    if mode == 'dev':
        bucket_name = bucket_name_dev
    else:
        bucket_name = bucket_name_prod
    bucket = s3.Bucket(bucket_name)
    tweets_path = '/tmp/tweets.json'
    with open(tweets_path, 'w') as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    # 取得ツイート数が十分な場合
    if len(tweets) >= n_required_tweets:
        # 不要なstored_tweetsを削除
        try:
            s3_client.delete_object(Bucket=bucket_name, Key='tmp/stored_tweets.json')
        except ClientError:
            # stored_tweets.jsonがs3に存在しない場合は何もしない
            pass

        if mode == 'prod':
            # ツイートをアーカイブとしてs3に格納
            filename = generate_archive_filename(tweets)
            bucket.upload_file(tweets_path, 'archive/{}'.format(filename))

        # 次の処理のトリガーとしてs3に格納
        bucket.upload_file(tweets_path, 'tmp/ready_tweets.json')

    # 取得ツイート数が不十分な場合
    else:
        # stored_tweetsとしてs3に格納
        bucket.upload_file(tweets_path, 'tmp/stored_tweets.json')
