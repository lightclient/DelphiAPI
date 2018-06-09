stakeCreated = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'StakeCreated',
    'address': '0x912cB4e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    'params': {
         'value': '100',
         'token': '0xc662F94694B41CA821a7dcD09F0DE1fE83D91e3d',
         'minimumFee': '10',
         'data': 'i love cats',
         'stakeReleaseTime': '9.999999999999999999999999999999999e+33',
         'arbiter': '0xEF49B306959c68981902a9565063Ba1EE6566146'
    },
    'values': {
        '_contractAddress': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10'
    },
    'token': {
        'name': 'MattCoin',
        'symbol': 'MATT',
        'decimals': 10
    }
}

stakeCreated2 = {
    'transactionHash': '0xgHzabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 39,
    'type': 'StakeCreated',
    'address': '0x912cB4e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    'params': {
         'value': '100',
         'token': '0xc662F94694B41CA821a7dcD09F0DE1fE83D91e3d',
         'minimumFee': '10',
         'data': 'hi i am matt',
         'stakeReleaseTime': '9.999999999999999999999999999999999e+33',
         'arbiter': '0xEF49B306959c68981902a9565063Ba1EE6566146'
    },
    'values': {
        '_contractAddress': '0x9390BCAc10a3FE3B85947A5780d68a2c805dEA64'
    },
    'token': {
        'name': 'MattCoin',
        'symbol': 'MATT',
        'decimals': 10
    }
}

claimantWhitelisted = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimantWhitelisted',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    'params': {
         'claimant': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
         'deadline': '1589280934319',
    }
}

claim1 = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimOpened',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    'params': {
         'claimant': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
         'amount': '1',
         'fee': '10',
         'data': 'i love cats',
         'arbiter': '0xEF49B306959c68981902a9565063Ba1EE6566146'
    },
    'values': {
        '_claimId': '0'
    },
    'function': 'openClaim'
}

claim1 = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimOpened',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    'params': {
         'amount': '1',
         'fee': '10',
         'data': 'i love cats'
    },
    'values': {
        '_claimId': '0',
        '_claimant': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    },
    'function': 'openClaim'
}

claim2 = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimOpened',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    'params': {
         'amount': '2',
         'fee': '9',
         'data': 'you are bad!!'
    },
    'values': {
        '_claimId': '0',
        '_claimant': '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
    },
    'function': 'openClaim'
}

ruleOnClaim1 = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ClaimRuled',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xEF49B306959c68981902a9565063Ba1EE6566146',
    'params': {
         ''
    }
}


releaseTimeIncreased = {
    'transactionHash': '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    'block': 35,
    'type': 'ReleaseTimeIncreased',
    'address': '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
    'sender': '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    'params': {
         'stakeReleaseTime': '1589280934319'
    }
}
