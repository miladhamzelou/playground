#!/usr/bin/env node

const keythereum = require("keythereum");
const fs = require('fs');
const path = require('path');
var password = process.argv[2];
var keystore = process.argv[3];
createAccount(password, keystore);


////////////////////////////////////////////////////////////////////////////////
function createAccount(password, keystore) {
  var params = { keyBytes: 32, ivBytes: 16 };
  var kdf = 'pbkdf2';
  var options = {
    kdf: 'pbkdf2',
    cipher: 'aes-128-ctr',
    kdfparams: {
      c: 262144,
      dklen: 32,
      prf: 'hmac-sha256'
    }
  };

  var dk = keythereum.create(params);
  var keyObject = keythereum.dump(password, dk.privateKey, dk.salt, dk.iv, options);
  var filename = keythereum.exportToFile(keyObject, keystore);
  fs.appendFileSync(path.join(keystore, 'password'), path.basename(filename) + ':' + password + '\n');
  return keyObject;
}
