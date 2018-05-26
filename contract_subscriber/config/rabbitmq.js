const { RABBITMQ_URL } = require('./constants')
const amqp = require('amqplib/callback_api');
const WorkQueue = require('wrappitmq').WorkQueue;

const event_queue = new WorkQueue({
	queue: 'delphi_events',
	url: RABBITMQ_URL
});

const contract_queue = new WorkQueue({
	queue: 'delphi_contracts',
	url: RABBITMQ_URL
});

exports.event_queue = event_queue;
exports.contract_queue = contract_queue;
