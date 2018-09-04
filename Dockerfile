FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y && apt-get install -y openssh-server git sudo python3 python3-pip python3-jenkins 

RUN useradd jenkins
RUN mkdir -p /home/jenkins
COPY id_rsa /home/jenkins/.ssh/id_rsa
COPY id_rsa.pub /home/jenkins/.ssh/authorized_keys
COPY known_hosts /home/jenkins/.ssh/known_hosts
COPY aws_credentials /home/jenkins/.aws/credentials
COPY sshd_conf /home/jenkins

ADD init.py /home/jenkins/init.py

WORKDIR /home/jenkins

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

