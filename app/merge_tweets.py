def merge_tweets(stored_tweets, new_tweets):
    if stored_tweets is None:
        return new_tweets
    else:
        new_tweets.extend(stored_tweets)  # new_tweetsにstored_tweetsを連結
        return new_tweets
