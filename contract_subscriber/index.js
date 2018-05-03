'use strict';

const delay = require('delay'),
	//  rollbar = require('./rollbar'),
	{ DelphiStake, DelphiVoting } = require('./web3_config'),
	//{ getAsync, writeAsync } = require('./redis_config'),
	{ sendEvents } = require('./eventsRetriever');

async function handler() {
	while (true) {
		try {
			// I use past events vs. subscribe in order to preserve ordering - FIFO
			// Also, subscribe is just polling - the socket connection does not provide the additional behavior, so these
			// are essentially accomplishing the same thing
			// let fromBlock = await getAsync('currentBlock') || 0;

			let fromBlock = 0;

			let voting_events = await DelphiVoting.getPastEvents({fromBlock, toBlock: 'latest'});
			let stake_events = await DelphiStake.getPastEvents({fromBlock, toBlock: 'latest'});

			// console.log("voting events:")
			// console.log(voting_events)
			//
			// console.log("staking events:")
			// console.log(stake_events)

			let eventBlock = await sendEvents(stake_events);

			// if (eventBlock) {
			// 	await writeAsync('currentBlock', eventBlock);
			// }

			process.exit(0)
			await delay(1000);

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
