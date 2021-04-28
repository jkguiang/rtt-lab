import time

class rtt_test:
    """
    Wrapper for an arbitrary RTT test function that adds the runtime to the report 
    that it produces
    (NOTE: RTT test function MUST return a dict!)
    """
    def __init__(self, multiple_files=False):
        self.multiple_files=multiple_files

    def __call__(self, func):
        if self.multiple_files:
            def wrapped_func(*args, **kwargs):
                report = {"file_reports": [], "runtime": -999}
                t0 = time.time()
                report["file_reports"] = func(*args, **kwargs)
                t1 = time.time()
                report["runtime"] = t1 - t0
                return report
        else:
            def wrapped_func(*args, **kwargs):
                t0 = time.time()
                report = func(*args, **kwargs)
                t1 = time.time()
                report["runtime"] = t1 - t0
                return report

        return wrapped_func
