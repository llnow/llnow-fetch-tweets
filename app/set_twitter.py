from get_api_key import *
from twitter import *


def set_twitter():
    api_key = get_api_key()
    twitter = Twitter(
        auth=OAuth2(
            bearer_token=api_key['BEARER_TOKEN']
        )
    )

    return twitter
