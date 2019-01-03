#!/usr/bin/env node

const Web3 = require("web3");
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

var to = process.argv[2];
var data = process.argv[3];
web3.eth.call({to: to, data: data}).then(result => {
  console.info("return: %s ", result);
});
