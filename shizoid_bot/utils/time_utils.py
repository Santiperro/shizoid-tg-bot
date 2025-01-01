import datetime

def format_ttl_flexible(ttl: int) -> str:
    time = datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=ttl)
    if ttl < 3600:
        return time.strftime("%M:%S")
    return time.strftime("%H:%M:%S")