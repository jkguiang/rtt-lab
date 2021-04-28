# RTT Lab
This is a virtual "laboratory" for testing the effect of Round Trip Times (RTT) on NanoAOD read latency. Established in 2021 for an [EXPAND](https://center.ucsd.edu/programs/EXPAND.html) project.

## Setup
1. Download Docker (i.e. [here](https://docs.docker.com/docker-for-mac/install/) for MacOS users)
2. Clone this repository
```
$ git clone https://github.com/jkguiang/rtt-lab.git
$ cd rtt-lab
```
3. Build the server Docker Image
```
rtt-lab $ cd server
rtt-lab/server $ docker build -t rtt-server .
```
4. Run a Docker container using the `rtt-server` image
      - `-td` keeps the container running (detatched)
      - `-v ...` mounts the inputs directory to the container with read/write privileges such that the server can serve those files
      - `--name=rtt-server` gives the container a human-readable name
```
rtt-lab/server $ docker run -td -v $PWD/inputs:/data --user=root --name=rtt-server rtt-server
```
5. Check the server information
      - if you changed the name of the server container, you will need to edit `inspect.py` to reflect this before running
      - the server should run at `172.17.0.X:1094`, where `X` can fluctuate depending on your machine (it also can change if you stop and re-run the container)
```
rtt-lab/server $ python inspect.py
Successfully inspected rtt-server
    Port: 1094
    IP Address: 172.17.0.2
    XRootD URL: root://172.17.0.2:1094//<file name>
```
6. Build the client Docker Image
```
$ cd ../client
rtt-lab/client $ docker build -t rtt-client .
```
7. Run a Docker container using the `rtt-client` image
      - `-td` keeps the container running (detatched)
      - `-v ...` mounts the project directory (should be your current working directory) to the container with read/write privileges
      - `--cap-add=NET_ADMIN` allows the container to modify network properties (i.e. use the tool for adding artificial network delay)
      - `--name=rtt-client` gives the container a human-readable name
```
rtt-lab/client $ docker run -td -v $PWD:/home/$(basename $PWD) --user=root --cap-add=NET_ADMIN --name=rtt-client rtt-client
```
8. Use the client container interactively (or modify the Dockerfile) to run your tests.
```
rtt-lab/client $ docker exec -it rtt-client /bin/bash
```

## Running the Unit Test
1. Use the client container interactively
```
$ docker exec -it rtt-client /bin/bash
```
2. Navigate to the `client` directory (this is a *shared area* between your machine and the container!)
```
[root@blah home]# cd client
```
3. Activate the conda environment
```
[root@blah client]# conda activate rtt-env
```
4. Run the unit test
      - if your server is running at `172.17.0.X:1094`, where `X != 2`, you will need to add `--server=172.17.0.X:1094` to the example below
```
(rtt-env) [root@blah client]# ./run.sh --unittest
Running simple_test.py
Runtime: 0.11977696418762207 seconds
Adding a 10ms delay...
Running simple_test.py
Runtime: 3.2398319244384766 seconds
Removing the 10ms delay...
Done.
```
5. The runtime with the artificial network delay was longer! :tada:

## Running Experiments
Several experiments have been designed to more rigorously simulate actual Physics use cases. Each of these tests is named `<name>_test.py` and placed in `client/experiments` (e.g. `client/experiments/root_test.py`). There is a bash script called `run.sh` in the `client` directory which allows you to run any of these experiments for a series of artificial `netem` delays. Again, we need to hop onto the client container, navigate to the `client` directory, then activate our conda environment:
```
$ docker exec -it rtt-client /bin/bash
[root@blah home]# cd client
[root@blah client]# conda activate rtt-env
```
Assuming we already ran the commands above, here is an example usage for `run.sh`:
```
(rtt-env) [root@blah client]# ./run.sh --experiment=root_test --min_delay=5 --max_delay=10 --step_size=1
```
As in the previous unit test example, if your server is running at `172.17.0.X:1094`, where `X != 2`, you will need to add `--server=172.17.0.X:1094` to the example above. Moreover, all additional arguments (i.e. arguments not explicitly used by `run.sh`) will be passed to the experiment. This can most easily be demonstrated by the Di-Higgs analysis example:
```
(rtt-env) [root@blah client]# ./run.sh --experiment=hgg_test --max_delay=50 --step_size=5 --server=172.17.0.3:1094 --nCores 1 --selections "HHggbb_boosted_Presel" --debug 1 --options "experiments/hgg/data/boosted_ggbb.json" --samples "experiments/hgg/data/samples_and_scale1fb.json" --output_tag "test"
```
In this case, all arguments past `--step_size` are passed to the experiment script `hgg_test.py`. Finally, for the sake of completeness, it should be noted that in the above example, the server was running at `172.17.0.3`, and of course, one would need to remove the `--server` argument or modify it depending on one's needs.
