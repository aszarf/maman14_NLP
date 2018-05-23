import time

def timelog():
    if 'tm' not in timelog.__dict__:
        timelog.tm = time.time()
    t = time.time() - timelog.tm
    timelog.tm = time.time()
    return t
