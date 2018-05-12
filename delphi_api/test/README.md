# API Server Testing


## Smoke Test
[smokeTest.sh](smokeTest.sh)

A backend smoke test to quickly verify that the PostgreSQL database and API Server are working together.

1. Spins up docker containers for the PostgreSQL database and API server.
2. Calls migrate.py to populate the database with a dummy Stake and dummy Whitelistee
3. Makes GET requests to the local API server using touchMainEndpoint.sh and touchSeededStake.sh
4. Verifies that entries were successfully added to the DB and retrieved by the server.


Usage:
```
./smokeTest.sh
```
