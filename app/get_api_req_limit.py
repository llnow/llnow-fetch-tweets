import requests
from get_api_key import *


def get_api_req_limit():
    user_agent = "Get Twitter Status Application/1.0"
    limit_endpoint = 'https://api.twitter.com/1.1/application/rate_limit_status.json'
    api_key = get_api_key()
    bearer = api_key['BEARER_TOKEN']

    headers = {
        'Authorization': 'Bearer {}'.format(bearer),
        'User-Agent': user_agent
    }
    params = {
        'resources': 'search'
    }

    try:
        res = requests.get(limit_endpoint, headers=headers, params=params, timeout=5.0)
        res.raise_for_status()
    except (TimeoutError, requests.ConnectionError):
        raise requests.ConnectionError("Cannot get Limit Status")
    except Exception:
        raise Exception("Cannot get Limit Status")

    limit = res.json()['resources']['search']['/search/tweets']['remaining']

    return limit
