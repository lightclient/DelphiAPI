'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ DelphiStakeFactory } = require('./config/web3'),
	{ getAsync, writeAsync } = require('./config/redis'),
	{ contract_queue } = require('./config/rabbitmq'),
	{ sendEvents } = require('./sender');

async function handler() {
	await contract_queue.connect();

	while (true) {
		try {
			// Use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide
			// the additional behavior, so these are essentially accomplishing the same thing
			// let fromBlock = await getAsync('currentBlock') || 0;
			let fromBlock = 0;
			let factoryEvents = await DelphiStakeFactory.getPastEvents({fromBlock, toBlock: 'latest'});
			await processEvents(factoryEvents);
			let eventBlock = await sendEvents(factoryEvents);

			if (eventBlock) {
				await writeAsync('currentBlock', eventBlock + 1);
			}

			await delay(10000);

		} catch (err) {
			// include rollbar error message soon
			// rollbar.error(err);
			console.log(err);

			// exit with error so kubernettes will automatically restart the job
			process.exit(1);
		}
	}

	await contract_queue.close()
}

async function processEvents(events) {
	for (let event of events) {
		if(event.event == 'StakeCreated') {
			// console.log(`${event.blockNumber} StakeCreated: ${event.returnValues._contractAddress}`);

			// send payload to queue
			await contract_queue.enqueue({
				address: event.returnValues._contractAddress,
				currentBlock: 0
			});
		}
	}
}

handler();
