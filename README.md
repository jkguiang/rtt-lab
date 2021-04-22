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
rtt-lab $ cd server
rtt-lab/server $ docker build -t rtt-server .
```
4. Run a Docker container using the `rtt-server` image
      - `-td` keeps the container running (detatched)
      - `--name=rtt-server` gives the container a human-readable name
```
rtt-lab/server $ docker run -td --name=rtt-server rtt-server
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

## Running tests
For a simple unit test, you can try the pre-written unit test found inside `client/experiments`.
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
4. Run a control
      - if your server is not running at `172.17.0.2:1094`, you will need to edit `test.sh` to reflect this
```
(rtt-env) [root@blah client]# ./test.sh 0
Runtime: 0.14122414588928223 seconds
```
5. Add an arbitrary delay (in ms)
```
(rtt-env) [root@blah client]# ./test.sh 10
Runtime: 2.930720090866089 seconds
```
6. The runtime with the artificial network delay was longer! :tada:
