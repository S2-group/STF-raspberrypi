#!/bin/bash

# Check for pyenv configuration
command -v pyenv >/dev/null
if [ $? -eq 0 ]; then
    eval "$(pyenv init -)"
    pyenv activate supervisord
fi

# Load nvm
command -v nvm >/dev/null
if [ $? -ne 0 ]; then
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
fi
nvm use 8

if [ -z ${BASE_DIR+x} ]; then 
    export BASE_DIR=$HOME
fi
source $BASE_DIR/sources/env-supervisord.inc

declare -a programs=(
    "stfApp"
    "stfAuthMock"
    "stfProcessor001"
    "stfProcessor002"
    "stfProvider"
    "stfReaper"
    "stfStoragePluginAPK"
    "stfStoragePluginImage"
    "stfStorageTemp"
    "stfTriproxyApp"
    "stfTriproxyDev"
    "stfWebsocket"
    "stfApi"
    "stfGroupsEngine"

    "rethinkdb"
)

pgrep supervisord > /dev/null
if [ $? -eq 0 ]; then
    for prog in "${programs[@]}"; do
        supervisorctl -s unix://$UNIX_HTTP_SERVER_SOCKET stop "$prog"
    done
else
    echo "supervisord is not running"
fi
