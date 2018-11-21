var assert = require('assert');
var should = require('should');


var ipfsAPI = require('ipfs-api') ;
const fs = require('fs')

describe('ipfs', function() {
  it('add/get', async function() {
    const ipfs = ipfsAPI('ipfs.infura.io', '5001', {protocol: 'https'})
    this.timeout(20000);

    let testFile = fs.readFileSync("test/ipfs.test.js");
    let testBuffer = Buffer.from(testFile);
    let response = await ipfs.files.add(testBuffer);
    console.info('add files: ', response);

    let files = await ipfs.files.get(response[0].path);
    console.info('path: ', files[0].path);
    console.info('content: ', files[0].content.toString('utf8'));
    assert.equal(files[0].path, response[0].path);
  });
});
