# Contract Subscriber

The factory and contract subscriber are lightweight micro-services that connects directly to the Ethereum network.

## Events

The Delphi smart contract can emit many different types of events. For simplicity sake, the subscribers do not do any processing on the events they receives. They pass all relevant data to the [event processor](/delphi_api/app/event_processor) for that. This keeps it very lightweight and easily distributable.

###### Event Schemata
* [DelphiStake events](/docs/delphi_stake.md)
* [DelphiVoting events](/docs/delphi_voting.md)

## Payload

All received evens are passed in a payload object to the [event processor](/delphi_api/app/event_processor) using RabbitMQ. The object's schema is show below.

| Attribute | Type | Description |
|-----------|------|-------------|
| `type`    | `string`  | the type of event |
| `address` | `address` | the contract's address |
| `sender`  | `address` | the address of whoever initiated the event   |
| `params`  | `json`    | all the parameters passed into the smart contract |
| `values`  | `json`    | all values emitted from contract event |
| `function`| `string`  | contract function invoked |
