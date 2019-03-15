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

## Postman Test
```
pipenv run make pm-test
```

# 4. ridibooks/account-dev 이미지 이용 가이드
- 변경이 가능한 설정 값들과 설정 방법
    - 변경 가능한 설정 값
        - site_domain
            - 사이트 도메인
            - default : `account.dev.ridi.io`
        - [allowed_hosts](https://docs.djangoproject.com/en/2.1/ref/settings/#std:setting-ALLOWED_HOSTS)
            - request의 host header로  허용되는 도메인 목록
            - white space delimiter 구분을 한다
            - 특별한 경우가 아니라면 `site_domain`과 같아야 한다
            - default : `account.dev.ridi.io account.test.ridi.io`
        - cookie_root_domain
            - 쿠키의 도메인
            - default : `.ridi.io`
        - store_url
            - store 주소
            - default : `https://master.test.ridi.io`
        - ridibooks_login_url
            - 리디북스의 로그인 페이지 주소
            - default : `https://master.test.ridi.io/account/login`

    - 설정 방법
        - 도커 실행시 지정된 키를 환경변수에 원하는 값으로 설정하면 변경 됨
        - 아래의 예시에서 확인 할 수 있음

- docker-compose 구성시 주의 사항
    - nginx의 서비스 이름은 반드시 지정한 `site_domain`과 같아야 함
    - `sentry_dsn`은 반드시 빈값으로 설정해야 함
    - [예시 account-dev-docker-compose.yml](https://github.com/ridi/account/blob/master/accoutn-dev-docker-compose.yml)

- nginx 필수 세팅
    - [proxy_redirect](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_redirect)
        - off
    - [proxy_pass_header](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass_header)
        - Server
    - [proxy_set_header](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_set_header)
        - Host $http_host
        - X-Real-IP $remote_addr
        - X-Forwarded-Proto $scheme
    - [proxy_pass](http://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_pass)
        - http://account-www:7001
    - [예시 account.conf](https://github.com/ridi/account/blob/master/docs/dev/nginx/account.conf)
    - [예시 cert](https://github.com/ridi/account/blob/master/docs/dev/cert/)
    

- 동작 하지 않을때 확인 할 것들
    - docker-compose 에서 nginx의 서비스의 이름이 `site_domain`과 동일한지
        - ridi/callback 요청을 받으면 해당 요청의 값을 가지고 ridi/oauth2로 self request를 보내는데, 이때 container는 pc의 hosts를 가지고 있지 않기 때문에 해당 설정은 필수임
    - vpn 혹은 사내에서 요청을 보내고 있는지
        - ridibooks/account-dev 이미지는 `account.dev.ridi.io` 와 동일한 인프라를 사용하고 있기 때문에 보안 옵션이 dev와 동일함

    - 위에 것들을 모두 확인 한 후에도 정삭 작동하지 않는다면 계정팀에게 문의해주시기 바랍니다.
