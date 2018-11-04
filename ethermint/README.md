# build
## native build 
```
scripts/native-build.sh  
```

## docker build 
mount native go source directory into docker.  
```
scripts/docker-build.sh  
```

# run
## prerequirement
```
npm install -g web3 keythereum toml json2toml web3
```
## configure validator (optional)
```
tendermint gen_validator > scripts/validator/nodeX.json
```

## configure account (optional)
```
./scripts/createAccount.js  password scripts/keystore/
```

## native run
```
mkdir native  
cd native  
source ../scripts/util.sh  
startNative  
```

## docker run
```
mkdir docker  
cd docker  
source ../scripts/util.sh  
startDocker  
```
