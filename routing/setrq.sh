#! /bin/bash
# Install compiler
apt-get install -y gcc
apt-get install -y g++
# Install rqalpha
pip install bcolz
pip install rqalpha
# Generate language pack
apt-get install -y locales
echo "en_US.UTF-8 UTF-8" > /etc/locale.gen
locale-gen
