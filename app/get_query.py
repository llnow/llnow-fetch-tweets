import boto3


def get_query():
    table = boto3.resource('dynamodb').Table('ll_now')

    # 検索キーワードを取得
    primary_key = {'primary': 'search_keyword'}
    res = table.get_item(Key=primary_key)
    keywords = res['Item']['keyword']
    # 検索フィルターを取得
    primary_key = {'primary': 'search_filter'}
    res = table.get_item(Key=primary_key)
    filters = res['Item']['filter']
    # 除外したいユーザを取得
    primary_key = {'primary': 'invalid_user_list'}
    res = table.get_item(Key=primary_key)
    users = res['Item']['user']

    query = ''
    for keyword in keywords:
        if not query:
            query += keyword
        else:
            query += ' OR ' + keyword

    for f in filters:
        query += ' -filter:' + f
    for user in users:
        query += ' -from:' + user

    return query
