# this is called by docker run
#
# starts jenkins
# installs plugins
# adds github based projects to jenkins/jobs

import http.client
import requests
import subprocess
import time

def install_software():
  # install build/test software
  # TODO: make sure the previous install is done prior to moving on
  subprocess.run(["ssh-keyscan github.com >> /home/jenkins/.ssh/known_hosts"])
  time.sleep(15)
  subprocess.run(["sudo", "apt-get", "install", "-y", "curl"])
  time.sleep(15)
  subprocess.run(["sudo", "useradd", "jenkins"])
  time.sleep(15)
  subprocess.run(["curl -sL https://deb.nodesource.com/setup_10.x |sudo -E bash -"], shell=True)
  time.sleep(15)
  subprocess.run(["sudo", "apt-get", "install", "-y", "nodejs"])
  time.sleep(15)
  # TODO: verify npm is installed
  subprocess.run(["sudo", "apt-get", "install", "-y", "chromium-browser"])
  time.sleep(15)
  subprocess.run(["sudo", "apt-get", "install", "-y", "libgconf2-4"])
  time.sleep(15)
  subprocess.run(["sudo", "apt-get", "install", "-y", "docker.io"])
  time.sleep(15)
  #subprocess.run(["sudo", "apt-get", "install", "-y", "awscli"])
  time.sleep(15)
  subprocess.run(["sudo", "apt-get", "install", "-y", "openjdk-8-jre-headless"])
  time.sleep(15)
  subprocess.run(["usermod", "-aG", "docker", "jenkins"])
  time.sleep(15)
  subprocess.run(["sudo", "npm", "install", "-g", "gulp"])
  time.sleep(15)
  subprocess.run(["sudo", "service", "docker", "start"])
  time.sleep(15)
  subprocess.run(["chown", "jenkins:jenkins", "-R", "/home/jenkins"])
  time.sleep(15)
  subprocess.run(["sudo", "service", "ssh", "start"])



def main():
  while True:
    print("main loop")


if __name__ == '__main__':
  install_software()
  main()
