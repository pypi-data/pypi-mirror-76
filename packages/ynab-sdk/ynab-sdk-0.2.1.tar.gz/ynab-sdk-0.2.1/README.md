# ynab-sdk-python
[![PyPI version](https://badge.fury.io/py/ynab-sdk.svg)](https://badge.fury.io/py/ynab-sdk)
[![Maintainability](https://api.codeclimate.com/v1/badges/b6042768d805939000c2/maintainability)](https://codeclimate.com/github/andreroggeri/ynab-sdk-python/maintainability)
[![codecov](https://codecov.io/gh/andreroggeri/ynab-sdk-python/branch/master/graph/badge.svg)](https://codecov.io/gh/andreroggeri/ynab-sdk-python)

Python implementation of the YNAB API ([https://api.youneedabudget.com/](https://api.youneedabudget.com/))

## Warning
This is pretty much a work in progress, the basic stuff is working, but nothing is guaranteed.
See below whats implemented and whats not

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `ynab-sdk-python`

```bash
pip install ynab-sdk
```

## Usage

```python
from ynab_sdk import YNAB

ynab = YNAB('some-key')
print(ynab.budgets.get_budgets())
```

## Endpoints
See below whats implemented (Not fully updated yet)


| Endpoint | Verb|Description |Working|Obs|
|---|---|---|---|---|
|/user|GET|Returns authenticated user information|NO||
|/budgets|GET|Returns budgets list with summary information|YES|
|/budgets/{budget_id}|GET|Returns a single budget with all related entities.  This resource is effectively a full budget export.|YES|
|/budgets/{budget_id}/settings|GET|Returns settings for a budget|YES|
|/budgets/{budget_id}/accounts|GET|Returns all accounts|YES|
|/budgets/{budget_id}/accounts/{account_id}|GET|Returns a single account|YES|
|/budgets/{budget_id}/categories|GET|Returns all categories grouped by category group.  Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).||
|/budgets/{budget_id}/categories/{category_id}|GET|Returns a single category.  Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).||
|/budgets/{budget_id}/months/{month}/categories/{category_id}|GET|Returns a single category for a specific budget month.  Amounts (budgeted, activity, balance, etc.) are specific to the current budget month (UTC).||
|/budgets/{budget_id}/months/{month}/categories/{category_id}|PATCH|Update a category for a specific month||
|/budgets/{budget_id}/payees|GET|Returns all payees|YES|
|/budgets/{budget_id}/payees/{payee_id}|GET|Returns single payee|YES|
|/budgets/{budget_id}/payee_locations|GET|Returns all payee locations|NO|
|/budgets/{budget_id}/payee_locations/{payee_location_id}|GET|Returns a single payee location|NO|
|/budgets/{budget_id}/payees/{payee_id}/payee_locations|GET|Returns all payee locations for the specified payee|NO|
|/budgets/{budget_id}/months|GET|Returns all budget months|NO|
|/budgets/{budget_id}/months/{month}|GET|Returns a single budget month|NO|
|/budgets/{budget_id}/transactions|GET|Returns budget transactions|YES|
|/budgets/{budget_id}/transactions|POST|Creates a single transaction or multiple transactions.  If you provide a body containing a 'transaction' object, a single transaction will be created and if you provide a body containing a 'transactions' array, multiple transactions will be created.|YES|
|/budgets/{budget_id}/transactions|PATCH|Updates multiple transactions, by 'id' or 'import_id'.|NO|
|/budgets/{budget_id}/transactions/{transaction_id}|GET|Returns a single transaction|YES|
|/budgets/{budget_id}/transactions/{transaction_id}|PUT|Updates a transaction|YES|
|/budgets/{budget_id}/transactions/bulk|POST|Creates multiple transactions.  Although this endpoint is still supported, it is recommended to use 'POST /budgets/{budget_id}/transactions' to create multiple transactions.|NO|
|/budgets/{budget_id}/accounts/{account_id}/transactions|GET|Returns all transactions for a specified account|YES|
|/budgets/{budget_id}/categories/{category_id}/transactions|GET|Returns all transactions for a specified category|NO|
|/budgets/{budget_id}/payees/{payee_id}/transactions|GET|Returns all transactions for a specified payee|NO|
|/budgets/{budget_id}/scheduled_transactions|GET|Returns all scheduled transactions|NO|
|/budgets/{budget_id}/scheduled_transactions/{scheduled_transaction_id}|GET|Returns a single scheduled transaction|NO|



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
