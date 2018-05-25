'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ loadDelphiStake } = require('./config/web3'),
	// { getAsync, writeAsync } = require('./config/redis'),
	{ contract_queue } = require('./config/rabbitmq'),
	{ sendEvents } = require('./sender');


let fromBlock = 0;

/*
@param fn - the function you want to backoff
@param retries - the number of times to retry the function
@param wait - the time to wait between tries in second
// */
// async function backoff(fn, retries, wait) {
// 	for(let i = 0; i < retries; i++) {
// 		try {
// 			await fn();
// 		} catch(err) {
// 			console.log("Unable to connect, retrying...")
// 		}
//
// 		await delay(1000 * wait);
// 	}
// }

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

			// Cancel consumer to stop receiving tasks.
			await consumer();

			await delay(5000);
		}

		await contract_queue.close()
	} catch (err) {
			// rollbar.error(err);
			console.log(err);

			// exit with error so kubernettes will automatically restart the job
			process.exit(1);
	}
}

handler();
