#!/usr/bin/env bash

set_local_vars() {
  echo "set_local_vars()"
  export AUTHORIZATION_TOKEN=${access_key:=FakeToken}
}

set_real_vars() {
  echo "set_real_vars()"
  environment=$(curl -s -X GET http://consul:8500/v1/kv/${service_name}/config/environment?raw)
  platform=$(curl -s -X GET http://consul:8500/v1/kv/${service_name}/config/PLATFORM?raw)
  credentials=$(curl -X GET http://vault/v1/secret/data/${environment}/${platform}/cert/aws-credentials -H "X-Vault-Token: ${1}" |jq -r '.data.key')
  $(echo credentials) > /var/jenkins_home/.aws/credentials
}

if [ -z $service_name ]
  then echo "service_name is NOT set"

  else echo "service_name: ${service_name}"
fi

if [[ $environment = "local" ]]
  then
    echo "running locally"
    if [ -d /rl/data/logs/${service_name} ]
      then :
      else
        echo "creating /rl/data/logs/${service_name}"
        mkdir -p /rl/{data/logs/${service_name}}
    fi
    set_local_vars

  else
    echo "retrieving vault token"
    token=$(curl -s -X GET http://consul:8500/v1/kv/${service_name}/vault_config/token?raw)
    echo "test $?"
    if [ $? = 0 ]
      then
        set_real_vars ${token}
        if [ -d /rl/data/logs/${service_name} ]
          then :
          else
            echo "creating /rl/data/logs/${service_name}"
            mkdir -p /rl/{data/logs/${service_name}}
        fi

      else
        echo "vault token NOT set, exiting"
        exit 1
    fi
fi

exec "$@"
RLC-MED-176070:docker-jenkin
