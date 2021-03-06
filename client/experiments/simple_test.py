import uproot
import argparse
import time
import json
import rtt

@rtt.wrappers.rtt_test()
def run_simple_test(server="172.17.0.2:1094", input_file="test_1000ints.dat", 
                    chunk_size=4):
    """
    Read the test.dat file on the server chunk-by-chunk using Uproot's XRootD 
    file handler
    """
    # Define connection to XRootD file
    xrd_path = f"root://{server}//{input_file}"
    xrd_resource = uproot.source.xrootd.XRootDResource(xrd_path, timeout=None)
    # Read in chunk-by-chunk
    n_bytes = xrd_resource.num_bytes
    byte_ranges = [(b, min(b+chunk_size, n_bytes)) 
                   for b in range(0, n_bytes, chunk_size)]
    report = {"reads": [], "file": xrd_path}
    for start, stop in byte_ranges:
        d = dict(
            which="chunk", 
            when=time.time(), 
            start=start, 
            stop=stop, 
            nbytes=stop-start
        )
        report["reads"].append(d)
        bytes_in = xrd_resource.get(start=start, stop=stop)

    return report

if __name__ == "__main__":
    # CLI
    cli = argparse.ArgumentParser(description="Run RTT Lab unit test")
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
        type=str, default="test_1000ints.dat",
        help="Path to input file on server"
    )
    cli.add_argument(
        "--chunk_size", 
        type=int, default=4,
        help="Size of chunks to read in"
    )

    # Get args
    args = cli.parse_args()
    # Run test
    report = run_simple_test(
        server=args.server, 
        input_file=args.input_file, 
        chunk_size=args.chunk_size
    )
    # Write out report
    if args.output_json:
        with open(args.output_json, "w") as f_out:
            json.dump(report, f_out)
    else:
        print("Runtime: {} seconds".format(report["runtime"]))
