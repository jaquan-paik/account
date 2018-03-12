#!/bin/bash


if [ "$TRAVIS_BRANCH" == "test/development" ]; then
    ENV="development"
    ACCOUNT_ECR=$DEV_ACCOUNT_ECR
    AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
elif [ "$TRAVIS_BRANCH" == "release/development" ]; then
    ENV="development"
    ACCOUNT_ECR=$DEV_ACCOUNT_ECR
    AWS_ACCESS_KEY_ID=$DEV_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY=$DEV_AWS_SECRET_ACCESS_KEY
elif [ "$TRAVIS_BRANCH" == "release/development" ]; then
    ENV="production"
    ACCOUNT_ECR=$PROD_ACCOUNT_ECR
    AWS_ACCESS_KEY_ID=$PROD_AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY=$PROD_AWS_SECRET_ACCESS_KEY
fi

export ENV
export ACCOUNT_ECR
export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY
