############################
# File: AutoLog.py
# Author: yzhao
# Date : 2016.12.24
# autolog in your dir /mnt
# How to use : 1. install fabric module
#              2. python AutoLog.py 10.73.131.63
############################
import time
from fabric.api import *
import sys

IP = sys.argv[1]
def autolog():
	with settings(warn_only=True, host_string='root@'+IP, password='redhat'):
                local("mkdir -p /mnt/%s_log" % IP)
		cmd1 = "tar -jcvf /root/var_log.gz /var/log/*"
		cmd2 = "tar -jcvf /root/network_scripts.gz /etc/sysconfig/network-scripts/*"
		cmd3 = "tar -jcvf /root/sosreport.gz /var/tmp/*"
		run(cmd1)
		run(cmd2)
		run(cmd3)
		get("/root/*.gz", "/mnt/%s_log/" % IP)

	
if __name__ == '__main__':
	autolog()
	print "The /var/log* ,sosreport, network_scripts logs in your dir /mnt/IP_log/!"
