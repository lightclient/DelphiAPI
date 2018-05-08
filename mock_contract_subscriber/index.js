'use strict';

const amqp = require('amqplib/callback_api');

async function handler() {

	const WorkQueue = require('wrappitmq').WorkQueue;

	const queue = new WorkQueue({
	  queue: 'delphi_events', // Name of the queue to use. (Default: workqueue)
	  url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672' // Can also be specified on connect()
	});

	await queue.connect();

	queue.on('error', (err) => {
	  // Something went wrong and you should log it.
		console.log('Queue error')
	});
	queue.on('close', (err) => {
	  // The connection was closed and the queue is no longer usable.
	  // An err is given if the connection was closed due to an error.
		console.log('Queue closed')
	});

	// const new_stake = {
	// 	logIndex: 1,
  //   transactionIndex: 0,
  //   transactionHash: '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
  //   blockHash: '0xd3a0b22d40a1e019d9c4ae9e1c5b32bdf1f8aaa6edb85b90529d4dfdf649f563',
  //   blockNumber: 35,
  //   address: '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
  //   type: 'mined',
  //   id: 'log_f9bf09fc',
  //   returnValues:
  //   Result {
  //      '0': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
  //      '1': '100',
  //      '2': '0x8f0483125FCb9aaAEFA9209D8E9d7b9C8B9Fb90F',
  //      '3': '10',
  //      '4': 'i love cats',
  //      '5': '9999999999999999999999999999999999',
  //      '6': '0xbaAA2a3237035A2c7fA2A33c76B44a8C6Fe18e87',
  //      _staker: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
  //      _claimableStake: '100',
  //      _token: '0x8f0483125FCb9aaAEFA9209D8E9d7b9C8B9Fb90F',
  //      _minimumFee: '10',
  //      _data: 'i love cats',
  //      _stakeReleaseTime: '9999999999999999999999999999999999',
  //      _arbiter: '0xbaAA2a3237035A2c7fA2A33c76B44a8C6Fe18e87'
	// 	 },
  //   event: 'StakeCreated',
  //   signature: '0xe6bf11c9793a7afd9e69a81cf800a910e6b4745469831f41652cc2c69e55d796',
  //   raw: {
	// 		data: '0x000000000000000000000000627306090abab3a6e1400e9345bc60c78a8bef5700000000000000000000000000000000000000000000000000000000000000640000000000000000000000008f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000e0000000000000000000000000000000000001ed09bead87c0378d8e63ffffffff000000000000000000000000baaa2a3237035a2c7fa2a33c76b44a8c6fe18e87000000000000000000000000000000000000000000000000000000000000000b69206c6f76652063617473000000000000000000000000000000000000000000',
  //   	topics: [Array]
	// 	}
	// }

	const new_stake = {
		type: 'StakeCreated',
		address: '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
		staker: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
		claimable_stake: '100',
		token: '0x8f0483125FCb9aaAEFA9209D8E9d7b9C8B9Fb90F',
		minimum_fee: '10',
		data: 'i love cats',
		release_time: '1525421121',
		arbiter: '0xbaAA2a3237035A2c7fA2A33c76B44a8C6Fe18e87'
	}

	const claimant_whitelisted = {
		type: 'ClaimantWhitelisted',
		stake: '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
		claimant: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
		deadline: '1525330759',
		transaction_from: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
	}

	// Enqueue a task.
	await queue.enqueue(new_stake);
	await queue.enqueue(claimant_whitelisted);
	await queue.close();
	process.exit(0)
}

handler()
