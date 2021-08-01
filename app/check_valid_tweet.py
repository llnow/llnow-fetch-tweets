import re


def check_valid_tweet(tweet, invalid_tweet_including, invalid_source_list):
    text = tweet['text']
    source = tweet['source']
    hashtags = tweet['entities']['hashtags']

    flag_valid_text = not (any(map(text.__contains__, invalid_tweet_including)))

    flag_valid_source = True
    pattern = r'<a href="(.*)">(.*)</a>'
    matches = re.finditer(pattern, source)
    for match in matches:
        groups = match.groups()
        source_url = groups[0].split('"')[0]

    if source_url in invalid_source_list:
        flag_valid_source = False

    # ハッシュタグの数が閾値より多いツイートを無効とみなす
    n_hashtags = len(hashtags)
    if n_hashtags <= 7:
        flag_valid_hashtags = True
    else:
        flag_valid_hashtags = False

    flag_valid_tweet = flag_valid_text and flag_valid_source and flag_valid_hashtags

    return flag_valid_tweet
