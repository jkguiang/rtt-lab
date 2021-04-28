# Parse arguments
delay=0
for arg in "$@"; do
    key=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)   
    case "$key" in
        --delay) delay=${val}; shift;;
    esac    
done
# Add delay
tc qdisc add dev eth0 root netem delay ${delay}ms
# Run test
python experiments/simple_test.py ${@}
# Remove delay
tc qdisc del dev eth0 root netem delay ${delay}ms
