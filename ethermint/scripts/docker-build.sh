#!/bin/bash
# 0) util
build_develop_image(){
    rm    -rf temp
    mkdir -p  temp
    docker build -t dxsdk/chain:develop -f scripts/Dockerfile.develop .
}

build_release_image(){
    mkdir -p temp/github.com/tendermint/
    rsync -a ~/go/src/github.com/tendermint/tendermint  temp/github.com/tendermint/
    rsync -a ~/go/src/github.com/tendermint/ethermint   temp/github.com/tendermint/
    docker build -t dxsdk/chain:release -f scripts/Dockerfile .
}

# 1) build develop image
build_develop_image

# 2) build release image
build_release_image
