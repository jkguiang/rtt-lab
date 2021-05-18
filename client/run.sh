#!/bin/bash

print_help() {
    echo "usage: ./run.sh --experiment=NAME [OPTIONAL ARGS] [ADDITIONAL ARGS]"
    echo ""
    echo "Run RTT lab experiment under a series of different delays"
    echo ""
    echo "required arguments:"
    echo "  --experiment NAME        Name of experiment (e.g. experiments/foo.py --> foo)"
    echo ""
    echo "optional arguments:"
    echo "  -h                       display this message"
    echo "  -f                       silence any overwrite warnings"
    echo "  --unittest               run simple_test.py (with any additional args) once"
    echo "                           with a 0ms delay and again with a 10ms delay"
    echo "  --delays DELAYS          comma-separated list of delays in ms (e.g. 1,2,3,4)"
    echo "  --min_delay MIN DELAY    minimum delay in ms (default: 0)"
    echo "  --max_delay MAX DELAY    maximum delay in ms (default: 0)"
    echo "  --step_size STEP SIZE    step size in going from min to max delay (default: 1)"
    echo "  --n_reps NUM REPS        number of times that a test should be repeated for"
    echo "                           a given netem delay (default: 1)"
    echo "  --tag TAG                unique tag for this run, such that output is written"
    echo "                           to outputs/foo_{TAG}/ (default: '')"
    echo ""
    echo "All additional args are passed to the experiment"
}

# Default values
need_help=false
use_force=false
unittest=false
delays_ms=""
min_delay=0
max_delay=0
step_size=1
n_reps=1
experiment=""
tag=""
args=""

# Parse arguments
for arg in "$@"; do
    key=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)   
    case "$key" in
        -h) need_help=true;;
        -f) use_force=true;;
        --unittest) unittest=true;;
        --delays) 
            ORIG_IFS=${IFS}; IFS=","; read -a delays_ms <<< "${val}"; 
            IFS=${ORIG_IFS};;
        --min_delay) min_delay=${val};;
        --max_delay) max_delay=${val};;     
        --step_size) step_size=${val};;     
        --n_reps) n_reps=${val};;
        --experiment) experiment=${val};;
        --tag) tag="_${val}";;
        *) if [[ "${args}" == "" ]]; then args+="$arg"; else args+=" $arg"; fi;;
    esac
done
# Remove all previously set rules
tc qdisc del dev eth0 root > /dev/null 2>&1

if [[ ${need_help} = true ]]; then
    print_help
elif [[ ${unittest} = true ]]; then
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
    if [[ "${delays_ms}" == "" ]]; then
        delays_ms=$(seq ${min_delay} ${step_size} ${max_delay})
    fi
    # Make the outputs directory if it doesn't exist already
    mkdir -p outputs
    # Safeguard against accidental overwriting
    output_dir=outputs/${experiment}${tag}
    while [[ -d ${output_dir} && ${use_force} = false ]]; do
        echo "Warning: this could may overwrite files in ${output_dir}"
        read -p "Replace current tag? (y/n/abort): " resp
        if [[ ${resp} == [yY] ]]; then
            read -p "Please enter a new or different tag: " new_tag
            if [[ "${new_tag}" != "" ]]; then
                output_dir=outputs/${experiment}_${new_tag}
                echo "Writing to ${output_dir} instead"
            fi
        elif [[ ${resp} == [nN] ]]; then
            break
        elif [[ "${resp}" == "abort" ]]; then
            exit 0
        fi
    done
    # Make directory for this experiment's outputs
    mkdir -p ${output_dir}
    # Run tests
    for delay_ms in ${delays_ms[@]}; do
        ms_output_dir=${output_dir}/${delay_ms}ms
        mkdir -p ${ms_output_dir}
        for rep in $(seq 1 ${n_reps}); do
            if [[ ${args} != "" ]]; then
                echo "Running ${experiment}.py ${args} with a ${delay_ms}ms delay..."
            else
                echo "Running ${experiment}.py with a ${delay_ms}ms delay..."
            fi
            # Add delay
            if (( $(echo "${delay_ms} > 0." | bc -l) )); then
                tc qdisc add dev eth0 root netem delay ${delay_ms}ms
            fi
            # Run test
            output_json="${ms_output_dir}/report_${rep}.json"
            python experiments/${experiment}.py ${args} --output_json=${output_json}
            # Remove delay
            if (( $(echo "${delay_ms} > 0." | bc -l) )); then
                tc qdisc del dev eth0 root netem delay ${delay_ms}ms
            fi
            # Compress output
            gzip -f ${output_json}
            echo "Done. Saved report to ${output_json}.gz"
        done
    done
elif [[ ${experiment} != "" ]]; then
    echo "ERROR: experiments/${experiment}.py does not exist!"
else
    print_help
fi
