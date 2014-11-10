from ubuntu:14.10

RUN apt-get update
RUN apt-get install -y python-pip
RUN pip install elb-dance
ADD boto.cfg /etc/boto.cfg
