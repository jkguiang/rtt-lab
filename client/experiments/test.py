import uproot
from argparse import ArgumentParser, RawTextHelpFormatter

def test(file_name, redirector="172.17.0.2:1094", chunk_size=4, verbose=False):
    # Define connection to XRootD file
    xrd_path = f"root://{redirector}//{file_name}"
    xrd_file = uproot.source.xrootd.XRootDResource(xrd_path, timeout=10)
    # Read in chunk-by-chunk
    n_bytes = xrd_file.num_bytes
    byte_ranges = [(b, min(b+chunk_size, n_bytes)) 
                   for b in range(0, n_bytes, chunk_size)]
    bytes_read = []
    for start, stop in byte_ranges:
        bytes_in = xrd_file.get(start=start, stop=stop)
        if verbose:
            print(byes_in)
        bytes_read.append(bytes_in)

    return

if __name__ == "__main__":
    test("test.dat")
    # CLI
    cli = ArgumentParser(description="Run RTT Lab unit test",
                               formatter_class=RawTextHelpFormatter)
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
        "-v", "--verbose",
        help="Print verbose output",
        action="store_true",
        default=False
    )

    # Get args
    args = cli.parse_args()
    test(args.input_file, chunk_size=args.chunk_size, verbose=args.verbose)
