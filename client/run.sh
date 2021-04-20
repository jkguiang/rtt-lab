delay_ms=${1}

# Add delay
tc qdisc add dev eth0 root netem delay ${1}ms

# Run test
start_utc_ns=$(date +%s%N)
python experiments/test.py --input_file=test.dat --chunk_size=4
end_utc_ns=$(date +%s%N)

# Print runtime
runtime="$((${end_utc_ns} - ${start_utc_ns}))"
echo "${runtime} nanoseconds"

# Remove delay
tc qdisc del dev eth0 root netem delay ${1}ms