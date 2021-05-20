# RTT Lab: Kubernetes
Since the RTT client and server are Docker containers, we can easily deploy them as pods on a Kubernetes cluster to get real network delays. The instructions below detail how to set this up. Note: this was done using [PRP](https://ucsd-prp.gitlab.io/) resources, so some additional (albeit minor) configuration will certainly be required to set this up on any other system.

## Set up the server pod
1. Tar up the inputs directory
```
tar -zcvf inputs.tar.gz ../server/inputs
```
NOTE: if you add input files such that the inputs directory becomes larger than 3MB, you will need to put these files somewhere publicly accessible, then manually download them to the server pod (e.g. using `wget` or `curl`).

2. Make a configmap that points to the tarball we just made
```
kubectl create configmap rtt-inputs-configmap --from-file=inputs.tar.gz
```
Don't forget to include `-n <namespace>` if needed on your system.

3. Create the pod
```
kubectl create -f deployments/rtt-server.yaml
```
4. Log into the pod, untar the inputs directory, and move it to the server area
```
$ kubectl exec -it <server pod name with hash> -- /bin/bash
[root@rtt-server-5b7f49b87f-fqvw2 /]# cd home
[root@rtt-server-5b7f49b87f-fqvw2 home]# tar -zxvf inputs.tar.gz
[root@rtt-server-5b7f49b87f-fqvw2 home]# mv server/inputs/* /data/
[root@rtt-server-5b7f49b87f-fqvw2 home]# rm -r server
[root@rtt-server-5b7f49b87f-fqvw2 home]# exit
```
5. Note the server IP
```
$ kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP               NODE                     NOMINATED NODE   READINESS GATES
rtt-server-5b7f49b87f-fqvw2   1/1     Running   0          2d18h   10.244.135.105   stashcache.t2.ucsd.edu   <none>           <none>
```
In the example above, we see that we will need to specify `--server=10.244.135.105:1094` when we run our tests on the client pod.

## Set up the client pod
1. Tar up the client directory
```
tar -zcvf client.tar.gz ../client
```
2. Make a configmap that points to the tarball we just made
```
kubectl create configmap rtt-client-dir-configmap --from-file=client.tar.gz
```
Again, don't forget to include `-n <namespace>` if needed on your system.

### Interactive tests
3. Create the pod
```
kubectl create -f deployments/rtt-client.yaml
```
4. Log into the pod and untar the client directory
```
$ kubectl exec -it <client pod name with hash> -- /bin/bash
[root@rtt-client-5d595d59cf-62gz9 home]# tar -zxvf client.tar.gz
```
5. Run tests! See the [main](https://github.com/jkguiang/rtt-lab/blob/main/README.md)/[client](https://github.com/jkguiang/rtt-lab/blob/main/client/README.md) READMEs for more.

### Automatic tests
Before running the steps below, it is crucial to (a) make sure the server is running and (b) check `make_client_yamls.py` to ensure that the hostname and locations are actually relevant to your studies. The default values are very specific to running on PRP machines! Lastly, check `run_tests.sh` to ensure that the tests being run are the ones you are interested in.

3. Make a configmap that points to `run_tests.sh`
```
kubectl create configmap rtt-client-exe-configmap --from-file=run_tests.sh
```
4. Make the pod yaml files
```
python make_client_yamls.py --server=<IP:port> --name=<optional name>
```
Note that you will need to do this **every time you restart the server**.

5. Create a pod
```
kubectl create -f pods/rtt-client-san-diego.yaml
```
The pod will copy the outputs to the server pod as a single tarred file, then shut down when the tests are finished.

## Useful commands for Kubernetes newbies
- Make a configmap: `kubectl create configmap <configmap name> --from-file=<path to file> -n <namespace>`

- List configmaps: `kubectl get configmaps`

- Create a pod: `kubectl create -f <yaml file>`

- Delete a pod: `kubectl delete -f <yaml file>`

- Copy from pod: `kubectl cp <pod name with has>:<path in container> <path in uaf>`

- Hop onto a pod: `kubectl exec -it <pod name with hash> -- /bin/bash`

- List pods: `kubectl get pods`

## PRP locations
All RTT times are averages computed by pinging a given server ~30 times and are relative to La Jolla, CA.
- :trident: San Diego (RTT = 0.38ms): `stashcache.t2.ucsd.edu`
- Santa Cruz (RTT = 10ms): `siderea.ucsc.edu`
- Kansas (RTT = 35.2ms): `osg.kans.nrp.internet2.edu`
- Chicago (RTT = 45ms): `osg.chic.nrp.internet2.edu`
- New York (RTT = 63.7): `osg.newy32aoa.nrp.internet2.edu`
- Amsterdam (RTT = 154ms): `fiona-r-uva.vlan7.uvalight.net`
