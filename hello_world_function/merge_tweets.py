def merge_tweets(stored_tweets, new_tweets):
    if stored_tweets is None:
        return new_tweets
    else:
        tweets = new_tweets.extend(stored_tweets)
        return tweets
