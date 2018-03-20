#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest
make ci-push-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
