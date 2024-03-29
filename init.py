# this is called by docker run
#
# starts jenkins
# installs plugins
# adds github based projects to jenkins/jobs

import http.client
import jenkins
import os
import requests
import socket
import subprocess
import time

def install_software():
  # install build/test software
  # TODO: make sure the previous install is done prior to moving on
  subprocess.run(["sudo", "apt-get", "update"])
  time.sleep(10)
  subprocess.run(["sudo", "mkdir", "/var/jenkins_home/.ssh", "/var/jenkins_home/.aws"])
  time.sleep(10)
  subprocess.run(["sudo", "chmod", "755", "/var/jenkins_home"])
  time.sleep(10)
  subprocess.run(["sudo", "cp", "/tmp/authorized_keys", "/var/jenkins_home/.ssh"])
  time.sleep(10)
  subprocess.run(["sudo", "cp", "/tmp/id_rsa", "/var/jenkins_home/.ssh"])
  time.sleep(10)
  subprocess.run(["chmod", "600", "/var/jenkins_home/.ssh/id_rsa", "/root/.ssh/id_rsa"])
  time.sleep(10)
  subprocess.run(["sudo", "cp", "/tmp/sshd_config", "/etc/ssh/"])
  time.sleep(10)
  subprocess.run(["sudo", "cp", "/tmp/known_hosts", "/var/jenkins_home/.ssh"])
  time.sleep(10)
  subprocess.run(["sudo", "ln", "-s", "/usr/local/go/bin/go", "/usr/local/bin/go"])
  time.sleep(10)
  subprocess.run(["sudo", "service", "ssh", "start"])
  time.sleep(10)
  subprocess.run(["sudo", "wget", "-q", "https://dl.google.com/go/go1.11.linux-amd64.tar.gz", "-P", "/tmp"])
  time.sleep(10)
  subprocess.run(["sudo", "gzip", "-d", "/tmp/go1.11.linux-amd64.tar.gz"])
  time.sleep(10)
  subprocess.run(["sudo", "tar", "xf", "/tmp/go1.11.linux-amd64.tar", "-C", "/tmp"])
  time.sleep(10)
  subprocess.run(["sudo", "mv", "/tmp/go", "/usr/local"])
  time.sleep(10)

  print("** INSTALLING NVM ** (Begin)")
  #subprocess.run(["curl", "-#", "-sL", "https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.0/install.sh", "-o", "/var/jenkins_home/install_nvm.sh"], capture_output=True)
  subprocess.run(["curl", "-#", "-sL", "https://raw.githubusercontent.com/creationix/nvm/master/install.sh", "-o", "/var/jenkins_home/install_nvm.sh"])
  time.sleep(60)
  subprocess.run(["mkdir", "/var/jenkins_home/.nvm"])
  time.sleep(5)
  subprocess.run(["touch", "/var/jenkins_home/.bash_profile"])
  time.sleep(5)
  subprocess.run(["echo", ". .nvm/nvm.sh", ">>", "/var/jenkins_home/.bash_profile"])
  time.sleep(5)
  subprocess.run(["chmod", "755", "/var/jenkins_home/install_nvm.sh"])
  time.sleep(15)
  #subprocess.run(["/var/jenkins_home/install_nvm.sh"], env={"NVM_DIR": "/var/jenkins_home/.nvm", "XDG_CONFIG_HOME": "/var/jenkins_home"})
  subprocess.run(["/var/jenkins_home/install_nvm.sh"], env={"NVM_DIR": "/var/jenkins_home/.nvm"})
  time.sleep(15)
  subprocess.run(["echo", 'export NVM_DIR="/var/jenkins_home/.nvm" \ [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"', ">>", "/var/jenkins_home/.bash_profile"])
  time.sleep(5)
  subprocess.run(["chown", "jenkins:jenkins", "/var/jenkins_home/.bash_profile", "-R", "/var/jenkins_home/.nvm"])
  print("** INSTALLING NVM (End) **")

  subprocess.run(["curl -sL https://deb.nodesource.com/setup_10.x |sudo -E bash -"], shell=True)
  time.sleep(30)
  subprocess.run(["sudo", "apt-get", "install", "-y", "nodejs"])
  time.sleep(30)
  subprocess.run(["ssh-keyscan", "github.com", '>>', "/var/jenkins_home/.ssh/known_hosts"])
  time.sleep(30)
  subprocess.run(["sudo", "chown", "jenkins:jenkins", "-R", "/var/jenkins_home"])
  time.sleep(30)
  print("****************************** pip3 INSTALLING consul_kv")
  subprocess.run(["pip3", "install", "consul_kv", "wget"])
  time.sleep(30)
  subprocess.run(["usermod", "-aG", "docker", "jenkins"])
  time.sleep(10)
  subprocess.run(["sudo", "cp", "/tmp/credentials", "/var/jenkins_home/.aws"])
  time.sleep(10)
  subprocess.run("if [ -d /var/jenkins_home/jenkins-rl-bin ]; then echo 'jenkins-rl-bin already exists'; else git clone git@github.com:chuck-hilyard/jenkins-rl-bin.git /var/jenkins_home/jenkins-rl-bin; fi", shell=True, stderr=subprocess.PIPE)

def join_jenkins_master():
  print("joining jenkins master")
  containerId = socket.gethostname()
  server = jenkins.Jenkins('http://jenkins-master', username='admin', password='admin')
  params = {
      'port': '22',
      'username': 'jenkins',
      'credentialsId': 'jenkins-credential-id',
      'host': '172.17.0.3'
    }
  server.create_node(
    containerId,
    nodeDescription = "test slave node",
    remoteFS = "/var/jenkins_home",
    labels = "common",
    exclusive = False,
    launcher = jenkins.LAUNCHER_SSH,
    launcher_params = params)

def is_master_up():
  print("is master up?")
  server = jenkins.Jenkins('http://jenkins-master', username='admin', password='admin')
  try:
    master_job_info = server.get_job_info("jenkins-init", depth=0, fetch_all_builds=False)
    is_up = master_job_info['displayName']
  except (http.client.RemoteDisconnected):
    print("jenkins master may have gone down")
    is_up = False
  except (jenkins.JenkinsException):
    print("unable to connect with master")
    is_up = False
  if is_up == 'jenkins-init':
    print("master is up!")
    return True
  else:
    print("master is DOWN!")
    return False

def node_exists_on_master():
  containerId = socket.gethostname()
  server = jenkins.Jenkins('http://jenkins-master', username='admin', password='admin')
  return server.node_exists(containerId)


def main():
  while True:
    print("main loop")
    status = is_master_up()
    if status == True:
      is_node_on_master = node_exists_on_master()
      if is_node_on_master == False:
        # this is removed in favor of master polling consul
        #join_jenkins_master()
        print("dummy line")
      else:
        print("this agent is already on master")
  else:
    print("master is DOWN...rechecking in 30 seconds")
  time.sleep(60)


if __name__ == '__main__':
  install_software()
  main()
