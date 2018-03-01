import subprocess
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import sys
import getpass
import git
import os
import time

jnprusername = str(sys.argv[1])
jnprpassword = str(sys.argv[2])

DEV_USER = jnprusername
PW = jnprpassword
VM_USER = getpass.getuser()
SSH_KEYGEN_DIR = "/home/%s/.ssh" % (VM_USER)
HOME_DIR = "/home/%s/" % (VM_USER)

def line_prepender(filename, line):
    #with os.popen(filename, 'w').write(PW) as f:
    with open(filename, 'rt') as f:
        content = f.read()
        f.seek(0, 0)
        s = line.rstrip('\r\n') + '\n' + content
        with open('tempfile.tmp', 'wt') as outf:
            outf.write(s)
    command = 'sudo mv tempfile.tmp ' + filename
    os.system('echo %s|sudo -S %s' % (PW, command))

def config_devices(podInfo='PodInfo.txt'):
    with open(podInfo, 'r') as f:
        devices = f.readlines()
        devices = [x.strip() for x in devices]

        podNum = ""
        hosts = ""
        for device in devices:
            if "Pod Number" in device:
                podKey,podValue = device.split(":")
                podNum = "pod" + podValue.strip()
            else:
                dev = Device(host=device, user=DEV_USER, password=PW).open()
                hostname = dev.facts["hostname"]
                hosts += ("{}     {}\n".format(device,hostname))
                dev.close()
        print("{}".format(hosts))
        line_prepender("/etc/hosts", hosts)

def config_ssh_keys(devInfo="PodInfo.txt"):
    with open(devInfo, 'r') as f:
        devices = f.readlines()
        devices = [x.strip() for x in devices]

        sshKeyFile = "/home/" + VM_USER +"/.ssh/id_rsa.pub"
        sshKey = ""
        with open(sshKeyFile, 'rt') as f:
            sshKey = f.read()
            sshKey = sshKey.strip()
        ssh_key_conf = 'set system login user {} uid 2018\nset system login user {} class super-user\nset system login user {} authentication ssh-rsa "{}"'.format(VM_USER,VM_USER,VM_USER,sshKey)
        with open('tempfile.conf', 'wt') as outf:
            outf.write(ssh_key_conf)

        CONFIG_FILE = 'tempfile.conf'

        for device in devices:
            if "Pod Number" not in device:
                dev = Device(host=device, user=DEV_USER, password=PW).open()
                with Config(dev) as cu:
                    cu.load(template_path=CONFIG_FILE, format='set', merge=True)
                    cu.commit(timeout=30)
                    print("Committing the configuration on device: {}".format(device))
                dev.close()

    command = 'sudo rm tempfile.conf'
    os.system('echo %s|sudo -S %s' % (PW, command))

def key_present():
    """Checks to see if there is an RSA already present. Returns a bool."""
    if "id_rsa" in os.listdir(SSH_KEYGEN_DIR):
        return True
    else:
        return False

def gen_key():
    """Generate a SSH Key."""
    if key_present():
        print("A key is already present.")
    else:
        # Genarate private key
        command = "ssh-keygen -f /home/" + VM_USER +"/.ssh/id_rsa -N ''"
        subprocess.call(command, shell=True)

def accept_ssh_keys(devInfo="PodInfo.txt"):
    with open(devInfo, 'r') as f:
        devices = f.readlines()
        devices = [x.strip() for x in devices]

        accept_keys = "#!/bin/sh\n\n# Accept the SSH Keys\n"
        for device in devices:
            if "Pod Number" not in device:
                accept_keys += "ssh-keygen -R {}\nssh-keyscan -H {} >> ~/.ssh/known_hosts\n\n".format(device,device)
        print("{}".format(accept_keys))
        with open(HOME_DIR + "installations_3.sh", "wt") as fil:
            fil.write(accept_keys)
            fil.close()
        time.sleep(3)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

print("\n\n      ########  Update the /etc/hosts file to match your network  ########")
config_devices()

print("\n\n      ########  Clone the GIT Project Repository  ########")
git.Git(HOME_DIR).clone("https://github.com/Sudhishna/EVPN-VXLAN.git")
print("EVPN-VXLAN Ansible Project cloned")

print("\n\n      ########  Generate SSH Key  ########")
gen_key()

print("\n\n      ########  Push User Login Configs to the devices  ########")
config_ssh_keys()

print("\n\n      ########  Accept the key from networking devices  ########")
accept_ssh_keys()
subprocess.call(['./installations_3.sh'])

countdown(40)

print("\n\n      #####  AUTOMATION SYSTEM IS READY   #####")
