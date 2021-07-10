import boto3


def update_since_id(next_since_id):
    try:
        table = boto3.resource('dynamodb').Table('ll_now')
        table.update_item(
            Key={'primary': 'fetch_tweet_since_id'},
            UpdateExpression='set id = :i',
            ExpressionAttributeValues={
                ':i': next_since_id
            }
        )

    except Exception as e:
        print(e)
