const redis = require('redis'),
	{ promisify } = require('util'),

REDIS_URL = process.env['REDIS_URL'] || 'redis://localhost:6379';

const client = redis.createClient({ url: REDIS_URL});

exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
