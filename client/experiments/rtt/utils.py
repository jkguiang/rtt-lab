import time
import uproot

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

class RTTSource(uproot.source.xrootd.XRootDSource):
    """
    Modified Uproot XRootD source object that writes metadata to a global dict
    (thanks to Nick Amin for writing this class)
    """
    def __init__(self, file_path, **options):
        super().__init__(file_path, **options)
        self.report = {"reads": [], "runtime":-999}

    def chunk(self, start, stop):
        d = dict(which="chunk", start=start, stop=stop, nbytes=stop-start)
        self.report["reads"].append(d)
        return super().chunk(start, stop)

    def chunks(self, ranges, notifications):
        d = dict(which="chunk", ranges=ranges)
        self.report["reads"].append(d)
        return super().chunks(ranges, notifications)