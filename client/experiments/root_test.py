import uproot
import argparse
import json
import utils

REPORT = {"reads": [], "runtime":-999}

class RTTSource(uproot.source.xrootd.XRootDSource):
    """
    Modified Uproot XRootD source object that writes metadata to a global dict
    (thanks to Nick Amin for writing this class)
    """
    def __init__(self, file_path, **options):
        super().__init__(file_path, **options)

    def chunk(self, start, stop):
        global REPORT
        d = dict(which="chunk", start=start, stop=stop, nbytes=stop-start)
        REPORT["reads"].append(d)
        return super().chunk(start, stop)

    def chunks(self, ranges, notifications):
        global REPORT
        d = dict(which="chunk", ranges=ranges)
        REPORT["reads"].append(d)
        return super().chunks(ranges, notifications)

@utils.rtt_test
def run_root_test(server="172.17.0.2:1094", verbose=False):
    """
    Read all of the branches from the test.root file on the server using a modified 
    Uproot XRootD source object
    (thanks to Nick Amin for writing this test)
    """
    global REPORT
    # Define connection to XRootD file
    xrd_path = f"root://{server}//test.root"
    uproot_file = uproot.open(xrd_path, xrootd_handler=RTTSource)
    ttree = uproot_file["tree"]
    floats = ttree["float"].array()
    integers = ttree["integer"].array()
    booleans = ttree["boolean"].array()
    return REPORT

if __name__ == "__main__":
    # CLI
    cli = argparse.ArgumentParser(description="Run RTT Lab unit test")
    cli.add_argument(
        "-v", "--verbose",
        action="store_true", default=False,
        help="Print verbose output"
    )
    cli.add_argument(
        "-o", "--output_json", 
        type=str, default="",
        help="Name of output JSON on client"
    )
    cli.add_argument(
        "--server", 
        type=str, default="172.17.0.2:1094",
        help="<IP>:<port> of server"
    )

    # Get args
    args = cli.parse_args()
    # Run test
    report = run_root_test(server=args.server, verbose=args.verbose)
    # Write out report
    if args.output_json:
        with open(args.output_json, "w") as f_out:
            json.dump(report, f_out)
    else:
        print("Runtime: {} seconds".format(report["runtime"]))
