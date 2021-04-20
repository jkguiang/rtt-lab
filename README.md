# RTT Lab
This is a virtual "laboratory" for testing the effect of Round Trip Times (RTT) on NanoAOD read latency. Established in 2021 for an [EXPAND](https://center.ucsd.edu/programs/EXPAND.html) project.

## Setup
1. Clone this repository
```
$ git clone https://github.com/jkguiang/rtt-lab.git
$ cd rtt-lab
```
2. Download Docker (i.e. [here](https://docs.docker.com/docker-for-mac/install/) for MacOS users)
3. Build the server Docker Image
```
$ cd server
$ docker build -t rtt-server .
```
4. Run a Docker container using the `rtt-server` image
      - `-td` keeps the container running (detatched)
      - `--name=rtt-server` gives the container a human-readable name
      - the server should run at `172.17.0.2:1094`, but run `python inspect.py` to check
```
$ docker run -td --name=rtt-server rtt-server
```
5. Build the client Docker Image
```
$ cd ../client
$ docker build -t rtt-client .
```
6. Run a Docker container using the `rtt-client` image
      - `-td` keeps the container running (detatched)
      - `-v ...` mounts the project directory (should be your current working directory) to the container with read/write privileges
      - `--cap-add=NET_ADMIN` allows the container to modify network properties (i.e. use the tool for adding artificial network delay)
      - `--name=rtt-client` gives the container a human-readable name
```
$ docker run -td -v $PWD:/home/$(basename $PWD) --user=root --cap-add=NET_ADMIN --name=rtt-client rtt-client
```
7. Use the client container interactively (or modify the Dockerfile) to run your tests.
```
$ docker exec -it rtt-client /bin/bash
```

## Running tests
For a simple unit test, you can try the pre-written unit test found inside `client/experiments`.
1. Use the client container interactively (see above)
2. Activate the conda environment
```
$ conda activate rtt-env
```
3. Run a control
```
(rtt-env) $ ./run.sh 0
384065700 nanoseconds
```
4. Add an arbitrary delay (in ms)
```
(rtt-env) $ ./run.sh 10
3187930400 nanoseconds
```
5. The runtime with the artificial network delay was longer! :tada:
