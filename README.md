# Account

[![Greenkeeper badge](https://badges.greenkeeper.io/ridi/account.svg)](https://greenkeeper.io/)
[![Build Status](https://travis-ci.org/ridi/account.svg?branch=master)](https://travis-ci.org/ridi/account)

# 1. Initialization

## Install Python3.6
```
brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/f2a764ef944b1080be64bd88dca9a1d80130c558/Formula/python.rb
```

## Install Pipenv
```
pip3 install pipenv
```

## Install mysql-connector
```
brew install mysql-connector-c
```

### Fix bug
```
vi $(which mysql_config)
```

Change 
```
# Create options
libs="-L$pkglibdir"
libs="$libs -l "
```
to 
```
# Create options
libs="-L$pkglibdir"
libs="$libs -lmysqlclient"
```
- https://github.com/PyMySQL/mysqlclient-python#note-about-bug-of-mysql-connectorc-on-macos


## Create virtual environment
```
pipenv install --dev
```


## Add to /etc/hosts
```
127.0.0.1 library-redis
127.0.0.1 library-mariadb
127.0.0.1 library-api.local.ridi.io
```

# 2. Docker run
```
make docker-up
```


# 3. Usage

## Install packages and Run
```
pipenv run make all
```

## Run server
```
pipenv run make run-www
```


## Linting
```
pipenv run make lint
```

## Test
```
pipenv run make test
``` 
