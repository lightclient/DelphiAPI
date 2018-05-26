const redis = require('redis'),
	{ promisify } = require('util'),
	{ REDDIS_URL } = require('./constants');

const client = redis.createClient({ url: REDDIS_URL});

exports.getAsync = promisify(client.get).bind(client);
exports.writeAsync = promisify(client.set).bind(client);
