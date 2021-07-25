def summarize_tweet(tweet):
    tweet_abst = {}
    tweet_abst['created_at'] = tweet['created_at']
    tweet_abst['id'] = tweet['id']
    tweet_abst['id_str'] = tweet['id_str']
    tweet_abst['text'] = tweet['text']
    tweet_abst['entities'] = tweet['entities']

    return tweet_abst
