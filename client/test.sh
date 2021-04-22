# Add delay
tc qdisc add dev eth0 root netem delay ${1}ms
# Run test
python experiments/simple_test.py --server="172.17.0.2:1094"
# Remove delay
tc qdisc del dev eth0 root netem delay ${1}ms
