#!/bin/bash

ENV=$1
ACCOUNT_ECR=$2
AWS_ACCESS_KEY_ID=$3
AWS_SECRET_ACCESS_KEY=$4
COMMIT_SHA=${TRAVIS_COMMIT::8}

export AWS_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY

# generate settings
make ci-settings ns=$ENV access_key=$AWS_ACCESS_KEY_ID secret_key=$AWS_SECRET_ACCESS_KEY region=$AWS_DEFAULT_REGION

# aws ecr login
$(aws ecr get-login --no-include-email --region=$AWS_DEFAULT_REGION)

# build image
make ci-build-account env=$ENV & make ci-build-celery env=$ENV & wait $1 $2

# tag image
make ci-tag-account env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
make ci-tag-account env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
make ci-tag-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
make ci-tag-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA

# push image
make ci-push-account env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
make ci-push-account env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA
make ci-push-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=latest
make ci-push-celery env=$ENV ecr_path=$ACCOUNT_ECR tag=$COMMIT_SHA

# deploy
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    -i account-nginx $ACCOUNT_ECR/$ENV/account/nginx-www:latest \
    --timeout 600 \
    account-scalable-cluster account-scalable & \
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    -i account-nginx $ACCOUNT_ECR/$ENV/account/nginx-admin:latest \
    --timeout 600 \
    account-fixed-cluster account-fixed & \
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    --timeout 600 \
    account-fixed-cluster account-celery-beat & \
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    --timeout 600 \
    account-fixed-cluster account-celery-high-worker & \
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    --timeout 600 \
    account-fixed-cluster account-celery-low-worker & \
wait $1 $2 $3 $4 $5
