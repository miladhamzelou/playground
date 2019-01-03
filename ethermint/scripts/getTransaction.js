#!/usr/bin/env node
const Web3 = require("web3");
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

var block = process.argv[2];
var index  = process.argv[3];
web3.eth.getTransactionFromBlock(block, index).then(tx => {
  console.info("tx: ", tx);

})
