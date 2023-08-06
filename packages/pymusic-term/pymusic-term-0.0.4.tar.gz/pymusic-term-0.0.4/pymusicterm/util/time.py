def milliseconds_to_seconds(milliseconds:int) -> int:
    return int((milliseconds/1000)%60)

def milliseconds_to_minutes(milliseconds:int) -> int:
    return int((milliseconds/(1000*60))%60)

def seconds_to_milliseconds(seconds:float) -> int:
    return int(round(seconds,2)*1000)
