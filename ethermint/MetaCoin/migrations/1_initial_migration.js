var Web3 = require("web3");
var Migrations = artifacts.require("./Migrations.sol");

module.exports = function(deployer, netowrk, accounts) {
    var address = '0x7eff122b94897ea5b0e2a9abf47b86337fafebdc';
    var password = '1234';
    var web3 = new Web3();

    console.log('>> Unlock account ');
    web3.setProvider(deployer.provider);
    web3.personal.unlockAccount(address, password, 600);

    console.log('>> Deploying migration');
    deployer.deploy(Migrations);
};
