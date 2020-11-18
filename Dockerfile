FROM ubuntu:latest
COPY Docker-entrypoint.sh /usr/local/bin/

ENV DEBIAN_FRONTEND "noninteractive"

RUN apt-get update && apt-get upgrade -yq && apt-get install -y openssh-server git sudo python3 python3-pip python3-jenkins chromium-browser vim curl libgconf-2-4 openjdk-8-jre openjdk-8-jdk nodejs awscli python3-boto3

RUN useradd -d /var/jenkins_home -s /bin/bash jenkins
COPY id_rsa.pub /tmp/authorized_keys
COPY id_rsa /tmp/id_rsa
COPY known_hosts /tmp/known_hosts
COPY aws_credentials /tmp/credentials
COPY sshd_config /tmp/sshd_config

ADD init.py /tmp/init.py

# nvm install
#ENV NVM_DIR="/var/jenkins_home/.nvm"
#RUN curl -sL https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh -o /tmp/install_nvm.sh \ 
#  && mkdir ${NVM_DIR} \
#  && /tmp/install_nvm.sh \
#  #&& echo "export NVM_DIR="/var/jenkins_home/.nvm" \
#  #  [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"  # This loads nvm \
#  #  [ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion" >> /var/jenkins_home/.bash_profile \
#  && chown jenkins:jenkins /var/jenkins_home/.bash_profile -R ${NVM_DIR}

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
ENV CHROME_BIN "/usr/bin/chromium-browser"
ENV CLEAN_WORKING_DIR "true"

EXPOSE 22

COPY entrypoint.sh /usr/local/bin/
ENTRYPOINT ["entrypoint.sh"]

CMD [ "python3", "-u", "/tmp/init.py" ]
