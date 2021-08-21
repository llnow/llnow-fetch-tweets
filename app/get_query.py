import boto3
from boto3.dynamodb.conditions import Key
from check_datetime_in_range import *


def get_query():
    table_ll_now = boto3.resource('dynamodb').Table('ll_now')
    table_ll_now_search_keyword = boto3.resource('dynamodb').Table('ll-now-search-keyword')

    # 検索キーワードを取得
    # default_keywordsを取得
    res = table_ll_now_search_keyword.query(
        KeyConditionExpression=Key('type').eq('default')
    )
    default_keywords = [d['keyword'] for d in res['Items']]

    # option_keywordsを取得
    res = table_ll_now_search_keyword.query(
        KeyConditionExpression=Key('type').eq('option')
    )
    option_keywords = []
    option_list = res['Items']
    for option in option_list:
        kw = option['keyword']
        since_str = option['since']
        until_str = option['until']
        if check_datetime_in_range(since_str, until_str):
            option_keywords.append(kw)

    keywords = default_keywords + option_keywords
    print('keywords:{}'.format(keywords))

    # 検索フィルターを取得
    primary_key = {'primary': 'search_filter'}
    res = table_ll_now.get_item(Key=primary_key)
    filters = res['Item']['filter']

    # 除外したいユーザを取得
    primary_key = {'primary': 'invalid_user_list'}
    res = table_ll_now.get_item(Key=primary_key)
    users = res['Item']['user']

    # queryを生成
    query = ' OR '.join(keywords)
    for f in filters:
        query += ' -filter:' + f
    for user in users:
        query += ' -from:' + user

    return query
