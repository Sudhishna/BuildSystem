#!/bin/sh

# Install Ansible
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 93C4A3FD7BB9C367
sudo apt-get update
sudo apt-get install ansible -y

# Install Ansible modules
ansible-galaxy install Juniper.junos,1.4.3

sudo rm -rf EVPN-VXLAN/
