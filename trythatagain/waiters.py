import time


def exp_backoff(i, unit):
    t = i ** 2 * unit
    time.sleep(t)
    return t


def linear_backoff(i, unit):
    t = (i + 1) * unit
    time.sleep(t)
    return t
