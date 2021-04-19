Setup
```
$ docker build -t rtt-lab .
$ docker run -itd -v $PWD:/home/$(basename $PWD) --user=root rtt-lab
```
