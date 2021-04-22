import uproot
import argparse
import json
import utils

@utils.rtt_test
def test(file_name, server="172.17.0.2:1094", chunk_size=4, verbose=False):
    # Define connection to XRootD file
    xrd_path = f"root://{server}//{file_name}"
    xrd_resource = uproot.source.xrootd.XRootDResource(xrd_path, timeout=None)
    # Read in chunk-by-chunk
    n_bytes = xrd_resource.num_bytes
    byte_ranges = [(b, min(b+chunk_size, n_bytes)) 
                   for b in range(0, n_bytes, chunk_size)]
    report = {"reads": [], "runtime": -999}
    for start, stop in byte_ranges:
        bytes_in = xrd_resource.get(start=start, stop=stop)
        if verbose:
            print(bytes_in)
        d = dict(which="chunk", start=start, stop=stop, nbytes=stop-start)
        report["reads"].append(d)

    return report

if __name__ == "__main__":
    # CLI
    cli = argparse.ArgumentParser(description="Run RTT Lab unit test")
    cli.add_argument(
        "-c", "--chunk_size", 
        type=int, default=4,
        help="Size (in bytes) of chunks to read"
    )
    cli.add_argument(
        "-i", "--input_file", 
        type=str, required=True,
        help="Name of input file on server"
    )
    cli.add_argument(
        "-o", "--output_json", 
        type=str, default="",
        help="Name of output JSON on client"
    )
    cli.add_argument(
        "-v", "--verbose",
        help="Print verbose output",
        action="store_true",
        default=False
    )
    cli.add_argument(
        "--server", 
        type=str, default="172.17.0.2:1094",
        help="<IP>:<port> of server"
    )

    # Get args
    args = cli.parse_args()
    # Run test
    report = test(
        args.input_file, 
	server=args.server,
        chunk_size=args.chunk_size, 
        verbose=args.verbose
    )
    # Write out report
    if args.output_json:
        with open(args.output_json, "w") as f_out:
            json.dump(report, f_out)
    else:
        print("Runtime: {} seconds".format(report["runtime"]))
