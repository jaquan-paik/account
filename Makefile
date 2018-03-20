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
	@pip3 install -r docs/requirements/local.txt

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

check-deprecated:
	@python3.6 src/script/check_deprecated_code.py


# docker
docker-up:
	@docker-compose up --build


# CI
ci-settings:
	@export AWS_ACCESS_KEY_ID=$(access_key)
	@export AWS_SECRET_ACCESS_KEY=$(secret_key)
	@export AWS_DEFAULT_REGION=$(region)
	@python3.6 src/script/handle_secret_file.py generate_$(ns)

# -- Build -- #
ci-build-account:
	@make ci-build-account-with-site site=www
	@make ci-build-account-with-site site=admin

ci-build-celery:
	@docker build -t $(env)/account/celery:latest -f ./docs/docker//celery/Dockerfile . --build-arg ENVIRONMENT="$(env)"

ci-build-account-with-site:
	@docker build -t $(env)/account/$(site):latest -f ./docs/docker/account/Dockerfile . --build-arg ENVIRONMENT="$(env)" --build-arg SITE="$(site)"

# -- Tag -- #
ci-tag-account:
	@make ci-tag-account-with-site site=www
	@make ci-tag-account-with-site site=admin

ci-tag-celery:
	@make ci-tag-account-with-site site=celery

ci-tag-account-with-site:
	@docker tag $(env)/account/$(site):latest $(ecr_path)/$(env)/account/$(site):$(tag)

# -- Push -- #
ci-push-account:
	@make ci-push-account-with-site site=www
	@make ci-push-account-with-site site=admin

ci-push-celery:
	@make ci-push-account-with-site site=celery

ci-push-account-with-site:
	@docker push $(ecr_path)/$(env)/account/$(site):$(tag)


# -- Nginx -- #
nginx-build-image:
	@make nginx-build-image-with-site site=www
	@make nginx-build-image-with-site site=admin

nginx-build-image-with-site:
	@docker build -t $(env)/account/nginx-$(site):latest -f ./docs/docker/nginx/Dockerfile . --build-arg ENVIRONMENT="$(env)" --build-arg SITE="$(site)"

nginx-tag-image:
	@make nginx-tag-image-with-site site=www
	@make nginx-tag-image-with-site site=admin

nginx-tag-image-with-site:
	@docker tag $(env)/account/nginx-$(site):latest $(ecr_path)/$(env)/account/nginx-$(site):$(tag)

nginx-push-image:
	@make nginx-push-image-with-site site=www
	@make nginx-push-image-with-site site=admin

nginx-push-image-with-site:
	@docker push $(ecr_path)/$(env)/account/nginx-$(site):$(tag)
