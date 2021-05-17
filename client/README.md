# RTT Lab
Only Python tests can be run by `run.sh`, so any non-Python scripts have be run manually. Therefore, the following instructions will only pertain to new Python tests, as any other tests are completely left to the user's discretion.

## Running tests
In order to _run_ any tests, you first need to hop onto the client container (assuming it's already running). This command is given in the main README, but we include it here as well for convenience.
```
docker exec -it rtt-client /bin/bash
```
Once on the container, `run.sh` can be used to access and run any tests in the `experiments` directory. The usage instructions are included here for convenience:
```
usage: ./run.sh --experiment=NAME [OPTIONAL ARGS] [ADDITIONAL ARGS]

Run RTT lab experiment under a series of different delays

required arguments:
  --experiment NAME        Name of experiment (e.g. experiments/foo.py --> foo)

optional arguments:
  -f                       silence any overwrite warnings
  --unittest               run simple_test.py (with any additional args) once with a 0ms delay and
                           again with a 10ms delay
  --min_delay MIN DELAY    minimum delay in milliseconds (default: 0)
  --max_delay MAX DELAY    maximum delay in milliseconds (default: 0)
  --step_size STEP SIZE    step size in going from min to max delay (default: 1)
  --n_reps NUM REPS        number of times that a test should be repeated for a given netem delay
  --tag TAG                unique tag for this run (i.e. output written to outputs/foo_{TAG}/...)

All additional args are passed to the experiment
```
To further illustrate the point, here's an example:
```
./run.sh --experiment=simple_test --tag=chunk1KB_file12KB \ 
         --min_delay=0ms --max_delay=10ms --step_size=2 --n_reps=5 \
         --chunk_size=1000 --input_file=test_12000ints.dat
```
As we see immediately, `--chunk_size` and `--input_file` are not arguments used by `run.sh`, so they will be passed to the test being run, namely `simple_test.py`. Thus, the example above will run `simple_test.py --chunk_size=1000 --input_file=test_12000ints.dat` 25 times, 5 times for each netem delay: 0ms, 2ms, 4ms, 8ms, and 10ms. Then, it will save the output (gzipped JSON files) from each iteration to `outputs/simple_test_chunk1KB_file12KB`, where the outputs are organized by netem delay:
```
outputs/simple_test_chunk1KB_file12KB/
|- 0ms/
|   |- report_1.json.gz
|   |- report_2.json.gz
|   |- ...
|   +- report_5.json.gz
|- 2ms/
|   |- report_1.json.gz
|   |- ...
|   +- report_5.json.gz
...
+- 10ms/
    |- report_1.json.gz
    |- ...
    +- report_5.json.gz
```

## Writing tests
Tests should be consolidated to a single file written to the `experiments` directory. In that file, there should be a single function that runs the relevant code for the test. This function must then be wrapped by the `rtt_test` wrapper, which will enforce the requirement that each test return a dictionary wherein it will write the test's runtime. Lastly, each test should have the following options in its CLI:
1. `--output_json`: path to the output JSON file
2. `--server`: <IP>:<port> of server

These options necessary because they are automatically passed to the test script by `run.sh`. Then, every test should write the report returned by the wrapped main function to the file given by `--output_json`. As mentioned before, additional CLI options that are _not_ used by `run.sh` are passed to the test script such that tests are still configurable from the command line. Lastly, every test must use the XRootD client Python API in order to access the files on the XRootD server. This is included in `uproot`, which is installed in the `rtt-env` conda environment. A wrapper of the XRootD source object is included specifically for RTT tests (cf. [here](https://github.com/jkguiang/rtt-lab/blob/main/client/experiments/rtt/objects.py)). This wrapper writes the bytes (both vector and regular chunks) read for each read to a dictionary that can be accessed as follows:
```python
import rtt
uproot_file = uproot.open("root://172.17.0.2:1094/test.root", xrootd_handler=rtt.objects.RTTSource)
# ... <-- Your code here
report = uproot_file._file._source.report
```
