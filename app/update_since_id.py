import os
import boto3

region = os.environ['AWS_DEFAULT_REGION']
ssm = boto3.client('ssm', region)


def update_since_id(next_since_id, mode):
    key = 'll-now-tweet-since-id-{}'.format(mode)

    try:
        update_ssm_param(key, next_since_id)
    except Exception as e:
        print(e)


def update_ssm_param(key, value):
    ssm.put_parameter(
        Name=key,
        Value=value,
        Overwrite=True
    )
