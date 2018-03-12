#!/bin/bash

ENV=$1
ACCOUNT_ECR=$2
AWS_ACCESS_KEY_ID=$3
AWS_SECRET_ACCESS_KEY=$4
COMMIT_SHA=${TRAVIS_COMMIT::8}

echo $COMMIT_SHA
echo $ENV
echo $ACCOUNT_ECR
echo $AWS_ACCESS_KEY_ID
echo $AWS_SECRET_ACCESS_KEY

## generate settings
#make ci-settings ns=$ENV access_key=$AWS_ACCESS_KEY_ID secret_key=$AWS_SECRET_ACCESS_KEY region=$AWS_DEFAULT_REGION
#
## aws ecr login
#$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)
#
## build image
#make ci-build-account env=$ENV
#make ci-build-celery env=$ENV
#
## tag image
#make ci-tag-library env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
#make ci-tag-library env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
#make ci-tag-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
#make ci-tag-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
#
## push image
#make ci-push-library env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
#make ci-push-library env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
#make ci-push-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
#make ci-push-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA

## deploy
#- ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY library-cluster library-service-all
#- ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY library-cluster library-service-api
#- ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY library-cluster library-service-www
