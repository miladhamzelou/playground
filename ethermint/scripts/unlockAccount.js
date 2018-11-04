#!/usr/bin/env node
var Web3 = require("web3");
var address = process.argv[2];
var password = process.argv[3];
var url;
if (process.argv[4] == null) {
  url = process.argv[4];
} else {
  url = 'http://localhost:8545';
}

var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider(url));
web3.eth.personal.unlockAccount(address, password, 600)
  .then( success => {
    if (success)
      console.info("succeeded to unlock account %s", address);
    else
      console.info("failed to unlock account %s", address);
  });
