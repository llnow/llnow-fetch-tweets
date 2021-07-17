import boto3
import re


def check_valid_tweet(tweet):
    text = tweet['text']
    source = tweet['source']
    table = boto3.resource('dynamodb').Table('ll_now')

    # 無効なツイートを見分けるための単語リストをDynamoDBから取得
    primary_key = {"primary": 'invalid_tweet_including'}
    res = table.get_item(Key=primary_key)
    invalid_tweet_including = res['Item']['word']

    flag_valid_text = not (any(map(text.__contains__, invalid_tweet_including)))

    # 無効なツイートソースのリストをDynamoDBから取得
    primary_key = {"primary": 'invalid_source_list'}
    res = table.get_item(Key=primary_key)
    invalid_source_list = res['Item']['source']

    flag_valid_source = True
    pattern = r'<a href="(.*)">(.*)</a>'
    matches = re.finditer(pattern, source)
    for match in matches:
        groups = match.groups()
        source_url = groups[0].split('"')[0]

    if source_url in invalid_source_list:
        flag_valid_source = False

    flag_valid_tweet = flag_valid_text and flag_valid_source

    return flag_valid_tweet
