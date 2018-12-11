.PHONY: all help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

all: set-githook run-www

docker-all: global-python-package-install-development run-www


run-www: settings run-server-www


# git
set-githook:
	@cd docs/git/ && ./install_git_hooks.sh

# install
npm-install:
	@npm install

settings:
	@cp docs/dev/settings/secrets.json ./secrets.json && python3.6 src/script/handle_secret_file.py -a encrypt

ci-settings:
	@python3.6 src/script/handle_secret_file.py -a generate -e $(ns)

global-python-package-install-development:
	@pip3.6 install -U pip==18.0 pipenv && pipenv install --system --deploy --dev

global-python-package-install-staging:
	@pip3.6 install -U pip==18.0 pipenv && pipenv install --system --deploy

global-python-package-install-production:
	@pip3.6 install -U pip==18.0 pipenv && pipenv install --system --deploy


# run
run-server-www:
	@python3.6 src/manage.py runserver 0.0.0.0:7001


# pre-processing
lint:
	pylint ./src/apps/ ./src/infra/ ./src/lib/ --rcfile=.pylintrc
	flake8

check-deprecated:
	@python3.6 src/script/check_deprecated_code.py


# test
test:
	@python3.6 src/manage.py test src --noinput --settings=sites.settings.test

pm-test: pm-test-up pm-test-run pm-test-down


pm-test-up:
	@docker-compose  -f ./docs/postman/docker-compose.yml up -d

pm-test-run:
	@sh ./docs/docker/wait_for_it.sh "docker exec account-pm-test /bin/bash" "docker exec account-pm-test /bin/bash pm-test.sh"

pm-test-down:
	@docker-compose  -f ./docs/postman/docker-compose.yml down

pm-test-test:
	docker exec account-www-123987 /bin/bash ls && docker exec account-www-123987 /bin/bash pwd

# docker
docker-up:
	@docker-compose up

# docker
docker-down:
	@docker-compose down

docker-logs:
	@docker ps -a -q -f name=account-www | awk '{print $1}' | xargs docker logs -f
