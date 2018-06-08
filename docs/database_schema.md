# Database Schema

* [Stakes](#stake-table)
* [Whitelist](#whitelist-table)
* [Claims](#claims-table)
* [Tokens](#token-table)
* [Settlements](#settlement-table)
* [Arbiters](#arbiter-table)


### Stake Table
| Column Name      | Type         | Description                                           |
|------------------|--------------|-------------------------------------------------------|
| address          | address      | the stake's address                                   |
| staker           | address      | the address of the stake's owner                      |
| claimable stake  | integer      | value of the stake in units of token                  |
| data             | string       | IPFS hash of data                                     |
| minimum_fee      | integer      | the minimum fee for each claim                        |
| claim_deadline   | integer      | unix time (in seconds) of the claim deadline          |
| token_id         | foreign key  | key to stake's token (address) in the token table     |
| token            | relationship | Token relationship (table of tokens)                  |
| arbiter_id       | foreign key  | key to stake's arbiter (address) in the arbiter table |
| arbiter          | relationship | Arbiter relationship (table of arbiters)              |
| whitelist        | relationship | Whitelistee relationship (table of whitelistees)      |
| claims           | relationship | Claims relationship (table of claims)                 |
| update_time      | date         | time the database entry was last modified             |
| create_time      | date         | the time the database entry was created               |


### Whitelistee Table
| Column Name | Type    | Description                                             |
|-------------|---------|---------------------------------------------------------|
| stake       | address | stake the claimant is associated with                   |
| claimant    | address | address of claimant                                     |
| deadline    | integer | earliest date in unix time that claimant can open claim |
| update_time | date    | time the database entry was last modified               |
| create_time | date    | the time the database entry was created                 |


### Claim Table
| Column Name       | Type        | Description                                           |
|-------------------|-------------|-------------------------------------------------------|
| stake             | address     | stake the claim is associated with                    |
| index             | integer     | index of claim in contract's claim array              |
| claimant          | address     | address of claimant                                   |
| amount            | integer     | amount being claimed in units of the stake's token    |
| arbiter           | foreign key | key to stake's arbiter (address) in the arbiter table |
| fee               | integer     | the minimum fee                                       |
| surplus_fee       | integer     | the amount paid in addition to the minimum fee        |
| data              | string      | IPFS of claim's evidence                              |
| ruling            | integer     | ruling code for claim                                 |
| ruled             | bool        | whether the claim has been ruled on yet or not        |
| settlement_failed | bool        | whether the settlement succeeded or not               |
| update_time       | date        | time the database entry was last modified             |
| create_time       | date        | the time the database entry was created               |


### Token Table
| Column Name | Type    | Description                               |
|-------------|---------|-------------------------------------------|
| address     | address | the EIP20's address                       |
| name        | string  | vanity name of token                      |
| symbol      | string  | vanity symbol of token                    |
| decimals    | integer | the precision of the token                |
| update_time | date    | time the database entry was last modified |
| create_time | date    | the time the database entry was created   |


### Settlement Table
| Column Name | Type        | Description                                             |
|-------------|-------------|---------------------------------------------------------|
| claim       | foreign key | foreign key of claim this settlement is associated with |
| sender      | address     | address of user who opened the claim                    |
| created     | date        | the time the database entry was created                 |
| update_time | date        | time the database entry was last modified               |
| create_time | date        | the time the database entry was created                 |


### Arbiter Table
| Column Name | Type    | Description                               |
|-------------|---------|-------------------------------------------|
| address     | address | the arbiter's address                     |
| name        | string  | name of the arbiter group                 |
| description | string  | description of the arbiter group          |
| update_time | date    | time the database entry was last modified |
| create_time | date    | the time the database entry was created   |
