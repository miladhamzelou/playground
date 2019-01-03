#!/usr/bin/env bash

script_dir=$(realpath $(dirname ${BASH_SOURCE}))
check_args() {
    if [ $# -ne 1 ]; then
        echo "error: require one argument"
        return 1
    fi
    if [ $1 -ge 1 ] && [ $1 -le 4 ]; then
        return 0
    fi
    echo "error: argument should be in 1~4"
    return 1
}

startEthermint() {
    check_args $* || return 1
    node=node$1
    ./${node}/startEthermint.sh
}
startTendermint() {
    check_args $* || return 1
    node=node$1
    ./${node}/startTendermint.sh
}

start() {
    check_args $* || return 1
    startEthermint $1
    startTendermint $1
}
stopEthermint() {
    check_args $* || return 1
    node=node$1
    ps aux|grep 'ethermint --datadir'  |grep "${node}" |awk '{ if (NF > 2) system("kill -9 " $2); }'
}
stopTendermint() {
    check_args $* || return 1
    node=node$1
    ps aux|grep 'tendermint --home' |grep "${node}" |awk '{ if (NF > 2) system("kill -9 " $2); }'
}
stop() {
    stopEthermint $*
    stopTendermint $*
}

status() {
    ps aux|grep 'tendermint --home'   |grep -v 'grep'
    ps aux|grep 'ethermint --datadir' |grep -v 'grep'
}

reset() {
    check_args $* || return 1
    node=node$1

    stopEthermint $1
    stopTendermint $1
    rm -rf ./${node}
}

startNative(){
    for i in {1..4}; do
        reset $i
    done

    ${script_dir}/setup.js 4 native

    for i in {1..4}; do
        start $i
    done
}

startDocker(){
    cp ${script_dir}/docker-compose.yml docker-compose.yml
    docker-compose down || true
    ${script_dir}/setup.js 4 docker
    docker-compose up -d
}
