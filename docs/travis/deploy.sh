#!/bin/bash

COMMIT_SHA=${TRAVIS_COMMIT::8}

# deploy
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-scalable-cluster account-scalable & \
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-fixed-cluster account-fixed & \
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-fixed-cluster account-celery-beat & \
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-fixed-cluster account-high-worker & \
ecs deploy --timeout=1200 --region=$AWS_DEFAULT_REGION --access-key-id=$AWS_ACCESS_KEY_ID --secret-access-key=$AWS_SECRET_ACCESS_KEY account-fixed-cluster account-low-worker & \
wait
