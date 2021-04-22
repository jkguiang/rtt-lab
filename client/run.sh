experiment=${1}

if [[ "${experiment}" != "" ]]; then
    # Delays will be multiples of 5
    delays_x5ms=$(seq 0 10)
    # Make the outputs directory if it doesn't exist already
    mkdir -p outputs
    # Run tests
    for delay_x5ms in ${delays_x5ms}; do
        delay_ms=$((${delay_x5ms}*5))
        echo "Running ${experiment}.py with a ${delay_ms}ms delay..."
        output_json="${experiment}_${delay_ms}ms.json"
        # Add delay
        tc qdisc add dev eth0 root netem delay ${delay_ms}ms
        # Run test
        python experiments/${experiment}.py \
            --input_file=test.dat \
            --server="172.17.0.2:1094" \
            --output_json="outputs/${output_json}" \
            --chunk_size=4
        # Remove delay
        tc qdisc del dev eth0 root netem delay ${delay_ms}ms
        echo "Done."
    done

else
    echo "Usage: ./run.sh <name of experiment>"
fi
