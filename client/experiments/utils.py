import time

def rtt_test(func):
    """
    Wrapper for an arbitrary RTT test function that adds the runtime to the report 
    that it produces
    (NOTE: RTT test function MUST return a dict!)
    """
    def wrapper(*args, **kwargs):
        t0 = time.time()
        report = func(*args, **kwargs)
        t1 = time.time()
        report["runtime"] = t1 - t0
        return report

    return wrapper
