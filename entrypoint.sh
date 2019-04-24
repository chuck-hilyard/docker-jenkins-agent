#!/usr/bin/env bash

set -e

chown -R jenkins:jenkins /var/jenkins_home

exec "$@"
