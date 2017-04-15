# !/usr/bin/env python
__author__ = 'yzhao@redhat.com'

import os
import time
from fabric.api import *
from selenium import webdriver

# env.host_string = 'root@10.73.131.65'
# env.password = 'redhat'
# ova_version = "rhvm-appliance-4.1.20170221.0-1.el7ev.4.1.rpm"

os.system('sh ./clean.sh')


def Before_stup():
	with settings(warn_only=True, host_string='root@10.73.131.65', password='redhat'):
		put("/home/zyh/Downloads/rhvm-appliance-4.1.20170413.0-1.el7.4.1.rpm", "/opt/rhvm-appliance-4.1.20170413.0-1.el7.4.1.rpm")
		cmd1 = "rpm -ivh /opt/rhvm-appliance-4.1.20170413.0-1.el7.4.1.rpm"
		cmd2 = "echo '10.73.73.100  yzhao.redhat.com' >> /etc/hosts "
		run(cmd1)
                run(cmd2)

def Deploy_HE():
	with settings(warn_only=True, host_string='root@10.73.131.65', password='redhat'):
		put("/home/zyh/workauto/goproj/src/github.com/dracher/autoanswer/run", "/root/run")
                run("chmod 755 run")
		run("./run -i")


if __name__ == "__main__":
	#ova_version = "rhvm-appliance-4.1.20170221.0-1.el7ev.4.1.rpm"
	Before_stup()
	Deploy_HE()
