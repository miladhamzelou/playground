#!/usr/bin/env node
const Web3     = require("web3");
const from     = "0x7eff122b94897ea5b0e2a9abf47b86337fafebdc";
const to       = "0xb0415e80b9a11fff35a396b854e52b3463b55f0a";
const password = "1234";
const gas      = 0x10000;
const gasPrice = 1;
const bonus    = 3;
const chainId  = 101;

var web3 = new Web3();
web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));

function unlockAccount() {
  console.info("1) unlock account");
  return web3.eth.personal.unlockAccount(from, password, 60000);
}

function printBalance(title) {
  console.info(title);
  return web3.eth.getBalance(from)
    .then((balance) => console.info("  from: ", balance))
    .then(()=> web3.eth.getBalance(to))
    .then( balance => console.info("  to: ", balance));
}

function sendBonus(step) {
  console.info("%d) getTransactionCount", step);
  step+=1;
  return web3.eth.getTransactionCount(from, "pending")
    .then(nonce => {
      console.info("  nonce: ", nonce);
      var rawTx = {
        nonce: nonce,
        from: from,
        to: to,
        data: "",
        value:  bonus,
        gasPrice: gasPrice,
        gas: gas
      };
      console.info("%d) signTransaction", step);
      step+=1;
      return web3.eth.signTransaction(rawTx);
    })
    .then(tx => {
      console.info(" signedTx: ", tx.raw);
      return web3.eth.getBlockNumber()
        .then(height => {
          console.info("%d) getBlockNumber", step);
          step+=1;
          console.info("  height: ", height);
        })
        .then(() => {
          console.info("%d) sendSignedTransaction", step);
          step+=1;
          var txTime = new Date();
          return web3.eth.sendSignedTransaction(tx.raw)
            .on('transactionHash', hash => {
              var now = new Date();

              console.info("%d) %s ms later, received tx hash", step, now - txTime)
              console.info("  hash: %s ",  hash);
              step+=1;
              var timer = setInterval( ()=> {
                web3.eth.getTransactionCount(from, "pending")
                  .then(nonce => {
                    if (!(nonce == tx.tx.nonce)) {
                      var now = new Date();
                      console.info("%d) %s ms later, nonce changed", step, now - txTime);
                      console.info("  nonce: %d -> %d", tx.tx.nonce, nonce);
                      step+=1;
                      clearInterval(timer);
                    }
                  })
              }, 100);
            })
            .on('receipt', receipt=> {
              var now = new Date();
              console.info("%d) %s ms later, mined tx in block", step, now-txTime);
              console.info("  height: %d", receipt.blockNumber);
              step+=1;
              return receipt;
            });
        })
        .catch(err => {
          console.error("err: ", err);
        });
    });
}


unlockAccount()
  .then(()=> printBalance("2) balances before tx"))
  .then(() => sendBonus(3))
  .then(() => printBalance("10) balances after tx"));
