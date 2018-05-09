const { cloneDeep, chain } = require('lodash'),
	  // { getAsync } = require('./redis_config'),
	  // { SQS_PARAMS } = require('./constants'),
	  { abiDecoder, getTransaction, getBlock } = require('./web3_config'),
	   // sqs = require('./sqs_config')
		 { pretty_print } = require('./utils.js');

const amqp = require('amqplib/callback_api');
const WorkQueue = require('wrappitmq').WorkQueue;

const queue = new WorkQueue({
	queue: 'delphi_events', // Name of the queue to use. (Default: workqueue)
	url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672' // Can also be specified on connect()
});



async function sendEvents(events) {
	try {
		await queue.connect();

		let highestBlock;
		for (let event of events) {

			const transactionHash = event.transactionHash
			const blockNumber = event.blockNumber
			const eventName = event.event
			const rawTransaction = await getTransaction(transactionHash);
			const transactionFrom = rawTransaction.from;
			const rawContractMethodInputs = abiDecoder.decodeMethod(rawTransaction.input);
			const contractMethodInputs = chain(rawContractMethodInputs.params)
				.keyBy('name')
				.mapValues('value')
				.mapKeys((value, key) => key.substring(1))
				.value();
			const blockData = await getBlock(blockNumber);
			const eventTimestamp = blockData.timestamp.toString();

			const payload = {
				transactionHash: event.transactionHash,
				block: event.blockNumber,
				type: event.event,
				address: event.address,
				sender: rawTransaction.from,
				params: contractMethodInputs,
			}

			console.log(contractMethodInputs)
			// console.log("%o", event.returnValues)
			// console.log("%o", rawContractMethodInputs.params)

			// pretty_print([
			// 	["Transaction Hash", transactionHash],
			// 	["Block Number", blockNumber],
			// 	["Event Name", eventName],
			// 	["Address", event.address],
			// 	["Raw Transaction", rawTransaction],
			// 	["Transaction From", rawTransaction.from],
			// 	["Raw Contract Methods", rawContractMethodInputs],
			// 	["Contract Method Inputs", contractMethodInputs],
			// 	["Block Data", blockData],
			// 	["Event Timestamp", eventTimestamp],
			// ])

			await queue.enqueue(payload);


			highestBlock = blockNumber;
		}

		await queue.close();

		return highestBlock;
	} catch (error) {
		// let index handle and log the error
		throw error;
	}
}

module.exports.sendEvents = sendEvents;
