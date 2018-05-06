# DelphiStake Events

Each event that the DelphiStake and DelphiVoting smart contracts emit should be logged and recorded in the caching layer. I will try to break down each event and determine what should be don in each instance.

## Events

### Claimant Whitelisted
Before going into business with a staker, the staker's counterparty should expect to be "whitelisted for claims" such that a clear path exists for the adjudication of disputes should.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_claimant`  | `address` | address that was just whitelisted on the stake |

##### Action
When a new address is whitelisted on a stake, the system should update the stake's database entry and insert the potential claimant into the whitelisted table



### Claim Opened
Whitelisted claimant can use this function to make a claim for remuneration. Once opened, an opportunity for pre-arbitration settlement will commence, but claims cannot be unilaterally cancelled. Claims can only be opened for whitelisted individuals, however anyone may open a claim on a whitelisted individual's behalf (depositing the necessary fee for them). Claims can be opened directly to arbitration or to a settlement stage first.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_claimant`  | `address` | the address of who ever filed the claim (_**not nessesarily the claimant**_) |
|  `_claimId`  | `uint` | the index of the claim in the contract's `claims` array |

##### Action
If a new claim is opened, the system should insert the claim id and the sender of the claim in the claims table with a foreign key to the associated stake. It should also query the contract for the fee offered to arbiters and include that in the claims table.



### Fee Increased
Increase the arbiter fee being offered for this claim. Regardless of how the claim is ruled, this fee is not returned. The fee cannot be increased while still in the settlement phase, or after a ruling has been submitted.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_increasedBy`  | `address` | The address that increased the fee |
| `_claimId`      | `uint`    | ID associated with the claim in question |
| `_amount`       | `uint`    | Amount the claim fee was increased |

##### Action
Search the claims table for a claim with the same claimId on the associated contract and increase the fee by `_amount`.



### Settlement Proposed
Once a claim has been opened, either party can propose settlements to resolve the matter without getting the arbiter involved. If a settlement is accepted, both parties recover the fee they would otherwise forfeit in the arbitration process.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_proposedBy`   | `address` | The address which proposed a settlement |
| `_claimId`      | `uint`    | ID associated with the claim |
| `_settlementId` | `uint`    | ID associate with the settlement |

##### Action
Insert an entry in a settlement proposal table with the relevant information.



### Settlement Accepted
Once either party in a claim has proposed a settlement, the opposite party can choose to accept the settlement. The settlement proposer implicitly accepts, so only the counterparty needs to invoke this function.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_acceptedBy`   | `address` | The address that was just whitelisted on the stake |
| `_claimId`      | `uint`    | ID associated with the claim |
| `_settlementId` | `uint`    | ID associate with the settlement |

##### Action
Update the claim associated with the settlement that it has been ruled on and denote who accepted the settlement.



### Settlement Failed
Either party in a claim can call settlementFailed at any time to move the claim from settlement to arbitration.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_acceptedBy`   | `address` | The address that was just whitelisted on the stake |
| `_claimId`      | `uint`    | ID associated with the claim |
| `_settlementId` | `uint`    | ID associate with the settlement |

##### Action
Update the settlement associate with `_settlementId` and mark it as rejected.



### Claim Ruled
This function can only be invoked by the stake's arbiter, and is used to resolve the claim. Invoking this function will rule the claim and pay out the appropriate parties.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_claimId`      | `uint`    | ID associated with the claim |

##### Action
Find the associated claim and updated it with the ruling.

### Release Time Increased
Increases the deadline for opening claims.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_stakeReleaseTime`      | `uint`    | the unix time stamp (in seconds) before which claims may be opened |

##### Action
Updated the associated stake's release time accordingly.



### Stake Withdrawn
Denotes that the stake has been returned to the staker, but only if the claim deadline has elapsed and no open claims remain.

##### Event Parameters
None

##### Action
Updated the associated stake, denoting that it has been withdrawn and completely.



### Stake Increased
Increases the stake in this DelphiStake.

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `_value`  | `uint` | The number of tokens to transfer into this stake be opened |

##### Action
Updated the associated stake's value accordingly.
