#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

# deploy
ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    -i account-nginx $ACCOUNT_ECR/$ENVIRONMENT/account/nginx-www:latest \
    --timeout 600 \
    account-scalable-cluster account-scalable & \

ecs deploy --tag=$COMMIT_SHA --region=$AWS_DEFAULT_REGION \
    --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY \
    -i account-nginx $ACCOUNT_ECR/$ENVIRONMENT/account/nginx-admin:latest \
    --timeout 600 \
    account-fixed-cluster account-fixed & \
wait $1 $2