import boto3
from botocore.exceptions import ClientError
import json
from distutils.util import strtobool
from get_ssm_params import *
from generate_archive_filename import *

bucket_name_prod = 'll-now-material'
bucket_name_dev = 'll-now-material-dev'
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')  # s3のファイル削除用


def put_tweets(tweets, flag_trigger_next_process, mode):
    # prodからdevバケットへもツイートをアップロードするかどうかをssmパラメータストアから取得
    key = 'll-now-upload-tweets-prod-to-dev'
    params = get_ssm_params(key)
    upload_tweets_prod_to_dev = strtobool(params[key])

    put_tweets_to_bucket(tweets, flag_trigger_next_process, mode)
    if mode == 'prod' and upload_tweets_prod_to_dev:
        put_tweets_to_bucket(tweets, flag_trigger_next_process, 'dev')


def put_tweets_to_bucket(tweets, flag_trigger_next_process, mode):
    if mode == 'dev':
        bucket_name = bucket_name_dev
    else:
        bucket_name = bucket_name_prod
    bucket = s3.Bucket(bucket_name)
    tweets_path = '/tmp/tweets.json'
    with open(tweets_path, 'w') as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    # 次の処理を呼び出す場合
    if flag_trigger_next_process:
        # 不要なstored_tweetsを削除
        try:
            s3_client.delete_object(Bucket=bucket_name, Key='tmp/stored_tweets.json')
        except ClientError as e:
            # stored_tweets.jsonがs3に存在しない場合は何もしない
            print(e)

        if mode == 'prod':
            # ツイートをアーカイブとしてs3に格納
            filename = generate_archive_filename(tweets)
            bucket.upload_file(tweets_path, 'archive/{}'.format(filename))

        # 次の処理のトリガーとしてs3に格納
        bucket.upload_file(tweets_path, 'tmp/ready_tweets.json')

    # 次の処理を呼び出さない場合
    else:
        # stored_tweetsとしてs3に格納
        bucket.upload_file(tweets_path, 'tmp/stored_tweets.json')
