#!/bin/sh

# To get the latest package lists 
sudo apt-get update -y
sudo apt-get upgrade

# Install Requred Python Packages
sudo apt-get install python-minimal software-properties-common python python-pip sshpass apt-transport-https ca-certificates python-dev libffi-dev libssl-dev -y

# install python 2.7.12
mv /usr/lib/python2.7 /usr/lib/badpython2.7
sudo apt-get install build-essential checkinstall -y
sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y
wget https://www.python.org/ftp/python/2.7.12/Python-2.7.12.tgz
tar -xvf Python-2.7.12.tgz
cd Python-2.7.12
./configure
make
make install
