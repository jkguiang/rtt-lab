experiment=${1}

if [[ "${experiment}" != "" ]]; then
    # Delays will be multiples of 5
    delays_x5ms=$(seq 0 10)
    # Make the outputs directory if it doesn't exist already
    mkdir -p outputs
    mkdir -p outputs/${experiment}
    # Run tests
    for delay_x5ms in ${delays_x5ms}; do
        delay_ms=$((${delay_x5ms}*5))
        echo "Running ${experiment}.py with a ${delay_ms}ms delay..."
        output_json="outputs/${experiment}/${experiment}_${delay_ms}ms.json"
        # Add delay
        tc qdisc add dev eth0 root netem delay ${delay_ms}ms
        # Run test
        python experiments/${experiment}.py \
            --server="172.17.0.2:1094" \
            --output_json=${output_json}
        # Remove delay
        tc qdisc del dev eth0 root netem delay ${delay_ms}ms
        # Compress output
        gzip -f ${output_json}
        echo "Done."
    done
else
    echo "Usage: ./run.sh <name of experiment>"
fi
