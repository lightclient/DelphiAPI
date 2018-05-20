'use strict';

const delay = require('delay'),
	// rollbar = require('./rollbar'),
	{ DelphiStake, DelphiVoting } = require('./config/web3'),
	// { getAsync, writeAsync } = require('./config/redis'),
	{ sendEvents } = require('./sender');


let fromBlock = 0;

async function handler() {
	while (true) {
		try {

			// Use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide
			// the additional behavior, so these are essentially accomplishing the same thing

			// let fromBlock = await getAsync('currentBlock') || 0;
			//let voting_events = await DelphiVoting.getPastEvents({fromBlock, toBlock: 'latest'});


			// retrieve all events from the DelphiStake contract
			let stakeEvents = await DelphiStake.getPastEvents({fromBlock, toBlock: 'latest'});

			// console.log(stakeEvents)

			// send events to queue
			let highestBlock = await sendEvents(stakeEvents);

			if (highestBlock) {
				//await writeAsync('currentBlock', eventBlock);
				fromBlock = highestBlock + 1
			}

			console.log('Latest processed block', fromBlock)

			await delay(10000);

		} catch (err) {
			// include rollbar error message soon
			// rollbar.error(err);
			console.log(err);

			// exit with error so kubernettes will automatically restart the job
			process.exit(1);
		}
	}
}

handler();
