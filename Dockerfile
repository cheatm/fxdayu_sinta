FROM continuumio/miniconda

ADD routing /routing
ENV fxdayu /fxdayu

RUN /bin/bash /routing/timezone.sh
RUN /bin/bash /routing/setrq.sh
RUN /bin/bash /routing/sinta.sh
RUN /bin/bash /routing/setcron.sh

CMD /usr/sbin/cron -f
