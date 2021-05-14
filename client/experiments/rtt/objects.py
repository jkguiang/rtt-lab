import uproot

class RTTSource(uproot.source.xrootd.XRootDSource):
    """
    Modified Uproot XRootD source object that writes metadata to a global dict
    (thanks to Nick Amin for writing this class)
    """
    def __init__(self, file_path, **options):
        super().__init__(file_path, **options)
        self.report = {"reads": [], "file": file_path}

    def chunk(self, start, stop):
        d = dict(which="chunk", start=start, stop=stop, nbytes=stop-start)
        self.report["reads"].append(d)
        return super().chunk(start, stop)

    def chunks(self, ranges, notifications):
        d = dict(which="chunks", ranges=ranges)
        self.report["reads"].append(d)
        return super().chunks(ranges, notifications)
