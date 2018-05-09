const networks = {
    'mainNet': 'https://mainnet.infura.io/',
    'rinkeby':  'https://rinkeby.infura.io/',
    'consensysrinkeby': 'https://rinkeby.infura.io/',
    'localhost': 'localhost:8545',
    'deth': 'http://ganache:8545',
}

const ethNetwork = process.env['ETH_NETWORK'] || 'deth';

exports.ETH_NETWORK = ethNetwork;
exports.ETH_NETWORK_URL = networks[ethNetwork];
