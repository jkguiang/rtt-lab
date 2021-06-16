import uproot
import time

class RTTSource(uproot.source.xrootd.XRootDSource):
    """
    Modified Uproot XRootD source object that writes metadata to a global dict
    (thanks to Nick Amin for writing this class)
    """
    def __init__(self, file_path, **options):
        super().__init__(file_path, **options)
        self.report = {"reads": [], "file": file_path}

    def chunk(self, start, stop):
        read_report = dict(
            which="chunk", 
            range=[start, stop],
            nbytes=stop-start
        )
        read_report["start"] = time.time()
        result = super().chunk(start, stop)
        read_report["stop"] = time.time()
        self.report["reads"].append(read_report)
        return result

    def chunks(self, ranges, notifications):
        read_report = dict(
            which="chunks", 
            ranges=ranges, 
            nbytes=sum([abs(r[1] - r[0]) for r in ranges])
        )
        read_report["start"] = time.time()
        result = super().chunks(ranges, notifications)
        read_report["stop"] = time.time()
        self.report["reads"].append(read_report)
        return result
