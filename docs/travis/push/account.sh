#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest
make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
