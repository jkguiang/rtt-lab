import uproot

def test(file_name, redirector="172.17.0.2:1094", chunk_size=4):
    # Define connection to XRootD file
    xrd_path = f"root://{redirector}//{file_name}"
    xrd_file = uproot.source.xrootd.XRootDResource(xrd_path, timeout=10)
    # Read in chunk-by-chunk
    n_bytes = xrd_file.num_bytes
    byte_ranges = [(b, min(b+chunk_size, n_bytes)) 
                   for b in range(0, n_bytes, chunk_size)]
    for start, stop in byte_ranges:
        print(xrd_file.get(start=start, stop=stop))

    return

if __name__ == "__main__":
    test("test.dat")
