# Delphi API

This is were will store all relevant documentation for interacting with the Delphi API.

## Get Stake Info

Retrieves all relevant information regarding a stake.

**URL** : `/stake/:stake_address`

**Method** : `GET`

### Success Response

**Code** : `200 OK`

**Content examples**

If the `:stake_address` is valid and has been cached in the database, the API will return the following response.

```json
{
  "data": {
      "staker": "0x627306090abaB3A6e1400e9345bC60c78a8BEf57",
      "value": 100,
      "token": {
        "name": "DelphiCoin",
        "symbol": "DC",
        "address": "0x5ed8cee6b63b1c6afce3ad7c92f4fd7e1b8fad9f"
      },
      "minimum_fee": 5,
      "data": "QmWWQSuPMS6aXCbZKpEjPHPUZN2NjB3YrhJTHsV4X3vb2t",
      "claim_deadline": 1525417344,
      "arbiter": {
        "name": "",
        "description": "",
        "address": "0x498bad589c7acd871945ed6ca30b7bab0a977af7"
      },
      "whitelisted_claimants": [
        "0x5ed8cee6b63b1c6afce3ad7c92f4fd7e1b8fad9f",
        "0x498bad589c7acd871945ed6ca30b7bab0a977af7",
        "0x554f8e6938004575bd89cbef417aea5c18140d92"
      ],
      "claims": [
        {
          "id": 0,
          "amount": 25,
          "fee": 5,
          "surplus_fee": 0,
          "data": "QmT4AeWE9Q9EaoyLJiqaZuYQ8mJeq4ZBncjjFH9dQ9uDVA",
          "ruling": 0,
          "ruled": 0,
          "settlement_failed": 1
        }
      ],
      "settlements": [
        {
          "amount": 10,
          "staker_agrees": 0,
          "claimant_agrees": 0
        }
      ]
  },
  "errors": []
}

```

If no stake is found, the API will return the following message.

```json
{
  "data": {},
  "errors": [
    {
      "code": 400,
      "message": "Unknown stake address."
    }
  ]
}
```


## Get all Claims by a Sinle Challenger

Retrieves a list of claims and associated claim data for which the claim
has the specified address listed for the claimant on that claim

**URL** : `/claimant/<challenger address>`

**Method** : `GET`


## Get all Stakes by a Single Staker

Retrieves a list of stakes and associated stake data for which the stake
has the specified address listed for the staker

**URL** : `/staker/<staker address>`

**Method** : `GET`


## Get all Stakes for a Whitelistee

Retrieves a list of stakes and associated stake data for which the stake
has includes a whitelistee with the specififed address

**URL** : `/whitelistee/<whitelistee address>`

**Method** : `GET`


## Get all Claims for an Arbiter Set

Retrieves a list of claims and associated claim data for which the claim
has the specified address listed for the arbiter

**URL** : `/arbiter/<arbiter address>`

**Method** : `GET`




## Notes

* It is likely that we will break the `data` hashes into objects to represent the data stored on IPFS.
* Don't rely on any data about the arbiter except its address. The rest may be wishful thinking.
