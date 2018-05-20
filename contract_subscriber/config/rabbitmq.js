const amqp = require('amqplib/callback_api');
const WorkQueue = require('wrappitmq').WorkQueue;

const event_queue = new WorkQueue({
	queue: 'delphi_events',
	url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672'
});

const contract_queue = new WorkQueue({
	queue: 'delphi_contracts',
	url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672'
});

exports.event_queue = event_queue;
exports.contract_queue = contract_queue;
