# API Service

The API service is a tradition client-server architecture. It transmits data stored within its database upon request.

## Endpoints

The only endpoint currently implemented is the `stake` endpoint.

| Endpoint | Description   |
|-----------|--------------|
| `/stake/{stake_address}` | Returns all data pertaining to a stake |

For an in-depth look at the schema for each endpoint, check out the [API documentation](/docs/api.md).

## Tests

This service has a set of tests in the [test](/delphi_api/test) folder.
