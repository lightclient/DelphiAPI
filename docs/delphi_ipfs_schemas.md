# StandardBounties Data Schemas

## Summary

In an effort to manage the use of Delphi across several platforms, the schemas of the various `data` objects have been standardized.


## version 0.1

Persona Schema:
```
{
   name: // optional - A string representing the name of the persona
   email: // optional - A string representing the preferred contact email of the persona
   githubUsername: // optional - A string representing the github username of the persona
   address: // required - A string web3 address of the persona
}
```

Claim `data` Schema:
```
{
  payload: {
    description: // a string representing that describes the reason for the claim
    claimant: {
       // persona for the claimant of the stake
    },
    created: // the timestamp in seconds when the claim was created
    tokenSymbol: // the symbol for the token which the claim is of
    tokenAddress: // the address for the token which the claim is of (0x0 if ETH)

    // ------- add optional fields here -------
    sourceDirectoryHash: // the IPFS hash of the directory which holds all evidence
  },
  meta: {
    platform: // a string representing the original posting platform (ie 'gitcoin')
    schemaVersion: // a string representing the version number (ie '0.1')
    schemaName: // a string representing the name of the schema (ie 'standardSchema' or 'gitcoinSchema')
  }
}
```
