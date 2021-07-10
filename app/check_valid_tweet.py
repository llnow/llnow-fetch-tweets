import boto3


def check_valid_tweet(tweet):
    text = tweet['text']
    table = boto3.resource('dynamodb').Table('ll_now')

    # 無効なツイートを見分けるための単語リストをDynamoDBから取得
    primary_key = {"primary": 'invalid_tweet_including'}
    res = table.get_item(Key=primary_key)
    invalid_tweet_including = res['Item']['word']

    return not(any(map(text.__contains__, invalid_tweet_including)))
