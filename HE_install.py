import time
from selenium import webdriver
from fabric.api import *
import logging
from vncdotool import api

env.password = 'redhat'
root_url = "http://10.73.73.13:9090"
NFS_storage_path = "10.66.61.114:/home/zyh/nfs1"
NIC = "em1"
deploy_model = "disk"
storage_path = "/home"
MAC = "52:54:00:5e:8e:c7"
VM_FQDN = "rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com"
VM_IP = "10.73.73.100"
root_password = "redhat"
engine_password = "redhat"


def press_keys(seq, cli):
    """press keys sequence

    """
    for keys in seq:
        if len(keys) > 1:
            for k in keys:
                cli.keyPress(k)
                time.sleep(0.5)
        elif len(keys) == 1:
            cli.keyPress("shift-%s" % keys[0])
        else:
            logging.warning("Error at least should have one key")



class HandleVNCSetup:
    def __init__(self, ip='10.73.73.13' ,vnc_pass='redhat'):
        self.ip = ip
        self.vnc_pass = vnc_pass
        self._set_vnc_pass()
        self.cli = api.connect(self.ip, password=self.vnc_pass)

    def _set_vnc_pass(self):
        with settings(warn_only=True, host_string='root@10.73.73.13', password='redhat'):
            run('hosted-engine --add-console-password --password=%s' % self.vnc_pass, quiet=True)

    def turn_on_ssh(self):
        for k in 'root':
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)

        for k in 'redhat':
            self.cli.keyPress(k)
            time.sleep(0.1)
        self.cli.keyPress('enter')
        time.sleep(1)

        #############################################
        for k in "sed -i 's/":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-3')  # --> '#'

        for k in "PermitRootLogin yes/PermitRootLogin yes/g' /etc/ssh/sshd":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-_')  # --> '_'

        for k in "config":
            self.cli.keyPress(k)
            time.sleep(0.1)

        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        #####################################

        for k in "sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd":
            self.cli.keyPress(k)
            time.sleep(0.1)

        self.cli.keyPress('shift-_')  # --> '_'

        for k in "config":
            self.cli.keyPress(k)
            time.sleep(0.1)

        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        ##################################

        for k in "service sshd restart":
            self.cli.keyPress(k)
            time.sleep(0.1)
        time.sleep(1)
        self.cli.keyPress('enter')
        time.sleep(1)

        logging.warning("Hope ssh is turn on, cause is hard to see if success.")


