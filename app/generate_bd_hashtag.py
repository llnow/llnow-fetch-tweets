import json
from datetime import datetime, timedelta, timezone
from boto3.dynamodb.conditions import Attr
from get_ssm_params import *


def generate_bd_hashtag():
    # 今日の日付を取得
    year, month, day = get_today()

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


def get_today():
    jst = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(jst)

    return now.year, now.month, now.day
