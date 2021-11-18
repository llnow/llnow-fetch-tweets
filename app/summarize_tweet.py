def summarize_tweet(tweet):
    tweet_abst = {}
    tweet_abst['created_at'] = tweet['created_at']
    tweet_abst['id'] = tweet['id']
    tweet_abst['id_str'] = tweet['id_str']
    tweet_abst['text'] = tweet['full_text']
    tweet_abst['entities'] = {}
    tweet_abst['entities']['hashtags'] = tweet['entities']['hashtags']
    tweet_abst['entities']['urls'] = tweet['entities']['urls']
    tweet_abst['user'] = {}
    tweet_abst['user']['id'] = tweet['user']['id']
    tweet_abst['user']['name'] = tweet['user']['name']
    tweet_abst['user']['screen_name'] = tweet['user']['screen_name']

    return tweet_abst
