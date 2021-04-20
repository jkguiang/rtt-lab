delays_x5ms=$(seq 0 10)

mkdir -p outputs

for delay_x5ms in ${delays_x5ms}; do
    delay_ms=$((${delay_x5ms}*5))
    echo "Running with a ${delay_ms}ms delay..."
    output_json="test_${delay_ms}ms.json"
    # Add delay
    tc qdisc add dev eth0 root netem delay ${delay_ms}ms
    # Run test
    python experiments/test.py \
        --input_file=test.dat \
        --output_json="outputs/${output_json}" \
        --chunk_size=4
    # Remove delay
    tc qdisc del dev eth0 root netem delay ${delay_ms}ms
    echo "Done."
done
