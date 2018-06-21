const amqp = require('amqplib/callback_api');
const WorkQueue = require('wrappitmq').WorkQueue;

RABBITMQ_URL = process.env['RABBITMQ_BIGWIG_URL'] || 'amqp://guest:guest@localhost:5672';

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
