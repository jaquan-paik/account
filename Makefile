.PHONY: all help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: install run

install: set-githook python-package-install settings

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

check-deprecated:
	@python3.6 src/script/check_deprecated_code.py


# docker
docker-up:
	@docker-compose up --build

docker-logs:
	@docker ps -a -q -f name=$(container) | awk '{print $1}' | xargs docker logs -f


# CI
ci-settings:
	@python3.6 src/script/handle_secret_file.py generate_$(ns)

ci-build-account:
	@docker build -t $(env)/account/www:latest -f ./docs/docker/account/Dockerfile .

ci-tag-account:
	@docker tag $(env)/account/www:latest $(ecr_path)/$(env)/account/www:$(tag)

ci-push-account:
	@docker push $(ecr_path)/$(env)/account/www:$(tag)


# -- Nginx -- #
nginx-build-image:
	@docker build -t $(env)/account/nginx:latest -f ./docs/docker/nginx/Dockerfile . --build-arg ENVIRONMENT="$(env)"

nginx-tag-image:
	@docker tag $(env)/account/nginx:latest $(ecr_path)/$(env)/account/nginx:$(tag)

nginx-push-image:
	@docker push $(ecr_path)/$(env)/account/nginx:$(tag)
