const { cloneDeep, chain } = require('lodash')
const assert = require('chai').assert
const buildPayload = require('../sender').buildPayload



describe("Contract Subscriber", () => {
  it("should connect to the correct Ethereum network", function(){
     const ETH_NETWORK = require('../constants').ETH_NETWORK;
     assert.equal(ETH_NETWORK, 'deth');
  });
});

describe("Payload builder", () => {
  event = {
    transactionHash: '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
    blockNumber: 35,
    event: 'StakeCreated',
    address: '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10'
  }

  transaction = {
    from: '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    input: '0xb6298d4500000000000000000000000000000000000000000000000000000000000000640000000000000000000000008f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f000000000000000000000000000000000000000000000000000000000000000a00000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000000000000001ed09bead87c0378d8e63ffffffff000000000000000000000000baaa2a3237035a2c7fa2a33c76b44a8c6fe18e87000000000000000000000000000000000000000000000000000000000000000b69206c6f76652063617473000000000000000000000000000000000000000000'
  }

  it("should have correct transaction hash", () => {
    payload = buildPayload(event, transaction)
    assert(payload.transactionHash ==
      '0xe9aabe3feaf9fa8759ce2f86d673036c59b9a182398ee3c8913e4b4dea2b3e9b',
      'Transaction hash incorrect')
  })

  it("should have correct block number", () => {
    payload = buildPayload(event, transaction)
    assert(payload.block == '35', 'Block number incorrect')
  })

  it("should have correct event type", () => {
    payload = buildPayload(event, transaction)
    assert(payload.type, 'StakeCreated', 'Event type incorrect')
  })

  it("should have correct contract address", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address,
      '0x345cA3e014Aaf5dcA488057592ee47305D9B3e10',
      'Contract address incorrect')
  })

  it("should have correct sender address", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address,
      '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
      'Sender address incorrect')
  })

  it("should decode correct value", () => {
    payload = buildPayload(event, transaction)
    assert(payload.params.value,
      '100',
      'Value incorrect')
  })

  it("should decode correct token address", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address,
      '0x8f0483125fcb9aaaefa9209d8e9d7b9c8b9fb90f',
      'Token address incorrect')
  })

  it("should decode correct minimum fee", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address, '10', 'Minimum fee incorrect')
  })

  it("should decode correct data", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address, 'i love cats', 'Data incorrect')
  })

  it("should decode correct data", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address,
      '9.999999999999999999999999999999999e+33',
      'Stake release time incorrect')
  })

  it("should decode correct arbiter", () => {
    payload = buildPayload(event, transaction)
    assert(payload.address, '0xbaaa2a3237035a2c7fa2a33c76b44a8c6fe18e87', 'Arbiter incorrect')
  })




})
