# StandardBounties Data Schemas

## Summary

In an effort to manage the use of StandardBounties across several platforms, the schemas of the various `data` objects have been standardized.


## version 0.1
last changed: 19/01/22

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
    description: // A string representing that describes the reason for the claim
    claimant: {
       // persona for the issuer of the bounty
    },
    created: // the timestamp in seconds when the claim was created
    tokenSymbol: // the symbol for the token which the claim is of
    tokenAddress: // the address for the token which the claim is of (0x0 if ETH)

    // ------- add optional fields here -------
    sourceDirectoryHash: // The IPFS hash of the directory which holds all evidence
  },
  meta: {
    platform: // a string representing the original posting platform (ie 'gitcoin')
    schemaVersion: // a string representing the version number (ie '0.1')
    schemaName: // a string representing the name of the schema (ie 'standardSchema' or 'gitcoinSchema')
  }
}
```

Claim `data` Schema:
```
{
  payload: {
    description: // A string representing that describes the reason for the claim
    claimant: {
       // persona for the issuer of the bounty
    },
    created: // the timestamp in seconds when the claim was created
    tokenSymbol: // the symbol for the token which the claim is of
    tokenAddress: // the address for the token which the claim is of (0x0 if ETH)

    // ------- add optional fields here -------
    sourceDirectoryHash: // The IPFS hash of the directory which holds all evidence
  },
  meta: {
    platform: // a string representing the original posting platform (ie 'gitcoin')
    schemaVersion: // a string representing the version number (ie '0.1')
    schemaName: // a string representing the name of the schema (ie 'standardSchema' or 'gitcoinSchema')
  }
}
```

Bounty fulfillment `data` Schema:
```
{
  payload: {
    description: // A string representing the description of the fulfillment, and any necessary links to works
    sourceFileName: // A string representing the name of the file being submitted
    sourceFileHash: // A string representing the IPFS hash of the file being submitted
    sourceDirectoryHash: // A string representing the IPFS hash of the directory which holds the file being submitted
    fulfiller: {
      // persona for the individual whose work is being submitted
    }

    // ------- add optional fields here -------
  },
  meta: {
    platform: // a string representing the original posting platform (ie 'gitcoin')
    schemaVersion: // a string representing the version number (ie '0.1')
    schemaName: // a string representing the name of the schema (ie 'standardSchema' or 'gitcoinSchema')
  }
}
```

### version 0.0
last changed: 19/12/17
```
{
  title: // A string representing the title of the bounty
  description: // A string representing the description of the bounty, including all requirements
  sourceFileName: // A string representing the name of the file
  sourceFileHash: // The IPFS hash of the file associated with the bounty
  contact: // A string representing the preferred contact method of the issuer of the bounty
  categories: // an array of strings, representing the categories of tasks which are being requested
  githubLink: // The link to the relevant repository
}
```
