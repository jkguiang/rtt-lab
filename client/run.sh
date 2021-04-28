# Default values
unittest=false
min_delay=0
max_delay=0
step_size=1
experiment=""
args=""

# Parse arguments
for arg in "$@"; do
    key=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)   
    case "$key" in
        --unittest) unittest=true; break;;
        --min_delay) min_delay=${val};;
        --max_delay) max_delay=${val};;     
        --step_size) step_size=${val};;     
        --experiment) experiment=${val};;
        *) args+="$arg";;
    esac
done

if [[ "$unittest" = true ]]; then
    # Run control
    echo "Running simple_test.py ${args}"
    python experiments/simple_test.py ${args}
    # Add delay
    echo "Adding a 10ms delay..."
    tc qdisc add dev eth0 root netem delay 10ms
    # Run 10ms-delayed test
    echo "Running simple_test.py ${args}"
    python experiments/simple_test.py ${args}
    # Remove delay
    echo "Removing the 10ms delay..."
    tc qdisc del dev eth0 root netem delay 10ms
    echo "Done."
elif [[ -f experiments/${experiment}.py ]]; then
    # Generate list of delays in milliseconds
    delays_ms=$(seq ${min_delay} ${step_size} ${max_delay})
    # Make the outputs directory if it doesn't exist already
    mkdir -p outputs
    mkdir -p outputs/${experiment}
    # Run tests
    for delay_ms in ${delays_ms}; do
        if [[ ${args} != "" ]]; then
            echo "Running ${experiment}.py ${args} with a ${delay_ms}ms delay..."
        else
            echo "Running ${experiment}.py with a ${delay_ms}ms delay..."
        fi
        # Add delay
        tc qdisc add dev eth0 root netem delay ${delay_ms}ms
        # Run test
        output_json="outputs/${experiment}/${experiment}_${delay_ms}ms.json"
        python experiments/${experiment}.py ${args} --output_json=${output_json}
        # Remove delay
        tc qdisc del dev eth0 root netem delay ${delay_ms}ms
        # Compress output
        gzip -f ${output_json}
        echo "Done. Saved report to ${output_json}.gz"
    done
elif [[ ${experiment} != "" ]]; then
    echo "ERROR: experiments/${experiment}.py does not exist!"
else
    echo "usage: ./run.sh --experiment=NAME [OPTIONAL ARGS] [ADDITIONAL ARGS]"
    echo ""
    echo "Run RTT lab experiment under a series of different delays"
    echo ""
    echo "required arguments:"
    echo "  --experiment NAME        Name of experiment (e.g. experiments/foo.py --> foo)"
    echo ""
    echo "optional arguments:"
    echo "  --min_delay MIN DELAY    minimum delay in milliseconds (default: 0)"
    echo "  --max_delay MAX DELAY    maximum delay in milliseconds (default: 0)"
    echo "  --step_size STEP SIZE    step size in going from min to max delay (default: 1)"
    echo ""
    echo "All additional args are passed to the experiment"
fi
