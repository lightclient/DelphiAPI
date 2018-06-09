const { cloneDeep, chain } = require('lodash'),
	  	// { getAsync } = require('./redis_config'),
	  	{ abiDecoder, getTransaction, getBlock, getTokenInfo } = require('./config/web3'),
			{ event_queue } = require('./config/rabbitmq');

async function sendEvents(events) {

	try {
		// TODO save this connection at a later point ...
		await event_queue.connect();

		let highestBlock;

		// only get the relevant information from each block and queue the result
		// to be processed in the event processor
		for (let event of events) {
			const rawTransaction = await getTransaction(event.transactionHash)

			// decodes the raw bytes into the transaction's parameters
			const rawContractMethodInputs = abiDecoder.decodeMethod(rawTransaction.input)

			// maps the transaction's paramerters to a nicer format
			const contractMethodInputs = chain(rawContractMethodInputs.params)
				.keyBy('name')
				.mapValues('value')
				.mapKeys((value, key) => key.substring(1))
				.value()

			// unsure if we even need these ... we'll figure out later
			// const blockData = await getBlock(blockNumber);
			// const eventTimestamp = blockData.timestamp.toString();

			// construct payload to place in queue
			let payload = {
				transactionHash: event.transactionHash,
				block: event.blockNumber,

				// the important stuff
				type: event.event,
				address: event.address,
				sender: rawTransaction.from,
				function: rawContractMethodInputs.name,
				params: contractMethodInputs,
				values: event.returnValues
			}

			// when a stake is created, check to see if the token associated with it
			// has a name, symbol, or decimal defined per EIP20 & add it to the payload.
			if(event.event == 'StakeCreated') {
				tokenInfo = await getTokenInfo(contractMethodInputs['token']);
				payload['token'] = tokenInfo;
			}

			// ** debug code ** //
			if (process.env['ENV'] == 'DEV') {
				console.log(payload);
				console.log("\n");
			}
			/* *************** */

			await event_queue.enqueue(payload)

			highestBlock = event.blockNumber
		}

		await event_queue.close()

		// return the highest process block
		return highestBlock

	} catch (error) {
		// let index handle and log the error
		throw error;
	}
}

module.exports.sendEvents = sendEvents;
