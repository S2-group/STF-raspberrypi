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
source $BASE_DIR/sources/env-stf.inc

pgrep supervisord > /dev/null
if [ $? -ne 0 ]; then
    echo "Starting supervisord"
    supervisord -c $BASE_DIR/sources/supervisord.conf
else
    echo "Using previous instance of supervisord"
fi

declare -a programs=(
    "rethinkdb"
    "adb"

    "stfApp"
    "stfAuthMock"
    "stfMigrate"
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
)
for prog in "${programs[@]}"; do
    supervisorctl -s unix://$UNIX_HTTP_SERVER_SOCKET start "$prog"
done
