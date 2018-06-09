# Delphi-API

The Delphi API is a caching layer for the [Delphi](https://github.com/Bounties-Network/Delphi) smart contract. It is a fast way to data written on the Ethereum blockchain. This allows the [Delphi user interface](https://github.com/BKDaugherty/delphi-unchained) to provide a better experience for users.

## Index

* [Develop Prerequisites](/docs/development_prerequisites.md)
* [Installation & Setup](#setup)
* [API Schmea](/docs/api.md)
* [System Architecture](#api-schema-and-documentation)
  * [Contract Subscriber](/contract_subscriber)
  * [Event Processor](/delphi_api/app/event_processor)
  * [API](/delphi_api)
* [Tests](/docs/testing.md)

## Setup
Before starting you'll need [Docker](https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac) up and running on your machine.

The caching layer can currently be attached to Rinkeby, Ropsten, and a localhost Ethereum network. Please modify the environment variable in the [variables.env](variables.env) file to which ever network you choose. After that, you'll be ready to start the API up.

###### Running the caching layer
```
git clone https://github.com/c-o-l-o-r/DelphiAPI.git
cd DelphiAPI
docker-compose up --build
```

###### Starting Up A Private Ethereum Blockchain & Delphoying Delphi Smart Contracts
```
git clone https://github.com/c-o-l-o-r/deth.git
cd deth/dapp
git clone https://github.com/BKDaugherty/delphi-unchained.git
cd ..
docker-compose up --build
docker exec -it deth_dapp_1 bash
root@deth_dapp: cd delphi-unchained
root@deth_dapp: npm install
root@deth_dapp: truffle install
root@deth_dapp: yarn contract
```

Locally, you will now be syncing directly from the contract. You may access the api at:

http://locahost:5000

If you add additional packages to a package.json or requirements.txt file, you'll need to rebuild the individual service.  To rebuild all services, you may run:
```
docker-compose down
docker-compose build
docker-compose up
```

## API Schema and Documentation

We plan to closely follow the architecture described in the [BountiesAPI repo](https://github.com/Bounties-Network/BountiesAPI).

## Architecture

![Architecture Diagram](/docs/images/architecture.jpg)

The **frontend or client** can be any third party service or collaborator that integrates with the [delphi ethereum contract](https://github.com/Bounties-Network/Delphi).  This API works as a caching and storage layer for what is input into the standard bounties contract. Due to storage costs, the contract puts the majority of the data into IPFS. To understand further, read the documentation on the [Delphi contract](https://github.com/Bounties-Network/Delphi).

The [**contract & factory subscribers**](/contract_subscriber) listen for events from the contracts. In the case a resync is occurring, it will listen to all historical events, starting from the genesis block. In order for the subscriber to know what it has already accessed, the redis cache stores a currentBlock key. When the subscriber picks up on a new event, it looks up the original transaction via web3 and passes the event data along with the original contract function inputs to RabbitMQ. A RabbitMQ fifo queue is used. This means we will never have duplication on keys and all events will be handled in the order they come through.

The [**delphi subscriber**](/delphi_api/app/event_processor) listens to events that have been passed into RabbitMQ by the contract subscriber.  The delphi subscriber uses the data from the event, the inputs to the original contract function, and the IPFS stored data to write the appropriate values to the DB via SQLAlchemy.

The [**delphi api**](/delphi_api) is a falcon API that serves the data that has been written by the delphi subscriber and other running jobs.
