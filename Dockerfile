FROM continuumio/miniconda

ADD routing /routing
ENV fxdayu /fxdayu


# Install system environment
RUN echo 'Asia/Shanghai' >/etc/timezone
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN apt-get update -y
RUN apt-get install -y cron
RUN apt-get install -y gcc
RUN apt-get install -y g++

# Install python environment
RUN pip install bs4
RUN pip install openpyxl
RUN pip install xlrd
RUN pip install git+https://github.com/xingetouzi/fxdayu_data/tree/py2-0.1.16.git
RUN pip install bcolz
RUN pip install rqalpha
RUN pip install git+https://github.com/cheatm/fxdayu_sinta.git

# Create and start cron service.
RUN crontab /routing/TimeList
RUN service cron start
