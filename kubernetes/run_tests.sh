#!/bin/bash

print_help() {
    echo "usage: ./run_tests.sh --server=IP:PORT --location=LOCATION"
    echo ""
    echo "Run RTT tests on client pod"
    echo ""
    echo "required arguments:"
    echo "  --server IP:PORT         IP:port of server pod"
    echo "  --location LOCATION      Geographic location of the client pod (e.g. new-york)"
    echo ""
    echo "optional arguments:"
    echo "  -h                       display this message"
}

server=""
location=""

# Parse arguments
for arg in "$@"; do
    key=$(echo $arg | cut -f1 -d=)
    val=$(echo $arg | cut -f2 -d=)   
    case "$key" in
        -h) print_help; exit 0;;
        --server) server=${val};;
        --location) location=${val};;     
    esac
done

# Set up
tar -zxvf client.tar.gz
cd client
source /root/miniconda3/etc/profile.d/conda.sh
conda activate rtt-env

if [[ "${server}" != "" && "${location}" != "" ]]; then
    # Run ROOT test
    ./run.sh --experiment=root_test --server=${server} --delays=0 --n_reps=10
    # Run simple tests
    ./run.sh --experiment=simple_test --tag=chunk4B_file1KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=4 --input_file=test_1000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk1KB_file12KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=1000 --input_file=test_12000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk4KB_file12KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=4000 --input_file=test_12000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk8KB_file48KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=8000 --input_file=test_48000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk16KB_file48KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=16000 --input_file=test_48000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk24KB_file48KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=24000 --input_file=test_48000ints.dat
    ./run.sh --experiment=simple_test --tag=chunk48KB_file48KB \
             --server=${server} --delays=0 --n_reps=10 \
             --chunk_size=48000 --input_file=test_48000ints.dat
    # Run Hgg tests
    ./run.sh --experiment=hgg_test \
             --server=${server} --delays=0 --n_reps=10 \
             --nCores 1 --selections "HHggbb_boosted_Presel" --debug 1 \
             --options "experiments/hgg/data/boosted_ggbb.json" \
             --samples "experiments/hgg/data/sample_and_scale1fb.json" \
             --output_tag "test"
    ./run.sh --experiment=hgg_test --tag=multifile \
             --server=${server} --delays=0 --n_reps=10 \
             --nCores 1 --selections "HHggbb_boosted_Presel" --debug 1 \
             --options "experiments/hgg/data/boosted_ggbb.json" \
             --samples "experiments/hgg/data/samples_and_scale1fb.json" \
             --output_tag "test"
    # Tar up the output
    tar -zcvf ${location}.tar.gz outputs/
    # Send output to server
    xrdcp -f ${location}.tar.gz root://${server}//${location}.tar.gz
else
    print_help
fi
