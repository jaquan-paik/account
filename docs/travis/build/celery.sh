#!/bin/sh

COMMIT_SHA=${TRAVIS_COMMIT::8}

make ci-build-celery env=$ENVIRONMENT

# tag image
make ci-tag-celery env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest
make ci-tag-celery env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
