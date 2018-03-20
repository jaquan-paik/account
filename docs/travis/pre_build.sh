#!/bin/bash

ENV=$1
AWS_ACCESS_KEY_ID=$3
AWS_SECRET_ACCESS_KEY=$4

make ci-settings ns=$ENV access_key=$AWS_ACCESS_KEY_ID secret_key=$AWS_SECRET_ACCESS_KEY region=$AWS_DEFAULT_REGION

$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

docker pull ridibooks/python:bootstrap-django-2017.02.01
docker pull nginx:stable
