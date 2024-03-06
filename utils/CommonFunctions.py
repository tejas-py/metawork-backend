import time


# get today second in epoch time
def today_seconds():
    today_time = time.localtime()
    seconds_today_time = time.mktime(today_time)
    return int(seconds_today_time)
