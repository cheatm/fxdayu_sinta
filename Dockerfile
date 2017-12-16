FROM continuumio/miniconda

ADD routing /routing
ADD configs /fxdayu/sinta
ENV fxdayu /fxdayu

RUN apt-get update -y
RUN /bin/bash /routing/timezone.sh
RUN /bin/bash /routing/setrq.sh
RUN /bin/bash /routing/sinta.sh
RUN /bin/bash /routing/setcron.sh

VOLUME /data /rqalpha

CMD /usr/sbin/cron -f
