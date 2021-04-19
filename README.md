# RTT Lab
This is a virtual "laboratory" for testing the effect of Round Trip Times (RTT) on NanoAOD read latency. Established in 2021 for an [EXPAND](https://center.ucsd.edu/programs/EXPAND.html) project.

## Setup
1. Clone this repository
```
$ git clone https://github.com/jkguiang/rtt-lab.git
$ cd rtt-lab
```
3. Download Docker (i.e. [here](https://docs.docker.com/docker-for-mac/install/) for MacOS users)
4. Build the Docker Image
```
$ docker build -t rtt-lab .
```
5. Run a Docker container using the `rtt-lab` image
  - `-itd` runs in interactive mode and keeps the container running
  - `-v ...` mounts the project directory (should be your current working directory) to the container with read/write privileges
```
$ docker run -itd -v $PWD:/home/$(basename $PWD) --user=root rtt-lab
```
6. Use the container interactively (or modify the Dockerfile to run your tests.)
```
$ docker exec -it <container id> /bin/bash
```
