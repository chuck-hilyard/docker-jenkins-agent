# this gives you a base jenkins installation configured for our environment
# the actual jenkins setup/config happens in the init script (see CMD)
FROM ubuntu:latest

USER root

#RUN /usr/local/bin/install-plugins.sh git matrix-auth workflow-aggregator docker-workflow blueocean credentials-binding 

ENV JENKINS_USER admin
ENV JENKINS_PASS admin
ENV JENKINS_SLAVE_ADDRESS ""
ENV CHROME_BIN /usr/bin/chromium-browser

RUN apt-get -y update && apt-get -y upgrade && apt-get -y install openjdk-8-jdk-headless openjdk-8-jre-headless python3 python3-jenkins python3-pip vim sudo git curl chromium-browser
RUN pip3 install requests
RUN useradd jenkins

COPY --chown=jenkins jenkins.war /home/jenkins/jenkins.war
COPY *.groovy /usr/share/jenkins/ref/init.groovy.d/
COPY *.xml /home/jenkins/
COPY aws_codebuild /root/.ssh/id_rsa
COPY aws_codebuild /home/jenkins/.ssh/id_rsa
COPY known_hosts /root/.ssh/known_hosts
COPY known_hosts /home/jenkins/.ssh/known_hosts

RUN cd /tmp; git clone https://github.com/chuck-hilyard/docker-jenkins-agent
RUN chown -R jenkins:jenkins /home/jenkins/; chown -R jenkins:jenkins /tmp
RUN echo "jenkins  ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/README

#VOLUME /home/jenkins

USER jenkins

CMD [ "python3", "-u", "/tmp/docker-jenkins-agent/init.py" ]
