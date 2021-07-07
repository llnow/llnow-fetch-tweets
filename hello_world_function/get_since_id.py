import boto3


def get_since_id():
    try:
        table = boto3.resource('dynamodb').Table('ll_now')
        primary_key = {'primary': 'fetch_tweet_since_id'}
        res = table.get_item(Key=primary_key)
        since_id = res['Item']['id']

        return since_id

    except Exception as e:
        print(e)
