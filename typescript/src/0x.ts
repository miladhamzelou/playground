import {
    assetDataUtils,
    BigNumber,
    ContractWrappers,
    generatePseudoRandomSalt,
    Order,
    orderHashUtils,
    signatureUtils,
    Web3ProviderEngine,
    RPCSubprovider,
    ERC20TokenWrapper,
} from '0x.js';
import { MnemonicWalletSubprovider } from '@0x/subproviders';
import { Web3Wrapper } from '@0x/web3-wrapper';



(async function() {
    const MNEMONIC = 'luggage scissors person arrive daughter stereo order print emotion rule ocean garment';
    const BASE_DERIVATION_PATH = `44'/60'/0'/0`;
    const DECIMAL = new BigNumber(18);
    const ROPSTEN_NETWORK_ID = 3;


    const mnemonicWallet = new MnemonicWalletSubprovider({
        mnemonic: MNEMONIC,
        baseDerivationPath: BASE_DERIVATION_PATH,
    });
    const pe = new Web3ProviderEngine();
    const rpcUrl = 'https://ropsten.infura.io/';
    pe.addProvider(mnemonicWallet);
    pe.addProvider(new RPCSubprovider(rpcUrl));
    pe.start();


    const providerEngine = pe;
    const web3Wrapper = new Web3Wrapper(providerEngine);
    const [owner, leftMaker, rightMaker, matcherAccount] = await web3Wrapper.getAvailableAddressesAsync();
    var erc20Wrapper = new ERC20TokenWrapper(web3Wrapper, ROPSTEN_NETWORK_ID, [owner, leftMaker, rightMaker, matcherAccount], owner);
    [erc20TokenA] = await erc20Wrapper.deployDummyTokensAsync(1, DECIMAL)
    console.info("erc20TokenA: ", erc20TokenA);
    return 0;
}())
