#!/bin/bash

sudo apt-get update -y
sudo apt-get install python3 -y
sudo apt-get install python3-pip -y
sudo pip3 install pymysql #doesn't work for me, sudo: pip3: command not found
sudo pip3 install mysql-connector
sudo pip3 install Flask
sudo pip3 install Flask-WTF
sudo pip3 install passlib
sudo pip3 install boto3