def HostedEngine_install():
    with settings(warn_only=True, host_string='root@10.66.61.114', password='redhat'):
        run("rm -rf /home/zyh/nfs1/*")
        run("service nfs start",quiet=True)
    with settings(warn_only=True, host_string='root@10.73.73.13', password='redhat'):
        cmd1 = "echo '10.73.73.13  dell-per510-01.lab.eng.pek2.redhat.com' >> /etc/hosts"
        cmd2 = "echo '10.73.73.100  rhevh-hostedengine-vm-04.lab.eng.pek2.redhat.com' >> /etc/hosts"
        #cmd3 = "cat /var/log/ovirt-hosted-engine-setup/* |grep '**%QEnd: OVEHOSTED_ENGINE_UP'"
        run(cmd1)
        run(cmd2)
        put("/var/www/html/zyh/rhevm-appliance-20160831.0-1.el7ev.ova", "/opt/rhevm-appliance-20160831.0-1.el7ev.ova")

    time.sleep(1)
    dr = webdriver.Firefox()
    dr.get(root_url)
    time.sleep(5)
    id = dr.find_element_by_id
    class_name = dr.find_element_by_class_name
    xpath = dr.find_element_by_xpath
    
    id("login-user-input").send_keys("root")
    time.sleep(1)
    id("login-password-input").send_keys("redhat")
    time.sleep(1)
    id("login-button").click()
    time.sleep(5)
    dr.get(root_url + "/ovirt-dashboard")
    dr.switch_to_frame("cockpit1:localhost/ovirt-dashboard")
    xpath("//a[@href='#/he']").click()
    time.sleep(3)
    class_name("btn-primary").click()
    time.sleep(5)
    class_name("btn-default").click()     #click next button,continue yes
    time.sleep(35)
    class_name("btn-default").click()    #use storage model
    time.sleep(2)
    class_name("form-control").send_keys(NFS_storage_path) #NFS storage path
    time.sleep(2)
    class_name("btn-default").click()    #confirm nfs storage path
    time.sleep(5)
    class_name("btn-default").click()    #iptables default confirm
    time.sleep(2)
    class_name("btn-default").click()    #gateway ip confirm
    time.sleep(2)
    class_name("form-control").clear()   #select NIC
    time.sleep(1)
    class_name("form-control").send_keys(NIC)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()   #select deploy model
    time.sleep(1)
    class_name("form-control").send_keys(deploy_model)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()    #select vnc
    time.sleep(1)
    class_name("form-control").clear()   #input ova path
    time.sleep(1)
    class_name("form-control").send_keys("/opt/rhevm-appliance-20160831.0-1.el7ev.ova")
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(65)

    class_name("form-control").clear()
    time.sleep(2)
    class_name("form-control").send_keys(storage_path)
    time.sleep(5)
    class_name("btn-default").click()
    time.sleep(3)

    class_name("btn-default").click()    #select cloud-init
    time.sleep(2)
    class_name("btn-default").click()    #select Generate
    time.sleep(2)
    class_name("form-control").send_keys(VM_FQDN)  #set VM FQDN
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()      #Manual setup
    time.sleep(1)
    class_name("form-control").send_keys("no")
    time.sleep(2)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()       #Set VM domain
    time.sleep(2)
    class_name("form-control").clear()      #set root password
    time.sleep(1)
    class_name("form-control").send_keys(root_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("form-control").clear()
    time.sleep(1)
    class_name("form-control").send_keys(root_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()     #set cpu type,default
    time.sleep(2)
    class_name("btn-default").click()     #set the number of vcpu
    time.sleep(2)
    class_name("form-control").clear()    #set unicast MAC
    time.sleep(1)
    class_name("form-control").send_keys(MAC)
    time.sleep(1)
    class_name("btn-default").click()     
    time.sleep(2)
    class_name("form-control").clear()    #set memory size
    time.sleep(1)
    class_name("form-control").send_keys("4096")
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()     #network,default DHCP
    time.sleep(2)
    class_name("btn-default").click()     #resovle hostname
    time.sleep(2)
    class_name("form-control").clear()    #set engine admin password
    time.sleep(1)
    class_name("form-control").send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(1)
    class_name("form-control").clear()
    time.sleep(1)
    class_name("form-control").send_keys(engine_password)
    time.sleep(1)
    class_name("btn-default").click()
    time.sleep(2)
    class_name("btn-default").click()     #set hostname,default hosted_engine_x
    time.sleep(2)
    class_name("btn-default").click()     #set the name of SMTP
    time.sleep(1)
    class_name("btn-default").click()     #set the port of SMTP,default 25
    time.sleep(1)
    class_name("btn-default").click()     #set email address
    time.sleep(1)
    class_name("btn-default").click()     #set comma-separated email address
    time.sleep(5)
    class_name("btn-default").click()     #confirm the configuration
    time.sleep(600)
   

    time.sleep(10)
    with settings(warn_only=True, host_string='root@10.73.73.13', password='redhat'):
        HandleVNCSetup(ip='10.73.73.13' ,vnc_pass='redhat').turn_on_ssh()
    time.sleep(10)


    with settings(warn_only=True, host_string='root@10.73.73.100', password='redhat'):
        put("/home/zyh/workauto/goproj/src/github.com/dracher/autoanswer/run", "~/run")
        run("chmod 755 ~/run")
        run("./run -i")
    time.sleep(40)
    
    class_name("btn-default").click()
    time.sleep(500)
    
    
    with settings(warn_only=True, host_string='root@10.73.73.100', password='redhat'):
            run("reboot",quiet=True)
    time.sleep(60)
    


		
if __name__ == "__main__":
    HostedEngine_install()