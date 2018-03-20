#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

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

wait $1 $2 $3