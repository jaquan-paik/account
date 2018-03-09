.PHONY: all help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: install run

install: set-githook python-package-install settings log

run: lint test run-www

run-admin: python-package-install settings run-server-admin

run-www: python-package-install settings run-server-www


# install
npm-install:
	@npm install

python-package-install:
	@pip3 install -r docs/requirements/development.txt

settings:
	@cp docs/dev/settings/secrets.json ./secrets.json && python3.6 src/script/handle_secret_file.py encrypt

migrate:
	@python3.6 src/manage.py admin migrate

log:
	-@mkdir logs


# git
set-githook:
	@cd docs/git/ && ./install_git_hooks.sh


# run
run-server-admin:
	@python3.6 src/manage.py admin runserver 0.0.0.0:7000

run-server-www:
	@python3.6 src/manage.py www runserver 0.0.0.0:7001

worker-low:
	@cd src && celery -A sites.celery.celery worker -Q low_priority --loglevel=debug

worker-high:
	@cd src && celery -A sites.celery.celery worker -Q high_priority --loglevel=debug

scheduler:
	@cd src && celery -A sites.celery.celery beat --loglevel=debug


# pre-processing
lint:
	@python3.6 $(shell which pylint) ./src/apps/ ./src/infra/ ./src/lib/ --rcfile=.pylintrc && flake8

test:
	@python3.6 src/manage.py test test src

pm-test:
	@npm run test


# docker
docker-up:
	@docker-compose up --build


# release
ci-build-account:
	@make ci-build-account-with-site site=www
	@make ci-build-account-with-site site=admin

ci-build-celery:
	@docker build -t $(env)/account/celery:latest -f ./docs/docker/celery/Dockerfile .

ci-build-account-with-site:
	@docker build -t $(env)/account/$(site):latest -f ./docs/docker/account/Dockerfile . --build-arg SITE="$(site)"
