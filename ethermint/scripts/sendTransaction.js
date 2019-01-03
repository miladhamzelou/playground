#!/usr/bin/env node
var Web3 = require('web3')
var from = process.argv[2];
var to = process.argv[3];
var value = process.argv[4];
var data = process.argv[5];
var web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

web3.eth.sendTransaction({from: from,to: to, value: value, data: data})
    .on('transactionHash',function(hash){console.log(hash)})
    .on('receipt',function(receipt){console.log(receipt)})
    //.on('confirmation',function(confirmationNumber,receipt){console.log(confirmationNumber)})
    .on('error',console.error)
