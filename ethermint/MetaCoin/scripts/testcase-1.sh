#!/bin/bash

#TESTSCRIPT_DIR 当前脚本的路径位置
if [ $0 == "/bin/bash" ]; then
    TESTSCRIPT_DIR="."
elif [ $0 == "-bash" ]; then
    TESTSCRIPT_DIR="."
else
    TESTSCRIPT_DIR=$(realpath $(dirname $0))
fi

#获取路径信息
PROJECT_DIR=$(dirname ${TESTSCRIPT_DIR})
PLAYGROUND_DIR=$(dirname ${PROJECT_DIR})
NODE1_ACCOUNT=0x1bf79321a6d313e6057f72bee5faa97403099e36
NODE1_PASSWORD=1234
NODE2_ACCOUNT=0xd6eb44c49d36debe6ead82220c123ff4bac1f03e
NODE2_PASSWORD=2234
REPORT_FILE=/dev/null

#新建report目录
if [ ! -d "${TESTSCRIPT_DIR}/report/" ]; then
    mkdir ${TESTSCRIPT_DIR}/report
fi

#导入外部依赖
source ${TESTSCRIPT_DIR}/utils.sh

#禁用掉当前的其他的错误消息
ulimit -c 0

echo -e "\n--------------------START THE TEST!--------------------\n"

echo -e "1) start ethermint & tendermint"

#重置节点的配置信息
cd ${PLAYGROUND_DIR}/native
source ${PLAYGROUND_DIR}/native/util.sh ${PLAYGROUND_DIR}/native
bash ${PLAYGROUND_DIR}/native/run.sh >${REPORT_FILE}
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi

echo -e "2) unlock account"
#解锁测试账户
cd ${TESTSCRIPT_DIR}
node unlockAccount.js http://localhost:8645 ${NODE2_ACCOUNT} ${NODE2_PASSWORD}
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi
node unlockAccount.js http://localhost:8545 ${NODE1_ACCOUNT} ${NODE1_PASSWORD}
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi

echo -e "3) add account"
#添加账户
node addAccount.js http://localhost:8645 1234
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi

echo -e "4) send tx periodically"
cd ${TESTSCRIPT_DIR}
{ nohup node sendTransaction.js > ${TESTSCRIPT_DIR}/report/sendTransaction.report 2>&1 & }

echo -e "5) check height growth normal"
cd ${TESTSCRIPT_DIR}
check_height_growth_normal 127.0.0.1 46657 60 > ${REPORT_FILE}

if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi 

#进入测试目录进行测试操作
cd ${PROJECT_DIR}
echo -e "6) deploy contract"
truffle migrate --reset
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi 

echo -e "7) test contract function"
truffle test
if [ $? -ne 0 ]; then
    echo -e "failed"
    exit 1
fi 

echo -e "8) stop node3, check height growth and test contract function"
cd ${PLAYGROUND_DIR}/native
stopEthermint 3  > ${REPORT_FILE}
stopTendermint 3 > ${REPORT_FILE} 

cd ${TESTSCRIPT_DIR}
check_height_growth_normal 127.0.0.1 46657 60 > ${REPORT_FILE}

if [ $? -ne 0 ]; then
    echo -e "check height growth failed!"
    exit 1
fi 

cd ${PROJECT_DIR}
truffle test test/metacoin.js

if [ $? -ne 0 ]; then
    echo -e "run the test cases failed!\n"
    exit 1
fi

echo -e "9) stop node4, and check the height growth"
cd ${PLAYGROUND_DIR}/native
stopTendermint 4  > ${REPORT_FILE}
stopEthermint 4  > ${REPORT_FILE}

cd ${TESTSCRIPT_DIR}
check_height_growth_normal 127.0.0.1 46657 60 > ${REPORT_FILE}

if [ $? -eq 0 ]; then
    echo -e "check height growth failed, it should not get the growth!\n"
    exit 1
fi 

echo -e "10) start node3, and check the height growth, test the contract function"
cd ${PLAYGROUND_DIR}/native
startTendermint 3  > ${REPORT_FILE}
startEthermint 3  > ${REPORT_FILE}

cd ${TESTSCRIPT_DIR}
check_height_growth_normal 127.0.0.1 46657 60 > ${REPORT_FILE}

if [ $? -ne 0 ]; then
    echo -e "check height growth failed!"
    exit 1
fi 

cd ${PROJECT_DIR}
truffle test test/metacoin.js  > ${REPORT_FILE}
if [ $? -ne 0 ]; then
    echo -e "run the test cases failed!\n"
    exit 1
fi

echo -e "11) run the contract test, and start node4, check the height growth on node4"
cd ${PLAYGROUND_DIR}/native
{ startTendermint 4 > ${REPORT_FILE} ; startEthermint 4  > ${REPORT_FILE} ; } &

cd ${PROJECT_DIR}
truffle test test/metacoin.js > ${REPORT_FILE}
if [ $? -ne 0 ]; then
    echo -e "run the test cases failed!\n"
    exit 1
fi

cd ${TESTSCRIPT_DIR}
check_height_growth_normal 127.0.0.1 46957 60 > ${REPORT_FILE}

if [ $? -ne 0 ]; then
    echo -e "check height growth on node4 failed"
    cd ${TESTSCRIPT_DIR}
    jobs -rp | xargs kill
    exit 1
fi 


echo -e "\n\n--------------------test pass--------------------\n"

cd ${TESTSCRIPT_DIR}
jobs -rp | xargs kill

cd ${PLAYGROUND_DIR}/native
for i in {1..4}; do
    stopEthermint $i > ${REPORT_FILE}
    stopTendermint $i > ${REPORT_FILE}
done
