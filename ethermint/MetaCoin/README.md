# 1.依赖的软件
* npm
* truffle
* web3

在运行测试脚本以前，需要安装npm，然后在MetaCoin文件夹下面运行`npm install`安装需要的包。

# 2.脚本文件说明

## 测试场景
**testcase-1.sh**

测试场景是在存在超过2/3的节点正常的情况下，系统可以正常运行。通过对各个节点的在线关闭与开启来进行测试。

具体的场景说明见 **issue #1**

```
bash testcase-1.sh
```
## 其他脚本说明
**unlockAccount.js**

解锁账户的脚本

```
node unlockAccount.js <url> <account> <password>
```
**addAccount.js**

账户的脚本

```
node addAccount.js <url> <password>
```

**sendTransaction.js**

调用web3不停地进行发送交易的js脚本，从节点1的一个账户发送一笔交易到节点4的账户。

```
node sendTransaction.js
```

**utils.sh**

主要是完成测试所需要的一些额外的函数，包括获取当前区块高度、检查当前高度增长是否正常等函数


# 3.测试说明
```
1.已经禁用掉core文件的生成

2.在开始测试的时候，通过后台调用sendTran.sh来不断的想node1发送消息，在结束的时候使用jobs来进行关闭，有的时候会产生一些core文件

3.report文件夹里面存放的是后台发送交易信息的详细报告
```

