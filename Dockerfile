#FROM openjdk:8-jdk
FROM ubuntu:latest

ARG user=jenkins
ARG group=jenkins
ARG uid=1000
ARG gid=1000
ARG JENKINS_AGENT_HOME=/home/${user}

ENV JENKINS_AGENT_HOME ${JENKINS_AGENT_HOME}

RUN groupadd -g ${gid} ${group} \
    && useradd -d "${JENKINS_AGENT_HOME}" -u "${uid}" -g "${gid}" -m -s /bin/bash "${user}"

# setup SSH server
RUN apt-get update \
    && apt-get install --no-install-recommends -y openssh-server git\
    && rm -rf /var/lib/apt/lists/*
RUN sed -i /etc/ssh/sshd_config \
        -e 's/#PermitRootLogin.*/PermitRootLogin no/' \
        -e 's/#RSAAuthentication.*/RSAAuthentication yes/'  \
        -e 's/#PasswordAuthentication.*/PasswordAuthentication no/' \
        -e 's/#SyslogFacility.*/SyslogFacility AUTH/' \
        -e 's/#LogLevel.*/LogLevel INFO/' && \
    mkdir /var/run/sshd

COPY --chown=jenkins id_rsa.pub /home/jenkins/.ssh/authorized_keys
COPY --chown=jenkins id_rsa /home/jenkins/.ssh/id_rsa
RUN ssh-keyscan github.com >> /home/jenkins/.ssh/known_hosts; chown jenkins:jenkins /home/jenkins/.ssh/known_hosts

VOLUME "${JENKINS_AGENT_HOME}" "/tmp" "/run" "/var/run"
WORKDIR "${JENKINS_AGENT_HOME}"

COPY setup-sshd /usr/local/bin/setup-sshd

EXPOSE 22

RUN cd /tmp; git clone https://github.com/chuck-hilyard/docker-jenkins-agent
RUN chown -R jenkins:jenkins /var/jenkins_home/; chown -R jenkins:jenkins /tmp
RUN echo "jenkins  ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/README

USER jenkins

CMD [ "python3", "-u", "/tmp/docker-jenkins-agent/init.py" ]
