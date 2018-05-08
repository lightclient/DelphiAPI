# Database Schema

* [Stakes](#stake-table)
* [Whitelist](#whitelist-table)
* [Claims](#claims-table)
* [Tokens](#token-table)
* [Settlements](#settlement-table)
* [Arbiters](#arbiter-table)

### Stake Table

| Column Name      | Type         | Description |
|------------------|--------------|-------------|
| staker           | address      | the stake's owner |
| value            | integer      | value of the stake in units of token |
| token            | foreign key  | key to stake's token (address) in the token table |
| minimum_fee      | integer      | the minimum fee for each claim |
| data             | string       | IPFS hash of data ? |
| claim_deadline   | integer      | unix time (in seconds) of the claim deadline |
| arbiter          | foreign key  | key to stake's arbiter (address) in the arbiter table |
| whitelist        | foreign key  | key to stake's whitelisted claimants in other table |
| claims           | foreign key  | key to stake's claims in claims table |
| settlements      | foreign key  | key to stake's settlements in settlements table |
| created          | date         | the time the database entry was created |
| modified         | date         | time the database entry was last modified |
| initialized_time | integer      | unix time (in seconds) that the stake was initialized


### Whitelist Table
| Column Name      | Type         | Description |
|------------------|--------------|-------------|
| claimant         | address      | address of claimant |
| deadline         | integer      | earliest date in unix time that claimant can open claim |
| created          | date         | the time the database entry was created |
| modified         | date         | time the database entry was last modified |
| stake            | address      | stake the claimant is associated with |


### Claims Table
| Column Name      | Type         | Description |
|------------------|--------------|-------------|
| claimant         | address      | address of claimant |
| sender           | address      | address of user who opened the claim |
| id               | integer      | index of claim in contract's claim array |
| surplus_fee      | integer      | the amount paid in addition to the minimum fee |
| data             | string       | IPFS of claim's evidence |
| ruling           | integer      | ruling code for claim |
| ruled            | bool         | whether the claim has been ruled on yet or not |
| settlement_failed| bool         | whether the settlement succeeded or not |
| created          | date         | the time the database entry was created |
| modified         | date         | time the database entry was last modified |
| stake            | address      | stake the claim is associated with |

### Token Table
| Column Name | Type     | Description |
|-------------|----------|-------------|
| address     | address  | the EIP20's address |
| name        | string   | vanity name of token |
| symbol      | string   | vanity symbol of token |
| decimals    | integer  | the precision of the token
| created     | date     | the time the database entry was created |
| modified    | date     | time the database entry was last modified |


### Settlement Table (work in progress)

| Column Name      | Type         | Description |
|------------------|--------------|-------------|
| claim            | foreign key  | foreign key of claim this settlement is associated with |
| sender           | address      | address of user who opened the claim |
| created          | date         | the time the database entry was created |
| modified         | date         | time the database entry was last modified |
| stake            | address      | stake the claim is associated with |

### Arbiter Table
| Column Name | Type     | Description |
|-------------|----------|-------------|
| address     | address  | the arbiter's address |
| name        | string   | name of the arbiter group |
| description | string   | description of the arbiter group |
| created     | date     | the time the database entry was created |
| modified    | date     | time the database entry was last modified |
