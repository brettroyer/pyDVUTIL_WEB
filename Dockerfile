FROM python:3.8.10
# https://hub.docker.com/_/python/tags?page=1&name=3.8.10
#https://www.howtogeek.com/devops/how-to-ssh-into-a-docker-container/

# Dockerfile Maintainer
MAINTAINER Brett Royer "brettroyer@gmail.com"

# Install Dependancys
RUN apt-get -qq -y update \
	&& apt-get -qq -y install git \
	nano \
	passwd \
	openssh-server \
	&& apt-get autoremove -y \
    && apt-get clean -y
	
RUN sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN useradd -m -s /bin/bash sshuser

RUN echo "sshuser:password" | chpasswd

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app

EXPOSE 22
EXPOSE 3001

ENTRYPOINT service ssh start && bash

# To keep container running
CMD tail -f /dev/null
