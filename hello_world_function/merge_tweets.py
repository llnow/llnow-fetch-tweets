def merge_tweets(stored_tweets, new_tweets):
    if stored_tweets is None:
        return new_tweets
    else:
        return stored_tweets + new_tweets
