from get_since_id import *
from get_query import *
from get_api_req_limit import *
from check_valid_tweet import *
from summarize_tweet import *
from parse2params import *
from update_since_id import *
import time
import boto3


def fetch_new_tweets(twitter, sleep_sec, max_api_request_force, mode):
    # dynamodbからsince_idを取得
    since_id = get_since_id(mode)

    table = boto3.resource('dynamodb').Table('ll_now')

    # 無効なツイートを見分けるための単語リストをDynamoDBから取得
    primary_key = {"primary": 'invalid_tweet_including'}
    res = table.get_item(Key=primary_key)
    invalid_tweet_including = res['Item']['word']

    # 除外したいユーザを取得
    primary_key = {'primary': 'invalid_user_list'}
    res = table.get_item(Key=primary_key)
    invalid_users = res['Item']['user']

    # 無効なツイートソースのリストをDynamoDBから取得
    primary_key = {"primary": 'invalid_source_list'}
    res = table.get_item(Key=primary_key)
    invalid_source_list = res['Item']['source']

    # クエリを取得
    query = get_query()

    params = {
        'q': query,
        'lang': 'ja',
        'result_type': 'recent',
        'count': 100,
        'since_id': since_id,
        'max_id': None,
        'tweet_mode': 'extended'
    }

    max_api_request_real = get_api_req_limit()
    print('max_api_request: ' + str(max_api_request_real))
    # 手動で定めた上限と実際の上限の小さい方を採用
    max_api_request = min(max_api_request_real, max_api_request_force)

    tweets = []
    for req in range(max_api_request):
        if req != 0 and req % 10 == 0:
            print('{} requested'.format(req))
            # リクエストの間隔を空けるために10回ごとにスリープ
            time.sleep(sleep_sec)

        res = twitter.search.tweets(
            q=params['q'],
            lang=params['lang'],
            result_type=params['result_type'],
            count=params['count'],
            since_id=params['since_id'],
            max_id=params['max_id'],
            tweet_mode=params['tweet_mode']
        )
        fetched_tweets = res['statuses']
        if len(fetched_tweets) == 0:
            break
        for tweet in fetched_tweets:
            if check_valid_tweet(tweet, invalid_tweet_including, invalid_users, invalid_source_list):
                tweet = summarize_tweet(tweet)
                tweets.append(tweet)

        # メタデータを取得
        search_metadata = res['search_metadata']
        # 崩れるので上書き
        search_metadata['query'] = query

        # 次のapiで使うparamsを整形
        next_results = search_metadata['next_results']
        since_id = search_metadata['since_id']
        next_results = next_results.lstrip('?')  # 先頭の?を削除
        params = parse2params(next_results)
        # 崩れるので上書き
        params['q'] = query
        params['since_id'] = since_id
        # next_resultsにないので追加
        params['tweet_mode'] = 'extended'

    if len(tweets) == 0:
        latest_tweet = None
        print('Fetched 0 new Tweet')
    else:
        latest_tweet = tweets[0]
        print('Fetched {} new Tweets'.format(len(tweets)))

    # since_idを更新
    if latest_tweet is not None:
        next_since_id = latest_tweet['id_str']
        update_since_id(next_since_id, mode)

    return tweets, search_metadata
