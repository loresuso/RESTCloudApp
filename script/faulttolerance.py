import os

res = os.popen("docker ps -a | grep -w frontend").read()
if "Exited" in res:
    os.system("docker restart frontend")
    exit(0)

if "Stopped" in res:
    os.system("docker restart frontend")
