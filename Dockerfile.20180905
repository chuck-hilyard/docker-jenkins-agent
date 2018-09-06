FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && apt-get install -y openssh-server git sudo python3 python3-pip python3-jenkins 

RUN useradd -d /var/jenkins_home jenkins
RUN mkdir -p /var/jenkins_home
COPY id_rsa.pub /var/jenkins_home/.ssh/authorized_keys
COPY known_hosts /var/jenkins_home/.ssh/known_hosts
COPY aws_credentials /var/jenkins_home/.aws/credentials
COPY init.py /var/jenkins_home/init.py
RUN chown -R jenkins:jenkins /var/jenkins_home

ADD init.py /home/jenkins/init.py

WORKDIR /var/jenkins_home

ENV JENKINS_URL "http://jenkins"
ENV JENKINS_SLAVE_ADDRESS ""
ENV JENKINS_USER "admin"
ENV JENKINS_PASS "admin"
ENV SLAVE_NAME ""
ENV SLAVE_SECRET ""
ENV SLAVE_EXECUTORS "1"
ENV SLAVE_LABELS "docker"
ENV SLAVE_WORING_DIR ""
ENV CLEAN_WORKING_DIR "true"
ENV CHROME_BIN "/usr/bin/chromium-browser"

EXPOSE 22

#USER jenkins

CMD [ "python3", "-u", "/home/jenkins/init.py" ]

