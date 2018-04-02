#!/bin/sh

# Install PIP packages
sudo -H pip install --upgrade pip
sudo -H pip install setuptools --upgrade
sudo -H pip install pyopenssl ndg-httpsclient pyasn1
sudo -H pip install junos-eznc
sudo -H pip install jxmlease
sudo -H pip install gitpython
sudo -H pip install ansible

# Install Ansible modules
ansible-galaxy install Juniper.junos

rm -rf ~/EVPN-VXLAN

# Install PIP3 packages
sudo apt-get install python3-pip -y
sudo -H pip3 install junos-eznc
sudo -H pip3 install gitpython
