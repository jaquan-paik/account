#!/bin/sh

COMMIT_SHA=${TRAVIS_COMMIT::8}

make ci-settings ns=$ENV access_key=$AWS_ACCESS_KEY_ID secret_key=$AWS_SECRET_ACCESS_KEY region=$AWS_DEFAULT_REGION
make ci-build-account env=$ENVIRONMENT

# tag image
make ci-tag-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=latest
make ci-tag-account env=$ENVIRONMENT ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
