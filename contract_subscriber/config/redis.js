const redis = require('redis'),
	{ promisify } = require('util');

const client = redis.createClient({ url: `redis://${process.env['REDIS_HOST']}:${process.env['REDIS_PORT']}`});

exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
