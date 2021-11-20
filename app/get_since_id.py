import os
import boto3

region = os.environ['AWS_DEFAULT_REGION']
ssm = boto3.client('ssm', region)


def get_since_id(mode):
    key = 'll-now-tweet-since-id-{}'.format(mode)

    try:
        params = get_ssm_params(key)
        since_id = params[key]

        return since_id

    except Exception as e:
        print(e)


def get_ssm_params(*keys):
    response = ssm.get_parameters(
        Names=keys
    )
    params = {}
    for p in response['Parameters']:
        params[p['Name']] = p['Value']

    return params
