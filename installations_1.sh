#!/bin/sh

# To get the latest package lists 
sudo apt-get update -y

# Install Requred Python Packages
sudo apt-get install python-minimal software-properties-common python python-pip sshpass apt-transport-https ca-certificates python-dev libffi-dev libssl-dev -y
