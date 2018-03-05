# 1. Initialization

## Install Python3.6
```
brew install python3
python3 --version
```

## Create virtual environment
```
python3.6 -m venv venv
```

## Activate virtual environment
```
source venv/bin/activate
```
## Install Mysql
```
brew install mysql
```

## Add to /etc/hosts
```
127.0.0.1 mariadb 
127.0.0.1 redis
127.0.0.1 memcached

127.0.0.1 account.dev.ridi.com
127.0.0.1 account-admin.dev.ridi.com
```

# 2. Docker run
```
make docker-up
```


# 3. Run

## Install packages and Run
```
make all
```

## Install packages
```
make install
```

## Run server
```
make run
```

## Run celery
```
make woreker-low
make woreker-high
make scheduler
```

## Linting
```
make lint
```

## Test
```
make test
``` 
