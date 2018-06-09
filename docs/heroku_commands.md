## clearing db

1. `heroku run bash`
2. `python migrate.py`

## clearing redis
`heroku redis:cli -a delphi-api --confirm delphi-api`
`flushall`

## clearing rabbitmq
purge queue from management portal
