import uproot
import argparse
import json
import rtt

@rtt.wrappers.rtt_test()
def run_root_test(server="172.17.0.2:1094", input_file="test.root", verbose=False):
    """
    Read all of the branches from the test.root file on the server using a modified 
    Uproot XRootD source object
    (thanks to Nick Amin for writing this test)
    """
    # Define connection to XRootD file
    xrd_path = f"root://{server}//{input_file}"
    # Grab the file and read in the ttree object
    uproot_file = uproot.open(xrd_path, xrootd_handler=rtt.objects.RTTSource)
    ttree = uproot_file["tree"]
    # Read all of the branches from this ttree
    floats = ttree["float"].array()
    integers = ttree["integer"].array()
    booleans = ttree["boolean"].array()
    return uproot_file._file._source.report

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
    cli.add_argument(
        "--input_file", 
        type=str, default="test.root",
        help="Path to input file on server"
    )

    # Get args
    args = cli.parse_args()
    # Run test
    report = run_root_test(
        server=args.server, 
        input_file=args.input_file,
        verbose=args.verbose
    )
    # Write out report
    if args.output_json:
        with open(args.output_json, "w") as f_out:
            json.dump(report, f_out)
    else:
        print("Runtime: {} seconds".format(report["runtime"]))
