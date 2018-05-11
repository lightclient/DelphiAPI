# DelphiVoting Events

Each event that the DelphiStake and DelphiVoting smart contracts emit should be logged and recorded in the caching layer. I will try to break down each event and determine what should be don in each instance.

## Events

### Vote Committed
Commits a vote for the specified claim. Can be overwritten while commitPeriod is active

##### Event Parameters

| Attribute | Type | Description |
|-----------|------|-------------|
| `voter`  | `address` | address that corresponds to one of the arbiters in the arbiter set |
| `_claimId` | `bytes32` | ID associated with the claim being voted on

##### Action
Insert the voter's address into a votes table. Ensure that the vote hasn't already been recorded. If it has, then update the timestamps.
