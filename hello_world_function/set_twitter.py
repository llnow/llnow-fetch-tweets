from get_api_key import *
from requests_oauthlib import OAuth1Session


def set_twitter():
    api_key = get_api_key()
    twitter = OAuth1Session(
        api_key['CONSUMER_KEY'],
        api_key['CONSUMER_SECRET'],
        api_key['ACCESS_TOKEN'],
        api_key['ACCESS_TOKEN_SECRET']
    )

    return twitter
