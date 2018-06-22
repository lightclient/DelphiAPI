'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ loadDelphiStake } = require('./config/web3'),
	// { getAsync, writeAsync } = require('./config/redis'),
	{ contract_queue } = require('./config/rabbitmq'),
	{ sendEvents } = require('./sender')

const SUBSCRIBER_DELAY = process.env['SUBSCRIBER_DELAY'] || 10;

let fromBlock = 0;

async function handler() {
	try {
		while (true) {
			// connect to queue each time so that unacked messages are redelivered
			await contract_queue.connect();

			// poll the next contract on the queue
			const consumer = await contract_queue.consume(async (task) => {
				console.log(task)

				let stake = loadDelphiStake(task.address);

				// retrieve all events from the DelphiStake contract
				let stakeEvents = await stake.getPastEvents({fromBlock: task.currentBlock, toBlock: 'latest'});

				// send events to queue
				let eventBlock = await sendEvents(stakeEvents);

				if (eventBlock) {
					task.currentBlock = eventBlock + 1;
				}

				await contract_queue.enqueue(task)
			});

			await consumer(); // cancel consumer to stop receiving tasks
			await delay(1000 * SUBSCRIBER_DELAY);
			await contract_queue.close()
		}
	} catch (err) {
			// rollbar.error(err);
			console.log(err);

			// exit with error so kubernettes will automatically restart the job
			process.exit(1);
	}
}

handler();
