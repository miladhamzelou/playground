#!/usr/bin/env bash

# 1) build ethermint
git clone http://git.51.nb/chain/ethermint.git ${HOME}/go/src/github.com/tendermint/ethermint
cd ${HOME}/go/src/github.com/tendermint/ethermint                                               
make get_vendor_deps                                                                        
make install

# 2) build tendermint
git clone http://github.com/tendermint/tendermint ${HOME}/go/src/github.com/tendermint/tendermint
cd ${HOME}/go/src/github.com/tendermint/tendermint
make get_vendor_deps
make install
