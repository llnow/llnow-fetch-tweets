from get_since_id import *
from get_query import *
from check_valid_tweet import *
from summarize_tweet import *
from parse2params import *
from update_since_id import *
import time
import boto3


def fetch_new_tweets(twitter, sleep_sec, max_api_request_force):
    # dynamodbからsince_idを取得
    since_id = get_since_id()

    table = boto3.resource('dynamodb').Table('ll_now')

    # 無効なツイートを見分けるための単語リストをDynamoDBから取得
    primary_key = {"primary": 'invalid_tweet_including'}
    res = table.get_item(Key=primary_key)
    invalid_tweet_including = res['Item']['word']

    # 無効なツイートソースのリストをDynamoDBから取得
    primary_key = {"primary": 'invalid_source_list'}
    res = table.get_item(Key=primary_key)
    invalid_source_list = res['Item']['source']

    # クエリを取得
    query = get_query()

    url_search = 'https://api.twitter.com/1.1/search/tweets.json'
    url_limit = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    params = {
        'q': query,
        'lang': 'ja',
        'result_type': 'recent',
        'count': 100,
        'since_id': since_id
    }
    res = twitter.get(url_limit)
    contents = res.json()
    max_api_request_real = contents['resources']['search']['/search/tweets']['remaining']
    print('max_api_request: ' + str(max_api_request_real))
    # 手動で定めた上限と実際の上限の小さい方を採用
    max_api_request = min(max_api_request_real, max_api_request_force)

    tweets = []
    for req in range(max_api_request):
        if req != 0 and req % 10 == 0:
            print('{} requested'.format(req))
            # リクエストの間隔を空けるために10回ごとにスリープ
            time.sleep(sleep_sec)

        res = twitter.get(url_search, params=params)
        contents = res.json()
        fetched_tweets = contents['statuses']
        if len(fetched_tweets) == 0:
            break
        for tweet in fetched_tweets:
            if check_valid_tweet(tweet, invalid_tweet_including, invalid_source_list):
                tweet = summarize_tweet(tweet)
                tweets.append(tweet)
        search_metadata = contents['search_metadata']
        next_results = search_metadata['next_results']
        since_id = search_metadata['since_id']
        next_results = next_results.lstrip('?')  # 先頭の?を削除
        params = parse2params(next_results)
        # 崩れるので上書き
        params['q'] = query
        params['since_id'] = since_id

    if len(tweets) == 0:
        latest_tweet = None
    else:
        latest_tweet = tweets[0]

    # since_idを更新
    if latest_tweet is not None:
        next_since_id = latest_tweet['id_str']
        update_since_id(next_since_id)

    return tweets
