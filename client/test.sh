delay_ms=${1}

# Add delay
tc qdisc add dev eth0 root netem delay ${1}ms

# Run test
python experiments/test.py \
    --input_file=test.dat \
    --server="172.17.0.2:1094" \
    --chunk_size=4

# Remove delay
tc qdisc del dev eth0 root netem delay ${1}ms
