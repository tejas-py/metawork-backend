import time


# get today second in epoch time
def today_seconds():
    today_time = time.localtime()
    seconds_today_time = time.mktime(today_time)
    return int(seconds_today_time)


def epoch_to_time(epoch_time):
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    return str_time
