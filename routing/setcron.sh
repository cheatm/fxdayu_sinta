#! /bin/bash

apt-get update -y
apt-get install -y cron
crontab /routing/TimeList
