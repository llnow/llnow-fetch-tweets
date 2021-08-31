import datetime as dt
import time
import pytz


def generate_archive_filename(tweets):
    until = utc2jst(tweets[0]['created_at'])
    since = utc2jst(tweets[-1]['created_at'])
    filename = 'tweets_{}_{}.json'.format(since, until)

    return filename


def utc2jst(utc):
    # time.struct_timeに変換
    st = time.strptime(utc, '%a %b %d %H:%M:%S +0000 %Y')
    # datetimeに変換(timezoneを付与)
    utc_time = dt.datetime(st.tm_year, st.tm_mon, st.tm_mday,
                           st.tm_hour, st.tm_min, st.tm_sec, tzinfo=dt.timezone.utc)
    # 日本時間に変換
    jst_time = utc_time.astimezone(pytz.timezone("Asia/Tokyo"))
    # フォーマットを変換
    jst_time_str = jst_time.strftime("%Y%m%d%H%M%S")

    return jst_time_str
