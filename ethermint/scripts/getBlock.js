#!/usr/bin/env node

const Web3 = require("web3");
var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

var from = process.argv[2];
web3.eth.(from).then(balance => {
  console.info("balance[%s] = %d ", from, balance);
});
