import time

def delayMSPositive(ms):
    start = time.perf_counter_ns()
    while time.perf_counter_ns() - start < ms * 1000000:
        pass

def delayMSNegative(ms):
    time.sleep(ms/1000)