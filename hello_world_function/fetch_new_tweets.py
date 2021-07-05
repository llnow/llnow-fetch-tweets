from check_valid_tweet import *
from parse2params import *
import boto3

BUCKET_NAME = 'll-now-material'


def fetch_new_tweets(twitter):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(BUCKET_NAME)

    # s3からsince_id.txtをダウンロード
    text_path = '/tmp/since_id.txt'
    bucket.download_file('tmp/since_id.txt', text_path)

    # since_idを取得
    with open(text_path, 'r') as f:
        since_id = f.read()

    url_search = 'https://api.twitter.com/1.1/search/tweets.json'
    url_limit = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    params = {
        'q': '#lovelive -filter:retweets -filter:replies',
        'lang': 'ja',
        'result_type': 'recent',
        'count': 100,
        'since_id': since_id
    }
    res = twitter.get(url_limit)
    contents = res.json()
    max_api_request = contents['resources']['search']['/search/tweets']['remaining']
    print('max_api_request: ' + str(max_api_request))
    tweets = []
    for req in range(max_api_request):
        if req != 0 and req % 10 == 0:
            print('{} requested'.format(req))
        res = twitter.get(url_search, params=params)
        contents = res.json()
        fetched_tweets = contents['statuses']
        if len(fetched_tweets) == 0:
            break
        for tweet in fetched_tweets:
            if check_valid_tweet(tweet):
                tweets.append(tweet)
        search_metadata = contents['search_metadata']
        next_results = search_metadata['next_results']
        since_id = search_metadata['since_id']
        next_results = next_results.lstrip('?')  # 先頭の?を削除
        params = parse2params(next_results)
        # 崩れるので上書き
        params['q'] = '#lovelive -filter:retweets -filter:replies'
        params['since_id'] = since_id

    if len(tweets) == 0:
        latest_tweet = None
    else:
        latest_tweet = tweets[0]

    # since_idを更新
    if latest_tweet is not None:
        updated_since_id = latest_tweet['id_str']
        obj = s3.Object(BUCKET_NAME, 'tmp/since_id.txt')
        obj.put(Body=updated_since_id)

    return tweets
