const { cloneDeep, chain } = require('lodash'),
	  	// { getAsync } = require('./redis_config'),
	  	{ abiDecoder, getTransaction, getBlock } = require('./config/web3'),
			{ queue } = require('./config/rabbitmq')

async function sendEvents(events) {

	try {
		// TODO save this connection at a later point ...
		await queue.connect();

		let highestBlock;
		for (let event of events) {

			// retrieves a transaction object
			const rawTransaction = await getTransaction(event.transactionHash)

			// build payload to send to queue using the event
			const payload = buildPayload(event, rawTransaction)

			// send payload to queue
			await queue.enqueue(payload)

			highestBlock = event.blockNumber
		}

		await queue.close()

		// return the highest process block
		return highestBlock

	} catch (error) {
		// let index handle and log the error
		throw error;
	}
}

function buildPayload(event, transaction) {

	try {

		// decodes the raw bytes into the transaction's parameters
		const rawContractMethodInputs = abiDecoder.decodeMethod(transaction.input)

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
		const payload = {
			transactionHash: event.transactionHash,
			block: event.blockNumber,

			// the important stuff
			type: event.event,
			address: event.address,
			sender: transaction.from,
			params: contractMethodInputs,
		}

		// ** debug code ** //
		if (process.env['ENV'] == "DEV") {
			console.log('Type: ', payload.type)
			console.log('Contract Address: ', payload.address)
			console.log('Sender: ', payload.sender)
			console.log('contract Methods: %o', contractMethodInputs)
		}
		/* *************** */

		return payload

	} catch (error) {
		// let index handle and log the error
		throw error;
	}


}

module.exports.sendEvents = sendEvents;
module.exports.buildPayload = buildPayload;
