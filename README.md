[![PyPI version](https://badge.fury.io/py/pytrium.svg)](https://badge.fury.io/py/pytrium) [![Build Status](https://travis-ci.org/phantomxc/pytrium.svg?branch=master)](https://travis-ci.org/phantomxc/pytrium)

Pytrium
=======

Pytrium is a Python 2/3 client library for the MX Atrium API.

## Table of Contents

- [pytrium](#pytrium)
  * [Installation](#installation)
  * [Requires](#requires)
  * [Documentation](#documentation)
  * [Quickstart](#quickstart)
  * [Api Methods](#api-methods)
    + [Users](#users)
    + [Transactions](#transactions)
    + [Accounts](#accounts)
    + [Institutions](#institutions)
    + [Members](#members)
    + [Holdings](#holdings)
  * [Contribute](#contribute)
  * [License](#license)

## Installation
```
pip install pytrium
```

## Requires
 * requests
 * future

## Documentation
This client library wraps all the available endpoints of the MX Atrium API. For additional information regarding data attributes, available query parameters, and typical work flows, visit the full documentation at https://atrium.mx.com/documentation

## Quickstart
1. First you'll need to create a free developer account at [https://atrium.mx.com](https://atrium.mx.com). This will provide you with a `MX-API-KEY` and `MX-CLIENT-ID`, both of which are required to hit the API. Please keep this information confidential.

2. Create your API instance.
  ```python
  from atrium import Api,

  api = Api(key="SAMPLE_KEY_XXX", client_id="SAMPLE_CLIENT_ID_XXX")
  ```


3. Create a user. See the [Docs](http://atrium.mx.com/documentation) for more options.
  ```python
  import json

  user = api.createUser(payload={
    "identifier": "U123987",
    "metadata": json.dumps({
      "first_name": "Charles",
      "last_name": "Xavier",
      "email": "professor@mx.com"
    })
  })
  ```

4. Find the institution the user banks at.
  ```python
  query = api.getInstitutions(queryParams={
    "name": "Awesome Bank"
  })
  institution = query['institutions'][0]
  ```

5. Get the required credentials for a specific institution via the `guid`.
  ```python
  creds = api.getCredentials(institution['code'])
  ```

6. Create a member for our user with the credentials above. A member is a connection between an institution and a user. Creating a member automatically attempt to authenticate and gather account data (aggregate).
  ```python
  member = api.createMember(user['guid'], payload={
    "institution_code": institution['code'],
    "credentials": [
      {
        "guid": creds[0]['guid'],
        "value": "AwesomeBankUserName"
      },
      {
        "guid": creds[1]['guid'],
        "value": "AwesomeBankPassword"
      }
    ]
  })
  ```

7. Once the member has been created, you can check the aggregation status. A list of all statuses are available in the [Docs](http://atrium.mx.com/)
  ```python
  status = api.getMemberStatus(user['guid'], member['guid'])
  ```

  If the institution requires Multi-Factor Authentication (MFA), the status will return as `CHALLENGED` along side a `credentials` list  with the additional authentication requirements.

  ```json
  {
      "status": "CHALLENGED",
      "challenges": [
        {
            "type": "TEXT",
            "guid": "CRD-678",
          "label": "What city were you born in?",
        }
      ]
  }
  ```

  The MFA required credentials can also be retrieved with the `getMemberChallenges` method.

  Resume the aggregation by answering MFA

  ```python
  api.resumeMemberAgg(user['guid'], member['guid'], payload={
    "challenges": [
      {
        "guid": "CRD-678",
        "value": "New York"
      }
    ]
  })
  ```

8. Download all the datas!
  ```python
  api.getTransactions(user['guid'], queryParams={
    "results_per_page": 100
  })

  api.getHoldings(user['guid'])

  api.getAccounts(user['guid'])
  ```

## API Methods

### Users:
  * **_getUsers(queryParams={})_**

    Get a list of all the available users. Supports pagination query params.

  * **_createUser(payload={})_**

    Create a user with the attributes provided in payload.

  * **_readUser(userGuid)_**

    Read a user by a user GUID.

  * **_updateUser(userGuid, payload={})_**

    Update a user by its GUID with the attributes provided in payload.

  * **_deleteUser(userGuid)_**

    Delete a user by its GUID.

### Transactions:
  * **_getTransactions(userGuid, queryParams={})_**

    Get a list of transactions by a user GUID. Supports pagination, and date filtering through query parameters.

  * **_getTransactionsByAccount(userGuid, acctGuid, queryParams={})_**

    Get a list of transactions for a specific account by a user GUID and account GUID. Supports pagination, and date filtering through query parameters.

  * **_readTransaction(userGuid, transGuid)_**

    Read a specific transaction by user GUID and transaction GUID.

### Accounts:
  * **_getAccounts(userGuid, queryParams={})_**

    Get a list of accounts by a user GUID. Supports pagination query parameters.

  * **_readAccount(userGuid, acctGuid)_**

    Read a specific account by a user GUID and account GUID.


### Institutions:
  * **_getInstitutions(queryParams={})_**

    Get a list of institutions. Supports pagination query params and searching by name.

  * **_readInstitution(instGuid)_**

    Read a specific institution by the institution GUID.

  * **_getCredentials(instGuid)_**

    Get a list of required credentials by the institution GUID.

### Members:
  * **_getMembers(userGuid, queryParams={})_**

    Get a list of members by a user GUID. Supports pagination query parameters.

  * **_createMember(userGuid, payload={})_**

    Create a member for a user by user GUID with attributes provided in payload.

  * **_readMember(userGuid, memGuid)_**

    Read a member by user GUID and member GUID.

  * **_updateMember(userGuid, memGuid, payload={})_**

    Update a member by user GUID and member GUID with attributes provided in payload.

  * **_deleteMember(userGuid, memGuid)_**

    Delete a member by user GUID and member GUID.

  * **_getMemberStatus(userGuid, memGuid)_**

    Get the status for a member by user GUID and member GUID.

  * **_getMemberChallenges(userGuid, memGuid)_**

    Get a list of challenges for a member by user GUID and member GUID. Returns an empty object if there are no challenges.

  * **_startMemberAgg(userGuid, memGuid)_**

    Aggregate a member by user GUID and member GUID. Returns an empty object on success.

  * **_resumeMemberAgg(userGuid, memGuid, payload={})_**

    Resume member aggregation by user GUID and member GUID for when it was challenged. Payload should contain the answered MFA credentials.

### Holdings:
  * **_getHoldings(userGuid, queryParams={})_**

    Get a list of holdings by user GUID. Supports pagination query parameters.

  * **_readHolding(userGuid, holdGuid)_**

    Read a holding by user GUID and holding GUID.

## Contribute

  Coming Soon

## License
[MIT](LICENSE.md)
