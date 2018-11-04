#!/usr/bin/env node
'use strict';
var keythereum = require('keythereum');
const fs = require('fs');
const path = require('path');
const util = require('util');
const { spawnSync } = require('child_process');
const toml = require('toml');
const json2toml = require('json2toml');

function updateBalance(genesis, address, balance){
  if (!genesis.alloc[address])
    genesis.alloc[address]= {}
  else
    genesis.alloc[address]= genesis.alloc[address];
  genesis.alloc[address]['balance'] =  balance.toString();
  return genesis;
}

function initTendermint(homedir){
  spawnSync('tendermint', ['--home', homedir, 'init']);
}

function initEthermint(datadir){
  spawnSync('ethermint', ['--datadir', datadir, 'init', path.join(datadir, 'tendermint', 'config', 'genesis.json')]);
}

function updateValidator(genesis, name, pub_key, power){
  var validator = {
    pub_key,
    'power': power,
    'name': name
  };
  genesis.validators.push(validator);
  return genesis;
}

function updateTendermintConfig(homedir, shift, seeds) {
  var configFile = path.join(homedir, 'config', 'config.toml');
  var config = toml.parse(fs.readFileSync(configFile));

  config.proxy_app = 'tcp://127.0.0.1:' + (46658 + shift);
  config.rpc.laddr = 'tcp://127.0.0.1:' + (46657 + shift);
  config.p2p.laddr = '0.0.0.0:' + (46656 + shift);
  config.p2p.seeds = seeds;

  var content = json2toml(config)
  fs.writeFileSync(configFile, content, 'utf8');
  return config;
}

function setupGenesis(count){
  // setup directory tree
  for (var i = 1; i <= count; i++){
    var name = 'node' + i;
    rmdir(name);
    fs.mkdirSync(name);
    var tendermint = path.join(name, 'tendermint');
    fs.mkdirSync(tendermint);
    var config = path.join(tendermint, 'config');
    fs.mkdirSync(config);
  }
  // load genesis template
  var genesis = JSON.parse(fs.readFileSync(path.join(__dirname, 'genesis-template.json')));
  var keystoreDir = path.join(__dirname, 'keystore');

  // setup keystore
  fs.readdirSync(keystoreDir).forEach((file, index) => {
    if (file.indexOf('UTC') != 0)
      return;


    for (var i = 1; i <= count; i++) {
      var destdir = path.join('node'+i, 'keystore');
      if (!fs.existsSync(destdir)) {
        fs.mkdirSync(destdir);
      }
      fs.copyFileSync(path.join(keystoreDir, file), path.join(destdir, file))
    }
  });

  // setup balance
  fs.readdirSync(keystoreDir).forEach((file, index) => {
    if (file.indexOf('UTC') != 0)
      return;
    var keystore = JSON.parse(fs.readFileSync(path.join(keystoreDir, file)));

    updateBalance(genesis, keystore.address,  1 * Math.pow(10, 20));
  });

  // setup validators
  for (var i = 1; i <= count; i++) {
    var name = 'node' + i;
    var power = 20;
    var src = path.join(__dirname, 'validator', name + '.json');
    var dest =  path.join('node' + i, 'tendermint', 'config', 'priv_validator.json');
    fs.copyFileSync(src, dest);
    var validator = JSON.parse(fs.readFileSync(dest));
    updateValidator(genesis, name, validator.pub_key, power);
  }

  // save to disk
  var json = JSON.stringify(genesis, null, 2);
  for (var i = 1; i <= count; i++){
    var dest = path.join('node' + i, 'tendermint', 'config', 'genesis.json');
    fs.writeFileSync(dest, json, 'utf8');
  }
}

function rmdir(dir) {
  if (!fs.existsSync(dir)) {
    return;
  }
  var stats = fs.statSync(dir);
  if (!stats.isDirectory()){
    return fs.unlinkSync(dir);
  }
  fs.readdirSync(dir).forEach((file, index) => rmdir(path.join(dir, file)));
  fs.rmdirSync(dir);
};


function setup(count, native){
  // setup genesis
  setupGenesis(count);

  // init tendermint
  for (var i = 1; i <= count; i++){
    var homedir = path.join('node'+ i, 'tendermint');
    initTendermint(homedir);
  }


  // init ethermint
  for (var i = 1; i <= count; i++){
    var datadir = path.join('node'+ i);
    initEthermint(datadir);
  }

  // update tendermint config
  var id = spawnSync('tendermint', ['--home', 'node1/tendermint', 'show_node_id']);
  var seeds;
  if (native) {
    seeds = id.stdout.toString().substr(0, 40) + '@127.0.0.1:' + 46656;
  } else {
    seeds = id.stdout.toString().substr(0, 40) + '@node1:' + 46656;
  }

  for (var i = 1; i <= count; i++){
    var homedir = path.join('node'+ i, 'tendermint');
    var shift;
    if (native) {
      shift = 100*(i-1);
    } else {
      shift = 0;
    }
    updateTendermintConfig(homedir, shift, seeds);
  }

  // generate ethermint start script
  for (var i = 1; i <= count; i++){
    var datadir;
    var shift;

    if (native) {
      datadir = 'node' + i.toString();
      shift = 100*(i-1);
    } else {
      datadir = '/data';
      shift = 0;
    }

    var filename = path.join('node' + i.toString(), 'startEthermint.sh');
    var template =
        `#!/usr/bin/env bash
ethermint --datadir %s  \
          --abci_laddr "%s" \
          --tendermint_addr "%s" \
          --rpc \
          --rpcapi eth,net,web3,personal,admin \
          --rpcaddr "0.0.0.0" \
          --rpcport %s \
          --verbosity 6  >%s 2>&1 &
disown
`;
    var command = util.format(template,
                              datadir,
                              'tcp://0.0.0.0:' + (46658 + shift).toString(),
                              'tcp://0.0.0.0:' + (46657 + shift).toString(),
                              (8545 + shift).toString(),
                              path.join(datadir, 'ethermint.log'));

    fs.writeFileSync(filename, command, {mode: 0o755});
  }
  // generate tendermint start script
  for (var i = 1; i <= count; i++){
    var datadir;
    if (native) {
       datadir = 'node' + i.toString();
    } else {
      datadir = '/data'
    }
    var homedir = path.join(datadir, 'tendermint');
    var filename = path.join('node' + i.toString(), 'startTendermint.sh');
    var template =
        `#!/usr/bin/env bash
tendermint --home %s node >%s 2>&1 &
disown
`;
    var command = util.format(template, homedir, path.join(datadir, 'tendermint.log'));
    fs.writeFileSync(filename, command, {mode: 0o755});
  }
}

var nodes = process.argv[2];
var native = process.argv[3] === "native";
setup(nodes, native);
