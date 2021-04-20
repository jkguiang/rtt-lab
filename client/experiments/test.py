def read_byte_by_byte(input_binary, chunk_size=4):
    with open(input_binary, "rb") as f_in:
        # Read the first chunk of bytes
        byte = f_in.read(chunk_size)
        while byte != b"":
            # Do stuff with this chunk of bytes
            print(byte)
            # Read the next chunk of bytes
            byte = f_in.read(chunk_size)

if __name__ == "__main__":
    read_byte_by_byte("inputs/test.dat", chunk_size=24)
