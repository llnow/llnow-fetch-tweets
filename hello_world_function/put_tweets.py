import boto3
import json

BUCKET_NAME = 'll-now-material'


def put_tweets(tweets, THRESHOLD):
    s3 = boto3.resource('s3')
    s3_client = boto3.client('s3')  # s3のファイル削除用
    bucket = s3.Bucket(BUCKET_NAME)
    tweets_path = '/tmp/tweets.json'
    with open(tweets_path, 'w') as f:
        json.dump(tweets, f, indent=4, ensure_ascii=False)
    # 取得ツイート数が十分な場合
    if len(tweets) >= THRESHOLD:
        # 不要なstored_tweetsを削除
        s3_client.delete_object(Bucket=BUCKET_NAME, Key='tmp/stored_tweets.json')
        # ready_tweetsとしてs3に格納(次の処理のトリガー)
        bucket.upload_file(tweets_path, 'tmp/ready_tweets.json')
    # 取得ツイート数が不十分な場合
    else:
        # stored_tweetsとしてs3に格納
        bucket.upload_file(tweets_path, 'tmp/stored_tweets.json')
