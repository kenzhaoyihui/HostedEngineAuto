import time
from fabric.api import *


env.host_string = 'root@10.73.73.100'
env.password = 'redhat'

def start_HE_setup():
	put("/home/zyh/workauto/goproj/src/github.com/dracher/autoanswer/run", "~/run")
	run("chmod 755 ~/run")
	cmd = "./run -i"
	run(cmd)

if __name__=="__main__":
	start_HE_setup()
