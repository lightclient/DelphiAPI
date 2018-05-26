const ds_json = require('../contracts/DelphiStake.json'),
		dv_json = require('../contracts/DelphiVoting.json'),
		df_json = require('../contracts/DelphiStakeFactory.json'),
	  Web3 = require('web3'),
	  abiDecoder = require('abi-decoder'),
	  { ETH_NETWORK, ETH_NETWORK_URL } = require('./constants');

// web3 setup
const web3 = new Web3(ETH_NETWORK_URL);

const factoryAddress = process.env['ENV'] == 'DEV' ? '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f' : '0xcac53a387d8e38c10a6a077482bd1741340e4e6e'

const DelphiStakeFactory = new web3.eth.Contract(
	df_json.abi,
	factoryAddress
);

// const DelphiStake = new web3.eth.Contract(
// 	ds_json.abi,
// 	'0x345ca3e014aaf5dca488057592ee47305d9b3e10'
// 	//'0x13c72f3c8bc7afc2609a9da61a0d185c50085cf8'
// );
//
// const DelphiVoting = new web3.eth.Contract(
// 	dv_json.abi,
// 	'0xbaaa2a3237035a2c7fa2a33c76b44a8c6fe18e87'
// )

function loadDelphiStake(address) {
	return new web3.eth.Contract(
		ds_json.abi,
		address
	);
}

abiDecoder.addABI(ds_json.abi);
abiDecoder.addABI(df_json.abi);
//abiDecoder.addABI(dv_json.abi);

exports.getTransaction = web3.eth.getTransaction;
exports.getBlock = web3.eth.getBlock;
exports.abiDecoder = abiDecoder;
// exports.DelphiStake = DelphiStake;
// exports.DelphiVoting = DelphiVoting;
exports.DelphiStakeFactory = DelphiStakeFactory;
exports.loadDelphiStake = loadDelphiStake;
exports.web3 = web3;
