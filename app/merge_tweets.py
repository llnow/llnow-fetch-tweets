from get_ssm_params import *


def merge_tweets(stored_tweets, new_tweets, n_required_tweets, mode):
    flag_trigger_next_process = False
    # 新しく取得したツイートの数の閾値をssmパラメータストアから取得
    key = 'll-now-threshold-rapid-tweets-increase-{}'.format(mode)
    params = get_ssm_params(key)
    threshold_rapid_tweets_increase = int(params[key])

    if len(new_tweets) >= threshold_rapid_tweets_increase:
        flag_trigger_next_process = True

    if stored_tweets is None:
        tweets = new_tweets
    else:
        tweets = new_tweets + stored_tweets  # new_tweetsとstored_tweetsを連結

    if len(tweets) >= n_required_tweets:
        flag_trigger_next_process = True

    print('{} Tweets are waiting to be processed'.format(len(tweets)))
    if flag_trigger_next_process:
        print('Invoked next process')
    else:
        print("Didn't invoke next process")

    return tweets, flag_trigger_next_process
