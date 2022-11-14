import datetime

def getMilliseconds(elaps):
    if (elaps==0):
        return 0
    return int(elaps / datetime.timedelta(milliseconds=1))