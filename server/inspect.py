import subprocess
import json

def inspect(container_id):
    docker_cmd = subprocess.Popen(
        ["docker", "inspect", container_id], 
        stdout=subprocess.PIPE
    )
    docker_output = docker_cmd.communicate()
    inspect_json = json.loads(docker_output[0])[0]
    name = inspect_json["Name"]
    port = list(inspect_json["NetworkSettings"]["Ports"].keys())[0]
    port = port.split("/")[0]
    ip = inspect_json["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]

    print("Successfully inspected {}".format(name.replace("/", "")))
    print(f"    Port: {port}")
    print(f"    IP Address: {ip}")
    print(f"    XRootD URL: root://{ip}:{port}//<file name>")
    return

if __name__ == "__main__":
    inspect("rtt-server")
