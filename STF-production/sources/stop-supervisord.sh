#!/bin/bash

# Check for pyenv
command -v pyenv >/dev/null
if [ $? -eq 0 ]; then
    eval "$(pyenv init -)"
    pyenv activate supervisord
fi

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
