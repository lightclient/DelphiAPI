# API Service

The API service is a traditional client-server architecture. It transmits data stored within its database upon request.

## Endpoints

The only endpoint currently implemented is the `stake` endpoint.

| Endpoint | Description   |
|-----------|--------------|
| `/stake/{stake_address}` | Returns all data pertaining to a stake |
| `/claimant/{claimant_address}` | Returns information about stakes the claimant is involved with. |
| `/staker/{staker_address}` | Returns all the stakes associated with a staker |
| `/whitelistee/{whitelistee_address}` | Returns all stakes someone is whitelisted on |
| `/arbiter/{arbiter_address}` | Returns all stakes that someone is listed as the arbiter to |

For an in-depth look at the schema for each endpoint, check out the [API documentation](/docs/api.md).

## Tests

This service has a set of tests in the [test](/delphi_api/test) folder.
