#!/usr/bin/env bash

BIN=~/playground/bin
CONFIG=~/playground/config
workspace=~/playground
password="123"
network="--floonet"

################################################################################
clean_server(){
    cd ${workspace}

    pkill -9 grin
    rm grin-server.toml
    rm -rf chain_data
    rm -rf grin-server.log
}

init_server() {
    cd ${workspace}

    ${BIN}/grin ${network} server config
    sed -i 's/run_tui = true/run_tui = false/g' grin-server.toml
    sed -i 's/enable_stratum_server = false/enable_stratum_server = true/g' grin-server.toml
    sed -i 's/file_log_level = "Debug"/file_log_level = "Trace"/g' grin-server.toml
    #sed -i 's/run_test_miner = false/run_test_miner = true/g' grin-server.toml
    #sed -i 's/#test_miner_wallet_url = "http:\/\/127.0.0.1:3415"/test_miner_wallet_url = "http:\/\/127.0.0.1:23415"/g' grin-server.toml
}
start_server() {
    cd ${workspace}

    ${BIN}/grin server start
}

################################################################################
clean_wallet() {
    cd ${workspace}

    pkill -9 grin
    rm grin-wallet.toml
    rm grin-wallet.log
    rm -rf wallet_data
}

init_wallet() {
    cd ${workspace}

    mkdir wallet_data
    cat > /tmp/init_wallet.exp <<'EOF'
set grin     [lindex $argv 0]
set network  [lindex $argv 1]
set password [lindex $argv 2]


spawn $grin $network init -h
expect -re "File .*grin-wallet.toml configured and created"
expect "Please enter a password for your new wallet"
expect "Password:"
send "$password\r"
expect "Confirm Password:"
send "$password\r"
expect ".*"
expect "Please back-up these words in a non-digital format."
expect "Command 'init' completed successfully"
EOF
    expect /tmp/init_wallet.exp ${BIN}/grin ${network} ${password}
}
start_wallet() {
    cd ${workspace}

    nohup ${BIN}/grin  wallet  -p ${password} listen >/dev/null &
}

################################################################################
init_miner(){
    cd ${workspace}

    cp ${CONFIG}/grin-miner.toml .
    sed -i 's/run_tui = true/run_tui = false/g' grin-miner.toml
    sed -i 's/stratum_server_addr = "127.0.0.1:3416"/stratum_server_addr = "127.0.0.1:13416"/g' grin-miner.toml
}

clean_miner(){
    cd ${workspace}

    pkill -9 grin-miner
    rm grin-miner.log
    rm grin-miner.toml
}

start_miner(){
    cd ${workspace}

    nohup ${BIN}/grin-miner >/dev/null &
}

################################################################################

clean_wallet713() {
    cd ${workspace}

    rm wallet713.toml
    rm -rf wallet713_data
}
init_wallet713() {
    cd ${workspace}
    cat > wallet713.toml  <<EOF
chain = "FlooTesting"
wallet713_data_path = "wallet713_data"

grinbox_domain = "grinbox.io"
grinbox_port=443

default_keybase_ttl = "24h"

grin_node_uri = "127.0.0.1:23413"
grin_node_secret = "${password}"

EOF
}
start_wallet713() {
    cd ${workspace}
    ${BIN}/wallet713 -c ./wallet713.toml --floonet
}
################################################################################
clean() {
    clean_miner
    clean_wallet
    clean_server
    clean_wallet713
}

init() {
    init_server
    init_wallet
    init_miner
    init_wallet713
}

start() {
    start_server
    start_wallet
    start_miner
}
