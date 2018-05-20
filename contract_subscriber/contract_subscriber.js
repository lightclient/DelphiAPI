'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ loadDelphiStake } = require('./config/web3'),
	// { getAsync, writeAsync } = require('./config/redis'),
	{ contract_queue } = require('./config/rabbitmq'),
	{ sendEvents } = require('./sender');


let fromBlock = 0;

async function handler() {
	await contract_queue.connect();

	while (true) {
		try {

			// Use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide
			// the additional behavior, so these are essentially accomplishing the same thing

			// let fromBlock = await getAsync('currentBlock') || 0;
			//let voting_events = await DelphiVoting.getPastEvents({fromBlock, toBlock: 'latest'});

			console.log("getting tasks")
			// Consume tasks.
			const cancel = await contract_queue.consume(async (task) => {
			  console.log(task)

				let stake = loadDelphiStake(task.address);

				// retrieve all events from the DelphiStake contract
				let stakeEvents = await stake.getPastEvents({fromBlock, toBlock: 'latest'});

				console.log(stakeEvents)

				// send events to queue
				let eventBlock = await sendEvents(stakeEvents);

				if (eventBlock) {
					task.currentBlock = eventBlock;
				}

				await contract_queue.enqueue(task)
			  // Will be acknowledged when work() is done.
			});

			// Cancel consumer to stop receiving tasks.
			await cancel();

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

handler();
