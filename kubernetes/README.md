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
kubectl create -f rtt-server.yaml
```
4. Log into the pod, untar the inputs directory, and move it to the server area
```
$ kubectl exec -it <server pod name with hash> -- /bin/bash
[root@rtt-server-5b7f49b87f-fqvw2 home]# tar -zxvf inputs.tar.gz
[root@rtt-server-5b7f49b87f-fqvw2 home]# mv inputs/* /data/
[root@rtt-server-5b7f49b87f-fqvw2 home]# rm -r inputs
[root@rtt-server-5b7f49b87f-fqvw2 home]# exit
```
5. Note the server IP
```
$ kubectl get pods -o wide
NAME                          READY   STATUS    RESTARTS   AGE     IP               NODE                     NOMINATED NODE   READINESS GATES
rtt-client-5d595d59cf-62gz9   1/1     Running   0          2d17h   10.244.135.91    stashcache.t2.ucsd.edu   <none>           <none>
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
kubectl create configmap rtt-client-configmap --from-file=client.tar.gz
```
Again, don't forget to include `-n <namespace>` if needed on your system.

3. Create the pod
```
kubectl create -f rtt-client.yaml
```
4. Log into the pod and untar the client directory
```
$ kubectl exec -it <client pod name with hash> -- /bin/bash
[root@rtt-client-5d595d59cf-62gz9 home]# tar -zxvf client.tar.gz
```
5. Run tests! See the [main](https://github.com/jkguiang/rtt-lab/blob/main/README.md)/[client](https://github.com/jkguiang/rtt-lab/blob/main/client/README.md) READMEs for more.

## Useful commands for Kubernetes newbies
- Make a configmap: `kubectl create configmap <configmap name> --from-file=<path to file> -n <namespace>`

- List configmaps: `kubectl get configmaps`

- Create a pod: `kubectl create -f <yaml file>`

- Delete a pod: `kubectl delete -f <yaml file>`

- Copy from pod: `kubectl cp pod_name:<path in container> <path in uaf>`

- Hop onto a pod: `kubectl exec -it <pod name with hash> -- /bin/bash`

- List pods: `kubectl get pods`

## PRP locations
- Amsterdam: `fiona-r-uva.vlan7.uvalight.net`
- Chicago: `osg.chic.nrp.internet2.edu`
- Kansas: `osg.kans.nrp.internet2.edu`
- New York: `osg.newy32aoa.nrp.internet2.edu`
- Santa Cruz: `siderea.ucsc.edu`
