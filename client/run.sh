# Default values
min_delay=0
max_delay=0
step_size=1
experiment=""

# Parse arguments
for arg in "$@"; do
    key=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)   
    case "$key" in
        --min_delay) min_delay=${val}; shift;;
        --max_delay) max_delay=${val}; shift;;     
        --step_size) step_size=${val}; shift;;     
        --experiment) experiment=${val}; shift;;
    esac    
done

# Run experiment
if [[ -f experiments/${experiment}.py ]]; then
    # Generate list of delays in milliseconds
    delays_ms=$(seq ${min_delay} ${step_size} ${max_delay})
    # Make the outputs directory if it doesn't exist already
    mkdir -p outputs
    mkdir -p outputs/${experiment}
    # Run tests
    for delay_ms in ${delays_ms}; do
        if [[ ${@} != "" ]]; then
            echo "Running ${experiment}.py ${@} with a ${delay_ms}ms delay..."
        else
            echo "Running ${experiment}.py with a ${delay_ms}ms delay..."
        fi
        # Add delay
        tc qdisc add dev eth0 root netem delay ${delay_ms}ms
        # Run test
        output_json="outputs/${experiment}/${experiment}_${delay_ms}ms.json"
        python experiments/${experiment}.py ${@} --output_json=${output_json}
        # Remove delay
        tc qdisc del dev eth0 root netem delay ${delay_ms}ms
        # Compress output
        gzip -f ${output_json}
        echo "Done. Saved report to ${output_json}.gz"
    done
elif [[ ${experiment} != "" ]]; then
    echo "ERROR: experiments/${experiment}.py does not exist!"
else
    echo "Usage: ./run.sh --experiment=<name of experiment>"
fi
