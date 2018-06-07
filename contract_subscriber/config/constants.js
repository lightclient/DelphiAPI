const networks = {
    'mainNet': 'https://mainnet.infura.io/U6bpkteiO0xMIuYeiHzk',
    'rinkeby': 'https://rinkeby.infura.io/U6bpkteiO0xMIuYeiHzk',
    'ropsten': 'https://ropsten.infura.io/U6bpkteiO0xMIuYeiHzk',
    'consensysrinkeby': 'https://rinkeby.infura.io/U6bpkteiO0xMIuYeiHzk',
    'localhost': 'localhost:8545',
    'deth': 'http://ganache:8545',
}

const ethNetwork = process.env['ETH_NETWORK'] || 'deth';

const subscriberDelay = process.env['SUBSCRIBER_DELAY'] || 10;

let rabbitmq_url = '';
let reddis_url = '';

if (process.env['ENV'] == 'DEV') {
  const user = process.env['RABBITMQ_DEFAULT_USER'];
  const pass = process.env['RABBITMQ_DEFAULT_PASS'];
  const host = process.env['RABBITMQ_HOST']
  const port = process.env['RABBITMQ_PORT'];
  rabbitmq_url = `amqp://${user}:${pass}@${host}:${port}`;

  reddis_url = `redis://${process.env['REDIS_HOST']}:${process.env['REDIS_PORT']}`;

} else {
  rabbitmq_url = process.env['RABBITMQ_BIGWIG_URL'];
  reddis_url  = process.env['REDIS_URL'];
}

exports.ETH_NETWORK = ethNetwork;
exports.ETH_NETWORK_URL = networks[ethNetwork];
exports.SUBSCRIBER_DELAY = subscriberDelay;
exports.RABBITMQ_URL = rabbitmq_url;
exports.REDDIS_URL = reddis_url;
