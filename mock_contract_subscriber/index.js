'use strict';

const amqp = require('amqplib/callback_api');

async function handler() {

	const WorkQueue = require('wrappitmq').WorkQueue;

	const queue = new WorkQueue({
	  queue: 'delphi-events', // Name of the queue to use. (Default: workqueue)
	  url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672' // Can also be specified on connect()
	});

	await queue.connect();

	queue.on('error', (err) => {
	  // Something went wrong and you should log it.
		console.log('Queue error')
	});
	queue.on('close', (err) => {
	  // The connection was closed and the queue is no longer usable.
	  // An err is given if the connection was closed due to an error.
		console.log('Queue closed')
	});

	const claimant_whitelisted = {
		eventName: 'ClaimantWhitelisted',
		eventTimeStamp: '1525330759',
		contractMethodInputs: JSON.stringify({ claimant: "0x627306090abaB3A6e1400e9345bC60c78a8BEf57"}),
		transactionFrom: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
	}

	// Enqueue a task.
	await queue.enqueue(claimant_whitelisted);
	await queue.close();
	process.exit(0)
}

handler()
