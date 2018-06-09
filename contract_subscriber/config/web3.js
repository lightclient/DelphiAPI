const ds_json = require('../contracts/DelphiStake.json'),
		dv_json = require('../contracts/DelphiVoting.json'),
		df_json = require('../contracts/DelphiStakeFactory.json'),
		token_abi = require('human-standard-token-abi'),
	  Web3 = require('web3'),
	  abiDecoder = require('abi-decoder'),
	  { ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');

// web3 setup
const web3 = new Web3(ETH_NETWORK_URL);

// this is where DelphiStakeFactory has been deployed in the ethersphere
factoryAddress = {
	deth: '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
	ropsten: '0xcac53a387d8e38c10a6a077482bd1741340e4e6e',
	rinkeby: '0x5751a4a918435b0ae87f1f28308597baa729d5c7'
}

const DelphiStakeFactory = new web3.eth.Contract(
	df_json.abi,
	factoryAddress[ETH_NETWORK]
);

function loadDelphiStake(address) {
	return new web3.eth.Contract(
		ds_json.abi,
		address
	);
}

abiDecoder.addABI(ds_json.abi);
abiDecoder.addABI(df_json.abi);

function loadToken(address) {
	return new web3.eth.Contract(
		token_abi,
		address
	);
}

async function getTokenInfo(address) {
	const token = loadToken(address);

	// extract useful data
	const name = await token.methods.name().call();
	const symbol = await token.methods.symbol().call();
	const decimals = await token.methods.decimals().call();

	const info = {
		name: name,
		symbol: symbol,
		decimals: decimals
	};

	return info;
}

exports.web3 = web3;
exports.getTransaction = web3.eth.getTransaction;
exports.getBlock = web3.eth.getBlock;
exports.loadDelphiStake = loadDelphiStake;
exports.getTokenInfo = getTokenInfo;
exports.abiDecoder = abiDecoder;

exports.DelphiStakeFactory = DelphiStakeFactory;
