from get_ssm_params import *


def merge_tweets(stored_tweets, new_tweets, search_metadata, n_required_tweets, mode):
    flag_trigger_next_process = False
    # 新しく取得したツイートの数の閾値をssmパラメータストアから取得
    key = 'll-now-threshold-rapid-tweets-increase-{}'.format(mode)
    params = get_ssm_params(key)
    threshold_rapid_tweets_increase = int(params[key])

    if len(new_tweets) >= threshold_rapid_tweets_increase:
        flag_trigger_next_process = True

    # 必要ならstored_tweetsとnew_tweetsを連結
    if stored_tweets is None:
        tweets = new_tweets
    else:
        tweets = new_tweets + stored_tweets

    if len(tweets) >= n_required_tweets:
        flag_trigger_next_process = True

    print('{} Tweets are waiting to be processed'.format(len(tweets)))
    if flag_trigger_next_process:
        print('Invoke next process')
    else:
        print("Don't invoke next process")

    # ツイートにメタデータを結合し，s3に出力する形に整形
    res = form_res(tweets, search_metadata)

    return res, flag_trigger_next_process


def form_res(tweets, search_metadata):
    res = {
        'statuses': tweets,
        'search_metadata': search_metadata
    }

    return res
