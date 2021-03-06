import subprocess
import sys
import getpass
import os
import time

if sys.stdin.isatty():
    print("Enter credentials")
    try: input = raw_input
    except NameError: pass
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

print("\n\n      ########  Installing Ansible and its modules  ########")
subprocess.call(['./installations_2.sh'])

if not os.path.exists(SSH_KEYGEN_DIR):
    os.makedirs(SSH_KEYGEN_DIR)
    
py_version = sys.version
python_version = py_version.split(".")[0]
py_ver = "python" + python_version

subprocess.call([py_ver,'setup-config.py',DEV_USER,PW])
