#!/usr/bin/env bash

grin_repo=~/codes/grin
grin_miner_repo=~/codes/grin-miner
workspace=~/playground
password="123"


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

    ${grin_repo}/target/debug/grin --usernet  server config
    sed -i 's/run_tui = true/run_tui = false/g' grin-server.toml
    # sed -i 's/enable_stratum_server = false/enable_stratum_server = true/g' grin-server.toml
    # sed -i 's/file_log_level = "Debug"/file_log_level = "Trace"/g' grin-server.toml
    sed -i 's/run_test_miner = false/run_test_miner = true/g' grin-server.toml
    sed -i 's/#test_miner_wallet_url = "http:\/\/127.0.0.1:3415"/test_miner_wallet_url = "http:\/\/127.0.0.1:23415"/g' grin-server.toml
}
start_server() {
    cd ${workspace}

    ${grin_repo}/target/debug/grin --usernet server run
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

    cat > /tmp/init_wallet.exp <<'EOF'
set grin_exe [lindex $argv 0]
set password [lindex $argv 1]

spawn $grin_exe --usernet  wallet init -h
expect -re "File .*grin-wallet.toml configured and created"
expect "Please enter a password for your new wallet"
expect "Password:"
send "$password\r"
expect "Confirm Password:"
send "$password\r"
EOF
    expect /tmp/init_wallet.exp ${grin_repo}/target/debug/grin ${password}
}
start_wallet() {
    cd ${workspace}

    ${grin_repo}/target/debug/grin --usernet  wallet -d . -p ${password} listen
}

################################################################################
init_miner(){
    cd ${workspace}

    cp ${grin_miner_repo}/grin-miner.toml .
    sed -i 's/run_tui = true/run_tui = false/g' grin-miner.toml
    sed -i 's/stratum_server_addr = "127.0.0.1:3416"/stratum_server_addr = "127.0.0.1:13416"/g' grin-miner.toml
    sed -i '/s/plugin_name = "cuckaroo_cpu_compat_29"/plugin_name = "cuckatoo_cpu_compat_29"/g' grin-miner.toml
}

clean_miner(){
    cd ${workspace}

    pkill -9 grin-miner
    rm grin-miner.log
}

start_miner(){
    cd ${workspace}

    ${grin_miner_repo}/target/debug/grin-miner
}

################################################################################
clean() {
    clean_miner
    clean_wallet
    clean_server
}

init() {
    init_server
    init_wallet
    init_miner
}
