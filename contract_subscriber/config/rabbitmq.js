const amqp = require('amqplib/callback_api');
const WorkQueue = require('wrappitmq').WorkQueue;

const queue = new WorkQueue({
	queue: 'delphi_events', // Name of the queue to use. (Default: workqueue)
	url: 'amqp://rabbitmq:rabbitmq@rabbitmq:5672' // Can also be specified on connect()
});

exports.queue = queue
