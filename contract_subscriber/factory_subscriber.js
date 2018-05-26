'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ DelphiStakeFactory } = require('./config/web3'),
	{ getAsync, writeAsync } = require('./config/redis'),
	{ contract_queue } = require('./config/rabbitmq'),
	{ sendEvents } = require('./sender'),
	{ SUBSCRIBER_DELAY } = require('./config/constants');

async function handler() {
	try {
		for(let i = 0; i < 10; i++) {
			try {
				await contract_queue.connect();
			} catch(err) {
				console.log("Unable to connect, retrying...")
			}

			await delay(1000 * 2);
		}

		while (true) {
			// Use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide
			// the additional behavior, so these are essentially accomplishing the same thing
			let fromBlock = await getAsync('currentBlock') || 0;
			let factoryEvents = await DelphiStakeFactory.getPastEvents({fromBlock, toBlock: 'latest'});
			await processEvents(factoryEvents);
			let eventBlock = await sendEvents(factoryEvents);

			if (eventBlock) {
				await writeAsync('currentBlock', eventBlock + 1);
			}

			await delay(1000 * SUBSCRIBER_DELAY);
		}

		await contract_queue.close()

	} catch (err) {
	// include rollbar error message soon
	// rollbar.error(err);=
	console.log(err);

	// exit with error so kubernettes will automatically restart the job
	process.exit(1);
	}
}

// add new stake to the contract queue
async function processEvents(events) {
	for (let event of events) {
		if(event.event == 'StakeCreated') {
			await contract_queue.enqueue({
				address: event.returnValues._contractAddress,
				currentBlock: 0
			});
		}
	}
}

handler();
