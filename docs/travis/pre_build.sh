#!/bin/bash

make ci-settings ns=$ENV

$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

docker pull ridibooks/python:bootstrap-django-2017.02.01
docker pull nginx:stable
