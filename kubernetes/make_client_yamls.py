import subprocess
import argparse
import os

HOSTNAMES = [
    "fiona-r-uva.vlan7.uvalight.net",
    "osg.chic.nrp.internet2.edu",
    "osg.kans.nrp.internet2.edu",
    "osg.newy32aoa.nrp.internet2.edu",
    "siderea.ucsc.edu",
    "stashcache.t2.ucsd.edu"
]

LOCATIONS = [
    "Amsterdam",
    "Chicago",
    "Kansas",
    "New York",
    "Santa Cruz",
    "San Diego"
]

def yaml_template(server, name, hostname, location):
    return f"""apiVersion: v1
kind: Pod
metadata:
  name: {name}
  namespace: cms
spec:
  tolerations:
  - effect: NoSchedule
    key: nautilus.io/stashcache
    operator: Exists
  containers:
  - image: jguiang/rtt-client:latest
    command: [ "/bin/bash", "-c", "--" ]
    args: [ "./run_tests.sh --server={server} --location={location};" ]
    imagePullPolicy: Always
    name: {name}
    resources:
      limits:
        cpu: 4
        memory: 4Gi
      requests:
        cpu: 2
        memory: 2Gi
    securityContext:
      capabilities:
        add:
        - NET_ADMIN
    volumeMounts:
    - mountPath: /home/
      name: cache-vol
    - mountPath: /home/client.tar.gz
      name: rtt-client-dir-configmap
      subPath: client.tar.gz
    - mountPath: /home/run_tests.sh
      name: rtt-client-exe-configmap
      subPath: run_tests.sh
  restartPolicy: Never
  nodeSelector:
    kubernetes.io/hostname: {hostname}
  schedulerName: default-scheduler
  terminationGracePeriodSeconds: 30
  volumes:
  - name: cache-vol
    emptyDir: {{}}
  - name: rtt-client-dir-configmap
    configMap: 
      name: rtt-client-dir-configmap
      items:
      - key: client.tar.gz
        path: client.tar.gz
      defaultMode: 0777
  - name: rtt-client-exe-configmap
    configMap: 
      name: rtt-client-exe-configmap
      items:
      - key: run_tests.sh
        path: run_tests.sh
      defaultMode: 0777"""

def make_client_yamls(server, name="rtt-client"):
    global HOSTNAMES
    global LOCATIONS
    os.makedirs("pods", exist_ok=True)
    for hostname, location in zip(HOSTNAMES, LOCATIONS):
        _location = location.lower().replace(" ", "-")
        with open(f"pods/rtt-client-{_location}.yaml", "w") as f_out:
            f_out.write(yaml_template(server, f"{name}-{_location}", hostname, _location))

if __name__ == "__main__":
    # Set up CLI
    cli = argparse.ArgumentParser(
        description="Make kubernetes config .yaml files for client pods"
    )
    cli.add_argument(
        "--port",
        type=str,
        default="1094",
        help="Port used by XRootD on server pod (defaul: 1094)"
    )
    cli.add_argument(
        "--name",
        type=str,
        default="rtt-client",
        help="Base name of pod"
    )
    # Parse CLI input
    args = cli.parse_args()
    # Find server
    kube_cmd = subprocess.Popen(
        ["kubectl", "get", "pods", "-o", "wide"], 
        stdout=subprocess.PIPE
    )
    kube_output = str(kube_cmd.communicate()[0])
    server = ""
    for row in kube_output.split("\\n")[:-1]:
        cols = row.split()
        if "rtt-server" in cols[0]:
            server = cols[5]
    if server != "":
        print(f"Found server at {server}")
        print("Port assumed to be {}".format(args.port))
        server += ":"+args.port
        make_client_yamls(server, name=args.name)
    else:
        print("ERROR: Kubernetes rtt-server deployment not found")
