#!/bin/sh

# Install PIP packages
sudo -H pip install --upgrade pip
sudo -H pip install setuptools --upgrade
sudo -H pip install pyopenssl ndg-httpsclient pyasn1
sudo -H pip install ansible
sudo -H pip install junos-eznc
sudo -H pip install jxmlease
sudo -H pip install gitpython

# Install Ansible modules
sudo ansible-galaxy install Juniper.junos

# Install PIP3 packages
sudo apt-get install python3-pip -y
sudo -H pip3 install --upgrade pip
sudo -H pip3 install junos-eznc
sudo -H pip3 install jxmlease
sudo -H pip3 install gitpython

rm -rf ~/EVPN-VXLAN
