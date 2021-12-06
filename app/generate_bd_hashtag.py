import json
from boto3.dynamodb.conditions import Attr
from get_ssm_params import *


def generate_bd_hashtag(mode):
    # 日付をssmパラメータストアから取得
    year, month, day = get_date(mode)

    table = boto3.resource('dynamodb').Table('lovelive-character')
    res = table.scan(
        FilterExpression=Attr('birthmonth').eq(month) & Attr('birthday').eq(day)
    )
    if res['Items']:
        birthday_character = res['Items'][0]['full_name']
        bd_hashtag = '#{}生誕祭{}'.format(birthday_character, year)
    else:
        bd_hashtag = ''

    return bd_hashtag


def get_date(mode):
    key = 'll-now-tweets-features-{}'.format(mode)
    params = get_ssm_params(key)
    tweets_feature = json.loads(params[key])
    until = tweets_feature['latest_tweet_created_at']
    year, month, day = map(int, until.split()[0].split('-'))

    return year, month, day
