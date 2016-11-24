import time
import logging
from fabric.api import *
from vncdotool import api

env.host_string = 'root@10.73.73.13'
env.password = 'redhat'


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
		run('hosted-engine --add-console-password --password=%s' % self.vnc_pass)

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

if __name__ == '__main__':
	HandleVNCSetup(ip='10.73.73.13' ,vnc_pass='redhat').turn_on_ssh()