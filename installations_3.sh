#!/bin/sh

# Accept the SSH Keys
ssh-keygen -R 172.25.92.2
ssh-keyscan -H 172.25.92.2 >> ~/.ssh/known_hosts

ssh-keygen -R 172.25.92.3
ssh-keyscan -H 172.25.92.3 >> ~/.ssh/known_hosts

ssh-keygen -R 172.25.92.4
ssh-keyscan -H 172.25.92.4 >> ~/.ssh/known_hosts

ssh-keygen -R 172.25.92.5
ssh-keyscan -H 172.25.92.5 >> ~/.ssh/known_hosts

