# this is called by docker run
#
# starts jenkins
# installs plugins
# adds github based projects to jenkins/jobs

import http.client
import requests
import subprocess
import time

# install build/test software
# TODO: make sure the previous install is done prior to moving on
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
subprocess.run(["sudo", "apt-get", "install", "-y", "awscli"])
time.sleep(15)
subprocess.run(["usermod", "-aG", "docker", "jenkins"])
time.sleep(15)
subprocess.run(["sudo", "npm", "install", "-g", "gulp"])
time.sleep(15)
subprocess.run(["sudo", "service", "docker", "restart"])

