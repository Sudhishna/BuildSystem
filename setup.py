import subprocess
import sys
import getpass
import git
import os
import time

if sys.stdin.isatty():
    print("Enter credentials")
    jnprusername = input("Lab Device Username: ")
    jnprpassword = getpass.getpass("Lab Device Password: ")
else:
    jnprusername = sys.stdin.readline().rstrip()
    jnprpassword = sys.stdin.readline().rstrip()

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

print("\n\n      ########  Making initial Installations  ########")
subprocess.call(['./installations_1.sh'])

line_prepender("/etc/apt/sources.list", "deb http://ppa.launchpad.net/ansible/ansible/ubuntu xenial main")

print("\n\n      ########  Installing Ansible and its modules  ########")
subprocess.call(['./installations_2.sh'])

subprocess.call(['python3','setup-config.py',DEV_USER,PW])

